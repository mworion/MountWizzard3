############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #  ####
#      ##  ##  #  ##  #     #
#     # # # #  # # # #     ###
#    #  ##  #  ##  ##        #
#   #   #   #  #   #     ####
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.4
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
############################################################
import logging
import PyQt5
import time
from queue import Queue
from astrometry import transform


class MountStatusRunnerMedium(PyQt5.QtCore.QObject):
    logger = logging.getLogger(__name__)

    CYCLE_STATUS_MEDIUM = 3000
    CYCLE_COMMAND = 200

    def __init__(self, app, thread, data, signalConnected):
        super().__init__()

        self.app = app
        self.thread = thread
        self.data = data
        self.signalConnected = signalConnected
        self.mutexIsRunning = PyQt5.QtCore.QMutex()
        self.isRunning = False
        self.connected = False
        self.socket = None
        self.messageString = ''
        self.sendCommandQueue = Queue()
        self.transform = transform.Transform(self.app)

    def run(self):
        self.logger.info('mount medium started')
        self.mutexIsRunning.lock()
        if not self.isRunning:
            self.isRunning = True
        self.mutexIsRunning.unlock()
        self.socket = PyQt5.QtNetwork.QTcpSocket()
        self.socket.hostFound.connect(self.handleHostFound)
        self.socket.connected.connect(self.handleConnected)
        self.socket.stateChanged.connect(self.handleStateChanged)
        self.socket.disconnected.connect(self.handleDisconnect)
        self.socket.readyRead.connect(self.handleReadyRead)
        self.socket.error.connect(self.handleError)
        self.doCommandQueue()

    def stop(self):
        self.mutexIsRunning.lock()
        self.isRunning = False
        self.mutexIsRunning.unlock()
        self.thread.quit()
        self.thread.wait()

    def destruct(self):
        if self.socket.state() != 3:
            self.socket.abort()
        else:
            self.socket.disconnectFromHost()
        self.socket.hostFound.disconnect(self.handleHostFound)
        self.socket.connected.disconnect(self.handleConnected)
        self.socket.stateChanged.disconnect(self.handleStateChanged)
        self.socket.disconnected.disconnect(self.handleDisconnect)
        self.socket.readyRead.disconnect(self.handleReadyRead)
        self.socket.error.disconnect(self.handleError)
        self.socket.close()

    def doCommandQueue(self):
        if not self.sendCommandQueue.empty() and self.connected:
            command = self.sendCommandQueue.get()
            self.sendCommand(command)
        if not self.connected and self.socket.state() == 0:
            self.socket.connectToHost(self.data['MountIP'], self.data['MountPort'])
            self.sendCommandQueue.queue.clear()
        # loop
        if self.isRunning:
            PyQt5.QtCore.QTimer.singleShot(self.CYCLE_COMMAND, self.doCommandQueue)

    def handleHostFound(self):
        self.app.sharedMountDataLock.lockForRead()
        self.logger.debug('Mount RunnerMedium found at {}:{}'.format(self.data['MountIP'], self.data['MountPort']))
        self.app.sharedMountDataLock.unlock()

    def handleConnected(self):
        self.socket.setSocketOption(PyQt5.QtNetwork.QAbstractSocket.LowDelayOption, 1)
        self.connected = True
        self.signalConnected.emit({'Medium': True})
        self.getStatusMedium()
        self.app.sharedMountDataLock.lockForRead()
        self.logger.info('Mount RunnerMedium connected at {0}:{1}'.format(self.data['MountIP'], self.data['MountPort']))
        self.app.sharedMountDataLock.unlock()

    def handleError(self, socketError):
        self.logger.warning('Mount RunnerMedium connection fault: {0}'.format(self.socket.errorString()))

    def handleStateChanged(self):
        self.logger.debug('Mount RunnerMedium connection has state: {0}'.format(self.socket.state()))

    def handleDisconnect(self):
        self.logger.info('Mount RunnerMedium connection is disconnected from host')
        self.signalConnected.emit({'Medium': False})
        self.connected = False

    def sendCommand(self, command):
        if self.connected and self.isRunning:
            if self.socket.state() == PyQt5.QtNetwork.QAbstractSocket.ConnectedState:
                self.socket.write(bytes(command + '\r', encoding='ascii'))
                self.socket.flush()
            else:
                self.logger.warning('Socket RunnerMedium not connected')

    def getStatusMedium(self):
        doRefractionUpdate = False
        pressure = 950
        temperature = 10
        if self.app.ui.checkAutoRefractionContinous.isChecked():
            doRefractionUpdate = True
            self.app.sharedEnvironmentDataLock.lockForRead()
            if 'MovingAverageTemperature' in self.app.workerEnvironment.data and 'MovingAveragePressure' in self.app.workerEnvironment.data and self.app.workerEnvironment.isRunning:
                pressure = self.app.workerEnvironment.data['MovingAveragePressure']
                temperature = self.app.workerEnvironment.data['MovingAverageTemperature']
            self.app.sharedEnvironmentDataLock.unlock()
        if self.app.ui.checkAutoRefractionNotTracking.isChecked():
            # if there is no tracking, than updating is good
            self.app.sharedMountDataLock.lockForRead()
            if 'Status' in self.data:
                if self.data['Status'] != '0':
                    doRefractionUpdate = True
            self.app.sharedMountDataLock.unlock()
            self.app.sharedEnvironmentDataLock.lockForRead()
            if 'Temperature' in self.app.workerEnvironment.data and 'Pressure' in self.app.workerEnvironment.data and self.app.workerEnvironment.isRunning:
                pressure = self.app.workerEnvironment.data['Pressure']
                temperature = self.app.workerEnvironment.data['Temperature']
            self.app.sharedEnvironmentDataLock.unlock()
        if doRefractionUpdate:
            if (900.0 < pressure < 1100.0) and (-30.0 < temperature < 35.0):
                self.app.mountCommandQueue.put(':SRPRS{0:04.1f}#'.format(pressure))
                if temperature > 0:
                    self.app.mountCommandQueue.put(':SRTMP+{0:03.1f}#'.format(temperature))
                else:
                    self.app.mountCommandQueue.put(':SRTMP-{0:3.1f}#'.format(-temperature))
        self.sendCommandQueue.put(':GMs#:Gmte#:Glmt#:Glms#:GRTMP#:GRPRS#')

    def handleReadyRead(self):
        # Get message from socket.
        while self.socket.bytesAvailable():
            tmp = self.socket.read(1024).decode()
            self.messageString += tmp
            # print(self.messageString)
        if len(self.messageString) < 28:
            return
        else:
            messageToProcess = self.messageString[:28]
            self.messageString = self.messageString[28:]
        # Try and parse the message.
        try:
            if len(messageToProcess) == 0:
                return
            self.app.sharedMountDataLock.lockForWrite()
            if 'FW' not in self.data:
                self.data['FW'] = 0
            valueList = messageToProcess.strip('#').split('#')
            # print(valueList)
            # all parameters are delivered
            if len(valueList) >= 4:
                if len(valueList[0]) > 0:
                    self.data['SlewRate'] = valueList[0]
                if len(valueList[1]) > 0:
                    self.data['TimeToFlip'] = int(float(valueList[1]))
                if len(valueList[2]) > 0:
                    self.data['MeridianLimitTrack'] = int(float(valueList[2]))
                if len(valueList[3]) > 0:
                    self.data['MeridianLimitSlew'] = int(float(valueList[3]))
                self.data['TimeToMeridian'] = int(self.data['TimeToFlip'] - self.data['MeridianLimitTrack'] / 360 * 24 * 60)
                if len(valueList[4]) > 0:
                    self.data['RefractionTemperature'] = valueList[4]
                if len(valueList[5]) > 0:
                    self.data['RefractionPressure'] = valueList[5]
            else:
                self.logger.warning('Parsing Status Medium combined command valueList is not OK: length:{0} content:{1}'.format(len(valueList), valueList))
        except Exception as e:
            self.logger.error('Parsing Status Medium combined command got error:{0}'.format(e))
        finally:
            self.app.sharedMountDataLock.unlock()
            if self.isRunning:
                PyQt5.QtCore.QTimer.singleShot(self.CYCLE_STATUS_MEDIUM, self.getStatusMedium)
