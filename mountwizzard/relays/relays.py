############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017
#
# Licence APL2.0
#
############################################################
import logging
import time
import requests
import urllib
from baseclasses import checkParamIP


class Relays:
    logger = logging.getLogger(__name__)                                                                                    # logging enabling

    def __init__(self, app):
        self.app = app
        self.stat = [False, False, False, False, False, False, False, False, False]
        self.username = ''
        self.password = ''
        self.relayIP = ''
        self.connected = False
        self.checkIP = checkParamIP.CheckIP()
        self.app.ui.btn_relay1.clicked.connect(lambda: self.runRelay(1))
        self.app.ui.btn_relay2.clicked.connect(lambda: self.runRelay(2))
        self.app.ui.btn_relay3.clicked.connect(lambda: self.runRelay(3))
        self.app.ui.btn_relay4.clicked.connect(lambda: self.runRelay(4))
        self.app.ui.btn_relay5.clicked.connect(lambda: self.runRelay(5))
        self.app.ui.btn_relay6.clicked.connect(lambda: self.runRelay(6))
        self.app.ui.btn_relay7.clicked.connect(lambda: self.runRelay(7))
        self.app.ui.btn_relay8.clicked.connect(lambda: self.runRelay(8))
        self.app.ui.relay1Text.textChanged.connect(lambda: self.app.ui.btn_relay1.setText(self.app.ui.relay1Text.text()))
        self.app.ui.relay2Text.textChanged.connect(lambda: self.app.ui.btn_relay2.setText(self.app.ui.relay2Text.text()))
        self.app.ui.relay3Text.textChanged.connect(lambda: self.app.ui.btn_relay3.setText(self.app.ui.relay3Text.text()))
        self.app.ui.relay4Text.textChanged.connect(lambda: self.app.ui.btn_relay4.setText(self.app.ui.relay4Text.text()))
        self.app.ui.relay5Text.textChanged.connect(lambda: self.app.ui.btn_relay5.setText(self.app.ui.relay5Text.text()))
        self.app.ui.relay6Text.textChanged.connect(lambda: self.app.ui.btn_relay6.setText(self.app.ui.relay6Text.text()))
        self.app.ui.relay7Text.textChanged.connect(lambda: self.app.ui.btn_relay7.setText(self.app.ui.relay7Text.text()))
        self.app.ui.relay8Text.textChanged.connect(lambda: self.app.ui.btn_relay8.setText(self.app.ui.relay8Text.text()))
        self.app.ui.le_relayIP.textChanged.connect(self.setIP)

    def initConfig(self):                                                                                                   # index 0 is first entry etc.
        self.app.ui.relay1Function.addItem('Switch - Toggle')
        self.app.ui.relay1Function.addItem('Pulse 1 sec')
        self.app.ui.relay2Function.addItem('Switch - Toggle')
        self.app.ui.relay2Function.addItem('Pulse 1 sec')
        self.app.ui.relay3Function.addItem('Switch - Toggle')
        self.app.ui.relay3Function.addItem('Pulse 1 sec')
        self.app.ui.relay4Function.addItem('Switch - Toggle')
        self.app.ui.relay4Function.addItem('Pulse 1 sec')
        self.app.ui.relay5Function.addItem('Switch - Toggle')
        self.app.ui.relay5Function.addItem('Pulse 1 sec')
        self.app.ui.relay6Function.addItem('Switch - Toggle')
        self.app.ui.relay6Function.addItem('Pulse 1 sec')
        self.app.ui.relay7Function.addItem('Switch - Toggle')
        self.app.ui.relay7Function.addItem('Pulse 1 sec')
        self.app.ui.relay8Function.addItem('Switch - Toggle')
        self.app.ui.relay8Function.addItem('Pulse 1 sec')
        try:
            if 'Relay1Function' in self.app.config:
                self.app.ui.relay1Function.setCurrentIndex(self.app.config['Relay1Function'])
            if 'Relay2Function' in self.app.config:
                self.app.ui.relay2Function.setCurrentIndex(self.app.config['Relay2Function'])
            if 'Relay3Function' in self.app.config:
                self.app.ui.relay3Function.setCurrentIndex(self.app.config['Relay3Function'])
            if 'Relay4Function' in self.app.config:
                self.app.ui.relay4Function.setCurrentIndex(self.app.config['Relay4Function'])
            if 'Relay5Function' in self.app.config:
                self.app.ui.relay5Function.setCurrentIndex(self.app.config['Relay5Function'])
            if 'Relay6Function' in self.app.config:
                self.app.ui.relay6Function.setCurrentIndex(self.app.config['Relay6Function'])
            if 'Relay7Function' in self.app.config:
                self.app.ui.relay7Function.setCurrentIndex(self.app.config['Relay7Function'])
            if 'Relay8Function' in self.app.config:
                self.app.ui.relay8Function.setCurrentIndex(self.app.config['Relay8Function'])
            if 'Relay1Text' in self.app.config:
                self.app.ui.relay1Text.setText(self.app.config['Relay1Text'])
                self.app.ui.btn_relay1.setText(self.app.config['Relay1Text'])
            if 'Relay2Text' in self.app.config:
                self.app.ui.relay2Text.setText(self.app.config['Relay2Text'])
                self.app.ui.btn_relay2.setText(self.app.config['Relay2Text'])
            if 'Relay3Text' in self.app.config:
                self.app.ui.relay3Text.setText(self.app.config['Relay3Text'])
                self.app.ui.btn_relay3.setText(self.app.config['Relay3Text'])
            if 'Relay4Text' in self.app.config:
                self.app.ui.relay4Text.setText(self.app.config['Relay4Text'])
                self.app.ui.btn_relay4.setText(self.app.config['Relay4Text'])
            if 'Relay5Text' in self.app.config:
                self.app.ui.relay5Text.setText(self.app.config['Relay5Text'])
                self.app.ui.btn_relay5.setText(self.app.config['Relay5Text'])
            if 'Relay6Text' in self.app.config:
                self.app.ui.relay6Text.setText(self.app.config['Relay6Text'])
                self.app.ui.btn_relay6.setText(self.app.config['Relay6Text'])
            if 'Relay7Text' in self.app.config:
                self.app.ui.relay7Text.setText(self.app.config['Relay7Text'])
                self.app.ui.btn_relay7.setText(self.app.config['Relay7Text'])
            if 'Relay8Text' in self.app.config:
                self.app.ui.relay8Text.setText(self.app.config['Relay8Text'])
                self.app.ui.btn_relay8.setText(self.app.config['Relay8Text'])
            if 'RelayIP' in self.app.config:
                self.app.ui.le_relayIP.setText(self.app.config['RelayIP'])
            if 'RelayUsername' in self.app.config:
                self.app.ui.le_relayUsername.setText(self.app.config['RelayUsername'])
            if 'RelayPassword' in self.app.config:
                self.app.ui.le_relayPassword.setText(self.app.config['RelayPassword'])
        except Exception as e:
            self.logger.error('item in config.cfg not be initialize, error:{0}'.format(e))
        finally:
            self.setIP()
            self.connected = self.checkAppStatus()

    def storeConfig(self):
        self.app.config['RelayIP'] = self.relayIP
        self.app.config['Relay1Function'] = self.app.ui.relay1Function.currentIndex()
        self.app.config['Relay2Function'] = self.app.ui.relay2Function.currentIndex()
        self.app.config['Relay3Function'] = self.app.ui.relay3Function.currentIndex()
        self.app.config['Relay4Function'] = self.app.ui.relay4Function.currentIndex()
        self.app.config['Relay5Function'] = self.app.ui.relay5Function.currentIndex()
        self.app.config['Relay6Function'] = self.app.ui.relay6Function.currentIndex()
        self.app.config['Relay7Function'] = self.app.ui.relay7Function.currentIndex()
        self.app.config['Relay8Function'] = self.app.ui.relay8Function.currentIndex()
        self.app.config['Relay1Text'] = self.app.ui.relay1Text.text()
        self.app.config['Relay2Text'] = self.app.ui.relay2Text.text()
        self.app.config['Relay3Text'] = self.app.ui.relay3Text.text()
        self.app.config['Relay4Text'] = self.app.ui.relay4Text.text()
        self.app.config['Relay5Text'] = self.app.ui.relay5Text.text()
        self.app.config['Relay6Text'] = self.app.ui.relay6Text.text()
        self.app.config['Relay7Text'] = self.app.ui.relay7Text.text()
        self.app.config['Relay8Text'] = self.app.ui.relay8Text.text()
        self.app.config['RelayUsername'] = self.app.ui.le_relayUsername.text()
        self.app.config['RelayPassword'] = self.app.ui.le_relayPassword.text()

    def setIP(self):
        valid, value = self.checkIP.checkIP(self.app.ui.le_relayIP)
        if valid:
            self.relayIP = value

    def checkAppStatus(self):
        connected = False
        if self.relayIP:
            try:
                urllib.request.urlopen('http://' + self.relayIP, None, 2)
                self.geturl('http://' + self.relayIP)
                connected = True
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    self.logger.info('relaybox present under ip: {0}'.format(self.relayIP))
                    connected = True
                else:
                    self.logger.error('connection error: {0}'.format(e))
            except urllib.request.URLError:
                self.logger.info('there is no relaybox present under ip: {0}'.format(self.relayIP))
            except Exception as e:
                self.logger.error('connection error: {0}'.format(e))
            finally:
                if connected:
                    self.requestStatus()
                return connected
        else:
            self.logger.info('there is no ip given for relaybox')

    def setStatus(self, response):
        lines = response.splitlines()
        if lines[0] == '<response>':
            self.stat[1] = (lines[2][8] == '1')
            self.stat[2] = (lines[3][8] == '1')
            self.stat[3] = (lines[4][8] == '1')
            self.stat[4] = (lines[5][8] == '1')
            self.stat[5] = (lines[6][8] == '1')
            self.stat[6] = (lines[7][8] == '1')
            self.stat[7] = (lines[8][8] == '1')
            self.stat[8] = (lines[9][8] == '1')
            self.logger.debug('status: {0}'.format(self.stat))
        if self.stat[1]:
            self.app.ui.btn_relay1.setProperty('running', True)
            self.app.ui.btn_relay1.style().unpolish(self.app.ui.btn_relay1)
            self.app.ui.btn_relay1.style().polish(self.app.ui.btn_relay1)
        else:
            self.app.ui.btn_relay1.setProperty('running', False)
            self.app.ui.btn_relay1.style().unpolish(self.app.ui.btn_relay1)
            self.app.ui.btn_relay1.style().polish(self.app.ui.btn_relay1)
        if self.stat[2]:
            self.app.ui.btn_relay2.setProperty('running', True)
            self.app.ui.btn_relay2.style().unpolish(self.app.ui.btn_relay2)
            self.app.ui.btn_relay2.style().polish(self.app.ui.btn_relay2)
        else:
            self.app.ui.btn_relay2.setProperty('running', False)
            self.app.ui.btn_relay2.style().unpolish(self.app.ui.btn_relay2)
            self.app.ui.btn_relay2.style().polish(self.app.ui.btn_relay2)
        if self.stat[3]:
            self.app.ui.btn_relay3.setProperty('running', True)
            self.app.ui.btn_relay3.style().unpolish(self.app.ui.btn_relay3)
            self.app.ui.btn_relay3.style().polish(self.app.ui.btn_relay3)
        else:
            self.app.ui.btn_relay3.setProperty('running', False)
            self.app.ui.btn_relay3.style().unpolish(self.app.ui.btn_relay3)
            self.app.ui.btn_relay3.style().polish(self.app.ui.btn_relay3)
        if self.stat[4]:
            self.app.ui.btn_relay4.setProperty('running', True)
            self.app.ui.btn_relay4.style().unpolish(self.app.ui.btn_relay4)
            self.app.ui.btn_relay4.style().polish(self.app.ui.btn_relay4)
        else:
            self.app.ui.btn_relay4.setProperty('running', False)
            self.app.ui.btn_relay4.style().unpolish(self.app.ui.btn_relay4)
            self.app.ui.btn_relay4.style().polish(self.app.ui.btn_relay4)
        if self.stat[5]:
            self.app.ui.btn_relay5.setProperty('running', True)
            self.app.ui.btn_relay5.style().unpolish(self.app.ui.btn_relay5)
            self.app.ui.btn_relay5.style().polish(self.app.ui.btn_relay5)
        else:
            self.app.ui.btn_relay5.setProperty('running', False)
            self.app.ui.btn_relay5.style().unpolish(self.app.ui.btn_relay5)
            self.app.ui.btn_relay5.style().polish(self.app.ui.btn_relay5)
        if self.stat[6]:
            self.app.ui.btn_relay6.setProperty('running', True)
            self.app.ui.btn_relay6.style().unpolish(self.app.ui.btn_relay6)
            self.app.ui.btn_relay6.style().polish(self.app.ui.btn_relay6)
        else:
            self.app.ui.btn_relay6.setProperty('running', False)
            self.app.ui.btn_relay6.style().unpolish(self.app.ui.btn_relay6)
            self.app.ui.btn_relay6.style().polish(self.app.ui.btn_relay6)
        if self.stat[7]:
            self.app.ui.btn_relay7.setProperty('running', True)
            self.app.ui.btn_relay7.style().unpolish(self.app.ui.btn_relay7)
            self.app.ui.btn_relay7.style().polish(self.app.ui.btn_relay7)
        else:
            self.app.ui.btn_relay7.setProperty('running', False)
            self.app.ui.btn_relay7.style().unpolish(self.app.ui.btn_relay7)
            self.app.ui.btn_relay7.style().polish(self.app.ui.btn_relay7)
        if self.stat[8]:
            self.app.ui.btn_relay8.setProperty('running', True)
            self.app.ui.btn_relay8.style().unpolish(self.app.ui.btn_relay8)
            self.app.ui.btn_relay8.style().polish(self.app.ui.btn_relay8)
        else:
            self.app.ui.btn_relay8.setProperty('running', False)
            self.app.ui.btn_relay8.style().unpolish(self.app.ui.btn_relay8)
            self.app.ui.btn_relay8.style().polish(self.app.ui.btn_relay8)

    def runRelay(self, relayNumber):
        if relayNumber == 1:
            if self.app.ui.relay1Function.currentIndex() == 0:
                print('switch')
                self.switch(relayNumber)
            else:
                print('pulse')
                self.pulse(relayNumber)
        if relayNumber == 2:
            if self.app.ui.relay2Function.currentIndex() == 0:
                self.switch(relayNumber)
            else:
                self.pulse(relayNumber)
        if relayNumber == 3:
            if self.app.ui.relay3Function.currentIndex() == 0:
                self.switch(relayNumber)
            else:
                self.pulse(relayNumber)
        if relayNumber == 4:
            if self.app.ui.relay4Function.currentIndex() == 0:
                self.switch(relayNumber)
            else:
                self.pulse(relayNumber)
        if relayNumber == 5:
            if self.app.ui.relay5Function.currentIndex() == 0:
                self.switch(relayNumber)
            else:
                self.pulse(relayNumber)
        if relayNumber == 6:
            if self.app.ui.relay6Function.currentIndex() == 0:
                self.switch(relayNumber)
            else:
                self.pulse(relayNumber)
        if relayNumber == 7:
            if self.app.ui.relay7Function.currentIndex() == 0:
                self.switch(relayNumber)
            else:
                self.pulse(relayNumber)
        if relayNumber == 8:
            if self.app.ui.relay8Function.currentIndex() == 0:
                self.switch(relayNumber)
            else:
                self.pulse(relayNumber)

    def geturl(self, url):
        result = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.app.ui.le_relayUsername.text(), self.app.ui.le_relayPassword.text()))
        return result

    def pulse(self, relayNumber):
        try:
            self.geturl('http://' + self.relayIP + '/FF0{0:1d}01'.format(relayNumber))
            time.sleep(1)
            self.geturl('http://' + self.relayIP + '/FF0{0:1d}00'.format(relayNumber))
            self.requestStatus()
        except Exception as e:
            self.logger.error('relay:{0}, error:{1}'.format(relayNumber, e))
        finally:
            pass

    def switch(self, relayNumber):
        try:
            self.geturl('http://' + self.relayIP + '/relays.cgi?relay={0:1d}'.format(relayNumber))
            self.requestStatus()
        except Exception as e:
            self.logger.error('relay:{0}, error:{1}'.format(relayNumber, e))
        finally:
            pass

    def requestStatus(self):
        try:
            result = self.geturl('http://' + self.relayIP + '/status.xml')
            self.setStatus(result.content.decode())
        except Exception as e:
            self.logger.error('error {0}'.format(e))
        finally:
            pass

    def switchAllOff(self):
        try:
            self.geturl('http://' + self.relayIP + '/FFE000')
            self.requestStatus()
        except Exception as e:
            self.logger.error('error {0}'.format(e))
        finally:
            pass
