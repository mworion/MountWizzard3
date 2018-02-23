############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
############################################################
import json
import logging
import platform
import time
import PyQt5
# packages for handling web interface to SGPro
from urllib import request
import requests


class SGPro(PyQt5.QtCore.QObject):
    logger = logging.getLogger(__name__)
    cameraStatusText = PyQt5.QtCore.pyqtSignal(str)
    solverStatusText = PyQt5.QtCore.pyqtSignal(str)
    cameraExposureTime = PyQt5.QtCore.pyqtSignal(str)

    CYCLESTATUS = 500
    CYCLEPROPS = 3000

    SOLVERSTATUS = {'ERROR': 'ERROR', 'DISCONNECTED': 'DISCONNECTED', 'IDLE': 'IDLE', 'BUSY': 'BUSY'}
    CAMERASTATUS = {'ERROR': 'ERROR', 'DISCONNECTED': 'DISCONNECTED', 'BUSY': 'DOWNLOADING', 'READY': 'IDLE', 'IDLE': 'IDLE', 'INTEGRATING': 'INTEGRATING'}

    def __init__(self, app, thread, commandQueue):
        super().__init__()
        self.app = app
        self.thread = thread
        self.commandQueue = commandQueue
        self.isRunning = False
        self.cancel = False
        self.mutexIsRunning = PyQt5.QtCore.QMutex()
        self.data = {'Camera': {}, 'Solver': {}}
        self.tryConnectionCounter = 0
        self.data['Camera']['AppAvailable'] = True
        self.data['Camera']['AppName'] = 'None'
        self.data['Camera']['AppInstallPath'] = 'None'
        self.data['Solver']['AppAvailable'] = True
        self.data['Solver']['AppName'] = 'None'
        self.data['Solver']['AppInstallPath'] = 'None'
        self.data['Camera']['Status'] = '---'
        self.data['Camera']['CONNECTION'] = {'CONNECT': 'Off'}
        self.data['Solver']['Status'] = '---'
        self.data['Solver']['CONNECTION'] = {'CONNECT': 'Off'}

        self.host = '127.0.0.1'
        self.port = 59590
        self.ipSGProBase = 'http://' + self.host + ':' + str(self.port)
        self.ipSGPro = 'http://' + self.host + ':' + str(self.port) + '/json/reply/'
        self.captureImagePath = 'SgCaptureImage'
        self.connectDevicePath = 'SgConnectDevicePath'
        self.disconnectDevicePath = 'SgDisconnectDevicePath'
        self.getCameraPropsPath = 'SgGetCameraProps'
        self.getDeviceStatusPath = 'SgGetDeviceStatus'
        self.enumerateDevicePath = 'SgEnumerateDevices'
        self.getImagePath = 'SgGetImagePath'
        self.getSolvedImageDataPath = 'SgGetSolvedImageData'
        self.solveImagePath = 'SgSolveImage'

        self.appExe = 'Sequence Generator.exe'
        if platform.system() == 'Windows':
            # sgpro only supported on local machine
            self.data['Camera']['AppAvailable'], self.data['Camera']['AppName'], self.data['Camera']['AppInstallPath'] = self.app.checkRegistrationKeys('Sequence Generator')
            if self.data['Camera']['AppAvailable']:
                self.app.messageQueue.put('Found: {0}\n'.format(self.data['Camera']['AppName']))
                self.logger.info('Name: {0}, Path: {1}'.format(self.data['Camera']['AppName'], self.data['Camera']['AppInstallPath']))
            else:
                self.logger.info('Application SGPro not found on computer')
            self.data['Solver']['AppAvailable'] = self.data['Camera']['AppAvailable']
            self.data['Solver']['AppName'] = self.data['Camera']['AppName']
            self.data['Solver']['AppInstallPath'] = self.data['Camera']['AppInstallPath']

    def run(self):
        # a running thread is shown with variable isRunning = True. This thread should have it's own event loop.
        self.mutexIsRunning.lock()
        if not self.isRunning:
            self.isRunning = True
        self.mutexIsRunning.unlock()
        self.setStatus()
        self.setCameraProps()
        while self.isRunning:
            if not self.commandQueue.empty():
                command = self.commandQueue.get()
                if command['Command'] == 'GetImage':
                    command['ImageParams'] = self.getImage(command['ImageParams'])
                elif command['Command'] == 'SolveImage':
                    command['ImageParams'] = self.solveImage(command['ImageParams'])
            time.sleep(0.2)
            PyQt5.QtWidgets.QApplication.processEvents()

    def stop(self):
        self.mutexIsRunning.lock()
        self.isRunning = False
        self.mutexIsRunning.unlock()
        self.thread.quit()
        self.thread.wait()

    def setStatus(self):
        suc, state, message = self.SgGetDeviceStatus('Camera')
        if suc:
            if state in self.CAMERASTATUS:
                if self.CAMERASTATUS[state] == 'DISCONNECTED':
                    self.data['Camera']['CONNECTION']['CONNECT'] = 'Off'
                else:
                    self.data['Camera']['CONNECTION']['CONNECT'] = 'On'
                    if 'integrating' in message:
                        self.data['Camera']['Status'] = 'INTEGRATING'
                        self.cameraStatusText.emit('INTEGRATE')
                    elif 'downloading' in message:
                        self.data['Camera']['Status'] = 'DOWNLOADING'
                        self.cameraStatusText.emit('DOWNLOAD')
                    elif 'ready' in message or 'idle' in message:
                        self.data['Camera']['Status'] = 'IDLE'
                        self.cameraStatusText.emit('IDLE')
            else:
                self.logger.error('Unknown camera status: {0}, message: {1}'.format(state, message))
        else:
            self.data['Camera']['Status'] = 'ERROR'
            self.data['Camera']['CONNECTION']['CONNECT'] = 'Off'
            self.cameraStatusText.emit(self.data['Camera']['Status'])
            self.cameraExposureTime.emit('---')

        # todo: SGPro does not report the status of the solver right. Even if not set in SGPro I get positive feedback and IDLE
        suc, state, message = self.SgGetDeviceStatus('PlateSolver')
        if suc:
            if state in self.SOLVERSTATUS:
                self.data['Solver']['Status'] = self.SOLVERSTATUS[state]
                if self.SOLVERSTATUS[state] == 'DISCONNECTED':
                    self.data['Solver']['CONNECTION']['CONNECT'] = 'Off'
                    self.solverStatusText.emit('DISCONN')
                else:
                    self.data['Solver']['CONNECTION']['CONNECT'] = 'On'
                    self.solverStatusText.emit('IDLE')
            else:
                self.logger.error('Unknown solver status: {0}'.format(state))
        else:
            self.data['Solver']['Status'] = 'ERROR'
            self.data['Solver']['CONNECTION']['CONNECT'] = 'Off'
            self.solverStatusText.emit('---')

        if 'CONNECTION' in self.data['Camera']:
            if self.data['Camera']['CONNECTION']['CONNECT'] == 'On':
                self.app.workerModelingDispatcher.signalStatusCamera.emit(3)
            else:
                self.app.workerModelingDispatcher.signalStatusCamera.emit(2)
        else:
            self.app.workerModelingDispatcher.signalStatusCamera.emit(0)

        if 'CONNECTION' in self.data['Solver']:
            if self.data['Solver']['CONNECTION']['CONNECT'] == 'On':
                self.app.workerModelingDispatcher.signalStatusSolver.emit(3)
            else:
                self.app.workerModelingDispatcher.signalStatusSolver.emit(2)
        else:
            self.app.workerModelingDispatcher.signalStatusSolver.emit(0)

        if self.isRunning:
            PyQt5.QtCore.QTimer.singleShot(self.CYCLESTATUS, self.setStatus)

    def setCameraProps(self):
        if 'CONNECTION' in self.data['Camera']:
            if self.data['Camera']['CONNECTION']['CONNECT'] == 'On':
                value = self.SgGetCameraProps()
                if value['Success']:
                    if 'GainValues' not in value['GainValues']:
                        self.data['Camera']['Gain'] = ['High']
                    else:
                        self.data['Camera']['Gain'] = value['GainValues']
                    self.data['Camera']['Message'] = value['Message']
                    if value['SupportsSubframe']:
                        self.data['Camera']['CCD_FRAME'] = {}
                        self.data['Camera']['CCD_FRAME']['HEIGHT'] = value['NumPixelsX']
                        self.data['Camera']['CCD_FRAME']['WIDTH'] = value['NumPixelsY']
                        self.data['Camera']['CCD_FRAME']['X'] = 0
                        self.data['Camera']['CCD_FRAME']['Y'] = 0
                    self.data['Camera']['CCD_INFO'] = {}
                    self.data['Camera']['CCD_INFO']['CCD_MAX_X'] = value['NumPixelsX']
                    self.data['Camera']['CCD_INFO']['CCD_MAX_Y'] = value['NumPixelsY']

        if self.isRunning:
            PyQt5.QtCore.QTimer.singleShot(self.CYCLEPROPS, self.setCameraProps)

    def getImage(self, imageParams):
        suc, mes, guid = self.SgCaptureImage(binningMode=imageParams['Binning'],
                                             exposureLength=imageParams['Exposure'],
                                             iso=str(imageParams['Iso']),
                                             gain='Not Set',
                                             speed=imageParams['Speed'],
                                             frameType='Light',
                                             filename=imageParams['File'],
                                             path=imageParams['BaseDirImages'],
                                             useSubframe=imageParams['CanSubframe'],
                                             posX=imageParams['OffX'],
                                             posY=imageParams['OffY'],
                                             width=imageParams['SizeX'],
                                             height=imageParams['SizeY'])
        self.logger.info('message: {0}'.format(mes))
        if suc:
            while True:
                suc, path = self.SgGetImagePath(guid)
                if suc:
                    break
                else:
                    time.sleep(0.1)
                    PyQt5.QtWidgets.QApplication.processEvents()
            imageParams['Imagepath'] = path
        else:
            imageParams['Imagepath'] = ''
        imageParams['Message'] = mes
        return imageParams

    def solveImage(self, imageParams):
        suc, mes, guid = self.SgSolveImage(imageParams['Imagepath'],
                                           RaHint=imageParams['RaJ2000'],
                                           DecHint=imageParams['DecJ2000'],
                                           ScaleHint=imageParams['ScaleHint'],
                                           BlindSolve=imageParams['Blind'],
                                           UseFitsHeaders=False)
        if not suc:
            self.logger.warning('Solver no start, message: {0}'.format(mes))
            imageParams['Message'] = mes
        while True:
            suc, mes, ra_sol, dec_sol, scale, angle, timeTS = self.SgGetSolvedImageData(guid)
            mes = mes.strip('\n')
            if mes[:7] in ['Matched', 'Solve t', 'Valid s', 'succeed']:
                self.logger.info('Imaging parameters {0}'.format(imageParams))
                imageParams['RaJ2000Solved'] = float(ra_sol)
                imageParams['DecJ2000Solved'] = float(dec_sol)
                imageParams['Scale'] = float(scale)
                imageParams['Angle'] = float(angle)
                imageParams['TimeTS'] = float(timeTS)
                break
            elif mes != 'Solving':
                break
            else:
                time.sleep(0.2)
                PyQt5.QtWidgets.QApplication.processEvents()
        imageParams['Message'] = mes
        return imageParams

    def SgCaptureImage(self, binningMode=1, exposureLength=1,
                       gain=None, iso=None, speed=None, frameType=None, filename=None,
                       path=None, useSubframe=False, posX=0, posY=0,
                       width=1, height=1):
        # reference {"BinningMode":0,"ExposureLength":0,"Gain":"String","Speed":"Normal","FrameType":"Light",
        # reference "Path":"String","UseSubframe":false,"X":0,"Y":0,"Width":0,"Height":0}
        data = {"BinningMode": binningMode, "ExposureLength": exposureLength, "UseSubframe": useSubframe, "X": posX, "Y": posY,
                "Width": width, "Height": height}
        if gain:
            data['Gain'] = gain
        if iso:
            data['Iso'] = iso
        if speed:
            data['Speed'] = speed
        if frameType:
            data['FrameType'] = frameType
        if path and filename:
            data['Path'] = path + '/' + filename
        try:
            result = requests.post(self.ipSGPro + self.captureImagePath, data=bytes(json.dumps(data).encode('utf-8')))
            result = json.loads(result.text)
            return result['Success'], result['Message'], result['Receipt']
        except Exception as e:
            self.logger.error('error: {0}'.format(e))
            return False, 'Request failed', ''

    def SgGetCameraProps(self):
        # reference {}
        data = {}
        try:
            result = requests.post(self.ipSGPro + self.getCameraPropsPath, data=bytes(json.dumps(data).encode('utf-8')))
            result = json.loads(result.text)
            return result
        except Exception as e:
            self.logger.error('error: {0}'.format(e))
            return False, 'Request failed', '', '', ''

    def SgGetDeviceStatus(self, device):
        # reference {"Device": "Camera"}, devices are "Camera", "FilterWheel", "Focuser", "Telescope" and "PlateSolver"}
        data = {'Device': device}
        try:
            result = requests.post(self.ipSGPro + self.getDeviceStatusPath, data=bytes(json.dumps(data).encode('utf-8')))
            result = json.loads(result.text)
            if 'Message' not in result:
                result['Message'] = 'None'
            return result['Success'], result['State'], result['Message']
        except Exception as e:
            self.logger.error('error: {0}'.format(e))
            return False, 'Request failed', 'Request failed'

    def SgGetImagePath(self, _guid):
        # reference {"Receipt":"00000000000000000000000000000000"}
        data = {'Receipt': _guid}
        try:
            result = requests.post(self.ipSGPro + self.getImagePath, data=bytes(json.dumps(data).encode('utf-8')))
            result = json.loads(result.text)
            return result['Success'], result['Message']
        except Exception as e:
            self.logger.error('error: {0}'.format(e))
            return False, 'Request failed'

    def SgGetSolvedImageData(self, _guid):
        # reference {"Receipt":"00000000000000000000000000000000"}
        data = {'Receipt': _guid}
        try:
            result = requests.post(self.ipSGPro + self.getSolvedImageDataPath, data=bytes(json.dumps(data).encode('utf-8')))
            result = json.loads(result.text)
            return result['Success'], result['Message'], result['Ra'], result['Dec'], result['Scale'], result['Angle'], result['TimeToSolve']
        except Exception as e:
            self.logger.error('error: {0}'.format(e))
            return False, 'Request failed', '', '', '', '', ''

    def SgSolveImage(self, path, RaHint=None, DecHint=None, ScaleHint=None, BlindSolve=False, UseFitsHeaders=False):
        # reference {"ImagePath":"String","RaHint":0,"DecHint":0,"ScaleHint":0,"BlindSolve":false,"UseFitsHeadersForHints":false}
        data = {"ImagePath": path, "BlindSolve": BlindSolve, "UseFitsHeadersForHints": UseFitsHeaders}
        if RaHint:
            data['RaHint'] = RaHint
        if DecHint:
            data['DecHint'] = DecHint
        if ScaleHint:
            data['ScaleHint'] = ScaleHint
        try:
            result = requests.post(self.ipSGPro + self.solveImagePath, data=bytes(json.dumps(data).encode('utf-8')))
            result = json.loads(result.text)
            return result['Success'], result['Message'], result['Receipt']
        except Exception as e:
            self.logger.error('error: {0}'.format(e))
            return False, 'Request failed', ''
