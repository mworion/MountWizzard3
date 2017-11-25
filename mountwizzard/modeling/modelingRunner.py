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
import PyQt5
# modeling runner get most of is basic parts from ModelingBase
from modeling.modelingBase import ModelingBase


class ModelingRunner(ModelingBase):

    def __init__(self, app):
        super().__init__(app)
        # make main sources available
        self.app = app
        self.initConfig()

    def runBaseModel(self):
        if not self.checkModelingAvailable():
            return
        if self.app.ui.checkClearModelFirst.isChecked():
            self.app.modelLogQueue.put('Clearing alignment modeling - taking 4 seconds.\n')
            self.clearAlignmentModel()
            self.app.modelLogQueue.put('Model cleared!\n')
        settlingTime, directory = self.setupRunningParameters()
        if len(self.modelPoints.BasePoints) > 0:
            simulation = self.app.ui.checkSimulation.isChecked()
            keepImages = self.app.ui.checkKeepImages.isChecked()
            modelData = self.imagingApps.prepareImaging(directory)
            self.modelData = self.runModel('Base', self.modelPoints.BasePoints, modelData, settlingTime, simulation, keepImages)
            self.modelData = self.app.mount.retrofitMountData(self.modelData)
            name = directory + '_base.dat'
            if len(self.modelData) > 0:
                self.app.ui.le_analyseFileName.setText(name)
                self.analyseData.saveData(self.modelData, name)
                self.app.mount.saveBaseModel()
        else:
            self.logger.warning('There are no Basepoints for modeling')

    def runRefinementModel(self):
        if not self.checkModelingAvailable():
            return
        num = self.app.mount.numberModelStars()
        simulation = self.app.ui.checkSimulation.isChecked()
        if num > 2 or simulation:
            settlingTime, directory = self.setupRunningParameters()
            if len(self.modelPoints.RefinementPoints) > 0:
                if self.app.ui.checkKeepRefinement.isChecked():
                    self.app.mount.loadRefinementModel()
                else:
                    self.app.mount.loadBaseModel()
                keepImages = self.app.ui.checkKeepImages.isChecked()
                modelData = self.imagingApps.prepareImaging(directory)
                refinePoints = self.runModel('Refinement', self.modelPoints.RefinementPoints, modelData, settlingTime, simulation, keepImages)
                for i in range(0, len(refinePoints)):
                    refinePoints[i]['Index'] += len(self.modelData)
                self.modelData = self.modelData + refinePoints
                self.modelData = self.app.mount.retrofitMountData(self.modelData)
                name = directory + '_refinement.dat'
                if len(self.modelData) > 0:
                    self.app.ui.le_analyseFileName.setText(name)
                    self.analyseData.saveData(self.modelData, name)
                    self.app.mount.saveRefinementModel()
            else:
                self.logger.warning('There are no Refinement Points to modeling')
        else:
            self.app.messageQueue.put('Refine stopped, no BASE model available !\n')

    def runCheckModel(self):
        if not self.checkModelingAvailable():
            return
        settlingTime, directory = self.setupRunningParameters()
        points = self.modelPoints.BasePoints + self.modelPoints.RefinementPoints
        if len(points) > 0:
            simulation = self.app.ui.checkSimulation.isChecked()
            keepImages = self.app.ui.checkKeepImages.isChecked()
            modelData = self.imagingApps.prepareImaging(directory)
            self.modelingResultData = self.runModel('Check', points, modelData, settlingTime, simulation, keepImages)
            name = directory + '_check.dat'
            if len(self.modelingResultData) > 0:
                self.app.ui.le_analyseFileName.setText(name)
                self.analyseData.saveData(self.modelingResultData, name)
        else:
            self.logger.warning('There are no Refinement or Base Points to modeling')

    def runAllModel(self):
        self.runBaseModel()
        self.runRefinementModel()

    def runTimeChangeModel(self):
        if not self.checkModelingAvailable():
            return
        settlingTime, directory = self.setupRunningParameters()
        points = []
        for i in range(0, int(float(self.app.ui.numberRunsTimeChange.value()))):
            points.append((int(self.app.ui.azimuthTimeChange.value()), int(self.app.ui.altitudeTimeChange.value()),
                           PyQt5.QtWidgets.QGraphicsTextItem(''), True))
        simulation = self.app.ui.checkSimulation.isChecked()
        keepImages = self.app.ui.checkKeepImages.isChecked()
        modelData = self.imagingApps.prepareImaging(directory)
        self.modelingResultData = self.runModel('TimeChange', points, modelData, settlingTime, simulation, keepImages)
        name = directory + '_timechange.dat'
        if len(self.modelingResultData) > 0:
            self.app.ui.le_analyseFileName.setText(name)
            self.analyseData.saveData(self.modelingResultData, name)

    def runHystereseModel(self):
        if not self.checkModelingAvailable():
            return
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
        modelData = self.imagingApps.prepareImaging(directory)
        self.modelingResultData = self.runModel('Hysterese', points, modelData, waitingTime, simulation, keepImages)
        name = directory + '_hysterese.dat'
        self.app.ui.le_analyseFileName.setText(name)
        if len(self.modelingResultData) > 0:
            self.app.ui.le_analyseFileName.setText(name)
            self.analyseData.saveData(self.modelingResultData, name)

    def runBatchModel(self):
        nameDataFile = self.app.ui.le_analyseFileName.text()
        self.logger.info('modeling from {0}'.format(nameDataFile))
        data = self.app.workerModeling.analyse.loadData(nameDataFile)
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
        self.app.mount.programBatchData(data)

    def runBoostModel(self):
        if not self.checkModelingAvailable():
            return
        if not self.app.ui.pd_chooseImagingApp.currentText().startswith('SGPro'):
            return
        settlingTime, directory = self.setupRunningParameters()
        if len(self.app.workerModeling.modelPoints.RefinementPoints) > 0:
            simulation = self.app.ui.checkSimulation.isChecked()
            keepImages = self.app.ui.checkKeepImages.isChecked()
            modelData = self.app.workerModeling.imagingApps.prepareImaging(directory)
            self.app.modeling.modelData = self.runBoost(self.app.workerModeling.modelPoints.RefinementPoints, modelData, settlingTime, simulation, keepImages)
            self.app.modeling.modelData = self.app.mount.retrofitMountData(self.app.modeling.modelData)
            name = directory + '_boost.dat'
            if len(self.app.modeling.modelData) > 0:
                self.app.ui.le_analyseFileName.setText(name)
                self.app.workerModeling.analyse.saveData(self.app.modeling.modelData, name)
                self.app.mount.saveRefinementModel()
                # if not self.app.workerModeling.cancel:
                self.app.mount.programBatchData(self.modelData)
        else:
            self.logger.warning('There are no Refinement Points to modeling')