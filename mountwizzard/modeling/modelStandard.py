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
import copy
import os
import shutil
import time
import PyQt5
from modeling.modelBase import ModelBase


class ModelStandard(ModelBase):

    def __init__(self, app):
        super(ModelStandard, self).__init__(app)
        # make main sources available
        self.app = app
        self.modelData = None
        self.results = []
        self.modelRun = False

    def runBaseModel(self):
        if self.app.ui.checkClearModelFirst.isChecked():
            self.app.modelLogQueue.put('Clearing alignment modeling - taking 4 seconds.\n')
            self.clearAlignmentModel()
            self.app.modelLogQueue.put('Model cleared!\n')
        settlingTime, directory = self.setupRunningParameters()
        if len(self.app.modeling.modelPoints.BasePoints) > 0:
            simulation = self.app.ui.checkSimulation.isChecked()
            keepImages = self.app.ui.checkKeepImages.isChecked()
            self.modelData = self.runModel('Base', self.app.modeling.modelPoints.BasePoints, directory, settlingTime, simulation, keepImages)
            self.modelData = self.app.mount.retrofitMountData(self.modelData)
            name = directory + '_base.dat'
            if len(self.modelData) > 0:
                self.app.ui.le_analyseFileName.setText(name)
                self.app.modeling.analyse.saveData(self.modelData, name)
                self.app.mount.saveBaseModel()
        else:
            self.logger.warning('There are no Basepoints for modeling')

    def runRefinementModel(self):
        num = self.app.mount.numberModelStars()
        simulation = self.app.ui.checkSimulation.isChecked()
        if num > 2 or simulation:
            settlingTime, directory = self.setupRunningParameters()
            if len(self.app.modeling.modelPoints.RefinementPoints) > 0:
                if self.app.ui.checkKeepRefinement.isChecked():
                    self.app.mount.loadRefinementModel()
                else:
                    self.app.mount.loadBaseModel()
                keepImages = self.app.ui.checkKeepImages.isChecked()
                refinePoints = self.runModel('Refinement', self.app.modeling.modelPoints.RefinementPoints, directory, settlingTime, simulation, keepImages)
                if self.app.ui.checkKeepRefinement.isChecked():
                    for i in range(0, len(refinePoints)):
                        refinePoints[i]['Index'] += len(self.modelData)
                    self.modelData = self.modelData + refinePoints
                else:
                    self.modelData = refinePoints
                self.modelData = self.app.mount.retrofitMountData(self.modelData)
                name = directory + '_refinement.dat'
                if len(self.modelData) > 0:
                    self.app.ui.le_analyseFileName.setText(name)
                    self.app.modeling.analyse.saveData(self.modelData, name)
                    self.app.mount.saveRefinementModel()
            else:
                self.logger.warning('There are no Refinement Points to modeling')
        else:
            self.app.modelLogQueue.put('Refine stopped, no BASE model available !\n')
            self.app.messageQueue.put('Refine stopped, no BASE model available !\n')

    def runCheckModel(self):
        settlingTime, directory = self.setupRunningParameters()
        points = self.app.modeling.modelPoints.BasePoints + self.app.modeling.modelPoints.RefinementPoints
        if len(points) > 0:
            simulation = self.app.ui.checkSimulation.isChecked()
            keepImages = self.app.ui.checkKeepImages.isChecked()
            self.app.modeling.modelAnalyseData = self.runModel('Check', points, directory, settlingTime, simulation, keepImages)
            name = directory + '_check.dat'
            if len(self.app.modeling.modelAnalyseData) > 0:
                self.app.ui.le_analyseFileName.setText(name)
                self.app.modeling.analyse.saveData(self.app.modeling.modelAnalyseData, name)
        else:
            self.logger.warning('There are no Refinement or Base Points to modeling')

    def runAllModel(self):
        self.runBaseModel()
        self.runRefinementModel()

    def runTimeChangeModel(self):
        settlingTime, directory = self.setupRunningParameters()
        points = []
        for i in range(0, int(float(self.app.ui.numberRunsTimeChange.value()))):
            points.append((int(self.app.ui.azimuthTimeChange.value()), int(self.app.ui.altitudeTimeChange.value()),
                           PyQt5.QtWidgets.QGraphicsTextItem(''), True))
        simulation = self.app.ui.checkSimulation.isChecked()
        keepImages = self.app.ui.checkKeepImages.isChecked()
        self.app.modeling.modelAnalyseData = self.runModel('TimeChange', points, directory, settlingTime, simulation, keepImages)
        name = directory + '_timechange.dat'
        if len(self.app.modeling.modelAnalyseData) > 0:
            self.app.ui.le_analyseFileName.setText(name)
            self.app.modeling.analyse.saveData(self.app.modeling.modelAnalyseData, name)

    def runHystereseModel(self):
        waitingTime, directory = self.setupRunningParameters()
        alt1 = int(float(self.app.ui.altitudeHysterese1.value()))
        alt2 = int(float(self.app.ui.altitudeHysterese2.value()))
        az1 = int(float(self.app.ui.azimuthHysterese1.value()))
        az2 = int(float(self.app.ui.azimuthHysterese2.value()))
        numberRunsHysterese = int(float(self.app.ui.numberRunsHysterese.value()))
        points = []
        for i in range(0, numberRunsHysterese):
            points.append((az1, alt1, PyQt5.QtWidgets.QGraphicsTextItem(''), True))
            points.append((az2, alt2, PyQt5.QtWidgets.QGraphicsTextItem(''), False))
        simulation = self.app.ui.checkSimulation.isChecked()
        keepImages = self.app.ui.checkKeepImages.isChecked()
        self.app.modeling.modelAnalyseData = self.runModel('Hysterese', points, directory, waitingTime, simulation, keepImages)
        name = directory + '_hysterese.dat'
        self.app.ui.le_analyseFileName.setText(name)
        if len(self.app.modeling.modelAnalyseData) > 0:
            self.app.ui.le_analyseFileName.setText(name)
            self.app.modeling.analyse.saveData(self.app.modeling.modelAnalyseData, name)

    def runBatchModel(self):
        nameDataFile = self.app.ui.le_analyseFileName.text()
        self.logger.info('modeling from {0}'.format(nameDataFile))
        data = self.app.modeling.analyse.loadData(nameDataFile)
        if not('RaJNow' in data and 'DecJNow' in data):
            self.logger.warning('RaJNow or DecJNow not in data file')
            self.app.modelLogQueue.put('{0} - mount coordinates missing\n'.format(self.timeStamp()))
            return
        if not('RaJNowSolved' in data and 'DecJNowSolved' in data):
            self.logger.warning('RaJNowSolved or DecJNowSolved not in data file')
            self.app.modelLogQueue.put('{0} - solved data missing\n'.format(self.timeStamp()))
            return
        if not('Pierside' in data and 'LocalSiderealTime' in data):
            self.logger.warning('Pierside and LocalSiderealTime not in data file')
            self.app.modelLogQueue.put('{0} - Time and Pierside missing\n'.format(self.timeStamp()))
            return
        self.app.mount.saveBackupModel()
        self.app.modelLogQueue.put('{0} - Start Batch modeling. Saving Actual modeling to BATCH\n'.format(self.timeStamp()))
        self.app.mount.mountHandler.sendCommand('newalig')
        self.app.modelLogQueue.put('{0} - \tOpening Calculation\n'.format(self.timeStamp()))
        for i in range(0, len(data['index'])):
            command = 'newalpt{0},{1},{2},{3},{4},{5}'.format(self.app.modeling.transform.decimalToDegree(data['RaJNow'][i], False, True),
                                                              self.app.modeling.transform.decimalToDegree(data['DecJNow'][i], True, False),
                                                              data['pierside'][i],
                                                              self.app.modeling.transform.decimalToDegree(data['RaJNowSolved'][i], False, True),
                                                              self.app.modeling.transform.decimalToDegree(data['DecJNowSolved'][i], True, False),
                                                              self.app.modeling.ttransform.decimalToDegree(data['LocalSiderealTimeFloat'][i], False, True))
            reply = self.app.mount.mountHandler.sendCommand(command)
            if reply == 'E':
                self.logger.warning('point {0} could not be added'.format(reply))
                self.app.modelLogQueue.put('{0} - \tPoint could not be added\n'.format(self.timeStamp()))
            else:
                self.app.modelLogQueue.put('{0} - \tAdded point {1} @ Az:{2}, Alt:{3} \n'
                                           .format(self.timeStamp(), reply, int(data['Azimuth'][i]), int(data['Altitude'][i])))
        reply = self.app.mount.mountHandler.sendCommand('endalig')
        if reply == 'V':
            self.app.modelLogQueue.put('{0} - Model successful finished! \n'.format(self.timeStamp()))
            self.logger.info('Model successful finished!')
        else:
            self.app.modelLogQueue.put('{0} - Model could not be calculated with current data! \n'.format(self.timeStamp()))
            self.logger.warning('Model could not be calculated with current data!')

    # noinspection PyUnresolvedReferences
    def runModel(self, modeltype, runPoints, directory, settlingTime, simulation=False, keepImages=False):
        # start clearing the data
        modelData = {}
        results = []
        # preparing the gui outputs
        self.app.modelLogQueue.put('status-- of --')
        self.app.modelLogQueue.put('percent0')
        self.app.modelLogQueue.put('timeleft--:--')
        self.app.modelLogQueue.put('delete')
        self.app.modelLogQueue.put('#BW{0} - Start {1} Model\n'.format(self.timeStamp(), modeltype))
        modelData = self.prepareImaging(modelData, directory)
        if not os.path.isdir(modelData['BaseDirImages']):
            os.makedirs(modelData['BaseDirImages'])
        self.logger.info('modelData: {0}'.format(modelData))
        self.app.mountCommandQueue.put('PO')
        self.app.mountCommandQueue.put('AP')
        # counter and timer for performance estimation
        numCheckPoints = 0
        timeStart = time.time()
        # here starts the real model running cycle
        for i, (p_az, p_alt, p_item, p_solve) in enumerate(runPoints):
            self.app.modeling.modelRun = True
            modelData['Azimuth'] = p_az
            modelData['Altitude'] = p_alt
            if p_item.isVisible():
                # todo: put the code to multi thread modeling
                if self.app.modeling.cancel:
                    self.app.modeling.cancel = False
                    self.app.modelLogQueue.put('#BW{0} -\t {1} Model canceled !\n'.format(self.timeStamp(), modeltype))
                    # tracking should be on after canceling the modeling
                    self.app.mountCommandQueue.put('AP')
                    # clearing the gui
                    self.app.modelLogQueue.put('status-- of --')
                    self.app.modelLogQueue.put('percent0')
                    self.app.modelLogQueue.put('timeleft--:--')
                    self.logger.info('Modeling cancelled in main loop')
                    # finally stopping modeling run
                    break
                self.app.modelLogQueue.put('#BG{0} - Slewing to point {1:2d}  @ Az: {2:3.0f}\xb0 Alt: {3:2.0f}\xb0\n'.format(self.timeStamp(), i+1, p_az, p_alt))
                self.logger.info('point {0:2d}  Az: {1:3.0f} Alt: {2:2.0f}'.format(i+1, p_az, p_alt))
                if modeltype in ['TimeChange']:
                    # in time change there is only slew for the first time, than only track during imaging
                    if i == 0:
                        self.slewMountDome(p_az, p_alt)
                        self.app.mountCommandQueue.put('RT9')
                else:
                    self.slewMountDome(p_az, p_alt)
                self.app.modelLogQueue.put('{0} -\t Wait mount settling / delay time:  {1:02d} sec'.format(self.timeStamp(), settlingTime))
                timeCounter = settlingTime
                while timeCounter > 0:
                    time.sleep(1)
                    timeCounter -= 1
                    self.app.modelLogQueue.put('backspace')
                    self.app.modelLogQueue.put('{0:02d} sec'.format(timeCounter))
                self.app.modelLogQueue.put('\n')
            if p_item.isVisible() and p_solve:
                modelData['File'] = self.app.modeling.CAPTUREFILE + '{0:03d}'.format(i) + '.fit'
                modelData['LocalSiderealTime'] = self.app.mount.data['LocalSiderealTime']
                modelData['LocalSiderealTimeFloat'] = self.app.modeling.transform.degStringToDecimal(self.app.mount.data['LocalSiderealTime'][0:9])
                modelData['RaJ2000'] = self.app.mount.data['RaJ2000']
                modelData['DecJ2000'] = self.app.mount.data['DecJ2000']
                modelData['RaJNow'] = self.app.mount.data['RaJNow']
                modelData['DecJNow'] = self.app.mount.data['DecJNow']
                modelData['Pierside'] = self.app.mount.data['Pierside']
                modelData['Index'] = i
                modelData['RefractionTemperature'] = self.app.mount.data['RefractionTemperature']
                modelData['RefractionPressure'] = self.app.mount.data['RefractionPressure']
                if modeltype in ['TimeChange']:
                    self.app.mountCommandQueue.put('AP')
                self.app.modelLogQueue.put('{0} -\t Capturing image for modeling point {1:2d}\n'.format(self.timeStamp(), i + 1))
                suc, mes, imagepath = self.capturingImage(modelData, simulation)
                if modeltype in ['TimeChange']:
                    self.app.mountCommandQueue.put('RT9')
                self.logger.info('suc:{0} mes:{1}'.format(suc, mes))
                if suc:
                    self.app.modelLogQueue.put('{0} -\t Solving Image\n'.format(self.timeStamp()))
                    suc, mes, modelData = self.solveImage(modelData, simulation)
                    self.app.modelLogQueue.put('{0} -\t Image path: {1}\n'.format(self.timeStamp(), modelData['ImagePath']))
                    if suc:
                        if modeltype in ['Base', 'Refinement', 'All']:
                            suc = self.addRefinementStar(modelData['RaJNowSolved'], modelData['DecJNowSolved'])
                            if suc:
                                self.app.modelLogQueue.put('{0} -\t Point added\n'.format(self.timeStamp()))
                                numCheckPoints += 1
                                results.append(copy.copy(modelData))
                                p_item.setVisible(False)
                            else:
                                self.app.modelLogQueue.put('{0} -\t Point could not be added - please check!\n'.format(self.timeStamp()))
                                self.logger.info('raE:{0} decE:{1} star could not be added'.format(modelData['RaError'], modelData['DecError']))
                        self.app.modelLogQueue.put('{0} -\t RA_diff:  {1:2.1f}    DEC_diff: {2:2.1f}\n'.format(self.timeStamp(), modelData['RaError'], modelData['DecError']))
                        self.logger.info('modelData: {0}'.format(modelData))
                    else:
                        self.app.modelLogQueue.put('{0} -\t Solving error: {1}\n'.format(self.timeStamp(), mes))
                self.app.modelLogQueue.put('status{0} of {1}'.format(i+1, len(runPoints)))
                modelBuildDone = (i + 1) / len(runPoints)
                self.app.modelLogQueue.put('percent{0}'.format(modelBuildDone))
                actualTime = time.time() - timeStart
                timeCalculated = actualTime / (i + 1) * (len(runPoints) - i - 1)
                mm = int(timeCalculated / 60)
                ss = int(timeCalculated - 60 * mm)
                self.app.modelLogQueue.put('timeleft{0:02d}:{1:02d}'.format(mm, ss))
        if not keepImages:
            shutil.rmtree(modelData['BaseDirImages'], ignore_errors=True)
        self.app.modelLogQueue.put('#BW{0} - {1} Model run finished. Number of modeled points: {2:3d}\n\n'.format(self.timeStamp(), modeltype, numCheckPoints))
        self.app.modeling.modelRun = False
        return results
