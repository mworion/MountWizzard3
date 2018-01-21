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
import logging
import platform
import threading
import PyQt5
import time
if platform.system() == 'Windows':
    from win32com.client.dynamic import Dispatch
    import pythoncom


class Environment(PyQt5.QtCore.QObject):
    logger = logging.getLogger(__name__)
    finished = PyQt5.QtCore.pyqtSignal()

    signalEnvironmentConnected = PyQt5.QtCore.pyqtSignal([int])

    CYCLE_DATA = 2000

    def __init__(self, app):
        super().__init__()
        self.isRunning = False
        self._mutex = PyQt5.QtCore.QMutex()

        self.app = app
        self.data = {
            'Connected': False
        }
        self.ascom = None
        self.ascomChooser = None
        self.ascomDriverName = ''
        self.chooserLock = threading.Lock()

    def initConfig(self):
        # first build the pull down menu
        if self.app.ui.pd_chooseEnvironment.receivers(self.app.ui.pd_chooseEnvironment.currentIndexChanged) > 0:
            self.app.ui.pd_chooseEnvironment.currentIndexChanged.disconnect()
        self.app.ui.pd_chooseEnvironment.clear()
        self.app.ui.pd_chooseEnvironment.addItem('No Environment')
        if platform.system() == 'Windows':
            self.app.ui.pd_chooseEnvironment.addItem('ASCOM')
        self.app.ui.pd_chooseEnvironment.addItem('INDI')
        # load the config including pull down setup
        try:
            if 'EnvironmentAscomDriverName' in self.app.config:
                self.ascomDriverName = self.app.config['EnvironmentAscomDriverName']
                self.app.ui.le_ascomEnvironmentDriverName.setText(self.app.config['EnvironmentAscomDriverName'])
            if 'Environment' in self.app.config:
                self.app.ui.pd_chooseEnvironment.setCurrentIndex(int(self.app.config['Environment']))
        except Exception as e:
            self.logger.error('item in config.cfg not be initialize, error:{0}'.format(e))
        finally:
            pass
        # connect change in environment to the subroutine of setting it up
        self.app.ui.pd_chooseEnvironment.currentIndexChanged.connect(self.chooserEnvironment)

    def storeConfig(self):
        self.app.config['EnvironmentAscomDriverName'] = self.ascomDriverName
        self.app.config['Environment'] = self.app.ui.pd_chooseEnvironment.currentIndex()

    def startAscom(self):
        if self.ascomDriverName != '' and not self.ascom:
            try:
                self.ascom = Dispatch(self.ascomDriverName)
                self.ascom.connected = True
                self.logger.info('Driver chosen:{0}'.format(self.ascomDriverName))
                # connection made
                self.data['Connected'] = True
            except Exception as e:
                self.logger.error('Could not dispatch driver: {0} and connect it, error: {1}'.format(self.ascomDriverName, e))
            finally:
                pass
        else:
            # no connection made
            self.data['Connected'] = False

    def stopAscom(self):
        try:
            if self.ascom:
                self.ascom.connected = False
        except Exception as e:
            self.logger.error('Could not stop driver: {0} and close it, error: {1}'.format(self.ascomDriverName, e))
        finally:
            self.data['Connected'] = False
            self.ascom = None

    def chooserEnvironment(self):
        self.chooserLock.acquire()
        if self.app.ui.pd_chooseEnvironment.currentText().startswith('No Environment'):
            self.stopAscom()
            self.data['Connected'] = False
            self.logger.info('Actual environment is None')
        elif self.app.ui.pd_chooseEnvironment.currentText().startswith('ASCOM'):
            self.startAscom()
            self.logger.info('Actual environment is ASCOM')
        elif self.app.ui.pd_chooseEnvironment.currentText().startswith('INDI'):
            self.stopAscom()
            if self.app.workerINDI.weatherDevice != '':
                self.data['Connected'] = self.app.workerINDI.data['Device'][self.app.workerINDI.weatherDevice]['CONNECTION']['CONNECT'] == 'On'
            else:
                self.data['Connected'] = False
            self.logger.info('Actual environment is INDI')
        if self.app.ui.pd_chooseEnvironment.currentText().startswith('No Environment'):
            self.signalEnvironmentConnected.emit(0)
        self.chooserLock.release()

    def run(self):
        # a running thread is shown with variable isRunning = True. This thread should hav it's own event loop.
        if not self.isRunning:
            self.isRunning = True
        if platform.system() == 'Windows':
            pythoncom.CoInitialize()
        self.chooserEnvironment()
        self.getData()
        while self.isRunning:
            if self.app.ui.pd_chooseEnvironment.currentText().startswith('INDI'):
                if self.app.workerINDI.weatherDevice != '':
                    self.data['Connected'] = self.app.workerINDI.data['Device'][self.app.workerINDI.weatherDevice]['CONNECTION']['CONNECT'] == 'On'
                else:
                    self.data['Connected'] = False
            if self.data['Connected']:
                self.signalEnvironmentConnected.emit(3)
            else:
                if self.app.ui.pd_chooseEnvironment.currentText().startswith('No Environment'):
                    self.signalEnvironmentConnected.emit(0)
                else:
                    self.signalEnvironmentConnected.emit(1)
            time.sleep(0.2)
            PyQt5.QtWidgets.QApplication.processEvents()
        if platform.system() == 'Windows':
            pythoncom.CoUninitialize()
        self.finished.emit()

    def stop(self):
        self._mutex.lock()
        self.isRunning = False
        self._mutex.unlock()
        self.stopAscom()

    def getData(self):
        if self.data['Connected']:
            if self.app.ui.pd_chooseEnvironment.currentText().startswith('ASCOM'):
                try:
                    if self.ascom:
                        if self.ascom.connected:
                            self.getAscomData()
                except Exception as e:
                    self.logger.error('Problem accessing ASCOm driver, error: {0}'.format(e))
                finally:
                    pass
            elif self.app.ui.pd_chooseEnvironment.currentText().startswith('INDI'):
                if self.app.workerINDI.data['Connected']:
                    self.getINDIData()
        else:
            self.data = {
                'Connected': False,
                'DewPoint': 0.0,
                'Temperature': 0.0,
                'Humidity': 0,
                'Pressure': 0,
                'CloudCover': 0,
                'RainRate': 0,
                'WindSpeed': 0,
                'WindDirection': 0,
                'SQR': 0
            }
        PyQt5.QtCore.QTimer.singleShot(self.CYCLE_DATA, self.getData)

    def getINDIData(self):
        pass

    # noinspection PyBroadException
    def getAscomData(self):
        try:
            self.data['DewPoint'] = self.ascom.DewPoint
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['Temperature'] = self.ascom.Temperature
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['Humidity'] = self.ascom.Humidity
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['Pressure'] = self.ascom.Pressure
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['SQR'] = self.ascom.SkyQuality
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['CloudCover'] = self.ascom.CloudCover
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['RainRate'] = self.ascom.RainRate
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['WindSpeed'] = self.ascom.WindSpeed
        except Exception:
            pass
        finally:
            pass
        try:
            self.data['WindDirection'] = self.ascom.WindDirection
        except Exception:
            pass
        finally:
            pass

    def setupDriver(self):
        try:
            self.ascomChooser = Dispatch('ASCOM.Utilities.Chooser')
            self.ascomChooser.DeviceType = 'ObservingConditions'
            self.ascomDriverName = self.ascomChooser.Choose(self.ascomDriverName)
            self.app.messageQueue.put('Driver chosen:{0}\n'.format(self.ascomDriverName))
            self.logger.info('Driver chosen:{0}'.format(self.ascomDriverName))
        except Exception as e:
            self.app.messageQueue.put('#BRDriver error in Setup Driver\n')
            self.logger.error('General error:{0}'.format(e))
        finally:
            pass
