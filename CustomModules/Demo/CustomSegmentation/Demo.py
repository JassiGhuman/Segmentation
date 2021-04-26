import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import loadNodeFromFile, loadNodesFromFile
from slicer.util import VTKObservationMixin
from slicer.util import arrayFromVolume
import ScreenCapture

#
# Demo
#

class Demo(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Demo"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#Demo">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

    # Additional initialization step after application startup is complete
    slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#

def registerSampleData():
  """
  Add data sets to Sample Data module.
  """
  # It is always recommended to provide sample data for users to make it easy to try the module,
  # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  import SampleData
  iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # it is recommended to store data sets that are larger than a few MB in a Github release.

  # Demo1
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='Demo',
    sampleName='Demo1',
    # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
    # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
    thumbnailFileName=os.path.join(iconsPath, 'Demo1.png'),
    # Download URL and target file name
    uris="https://github.com/Samarth2028/Test/blob/a23d3d836d6eda239576ca1308e0dc42fe217d7a/ID00007637202177411956430_heart.nrrd",
    fileNames='Demo1.nrrd',
    # Checksum to ensure file integrity. Can be computed by this command:
    #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    checksums = 'SHA256:56DC4FC8C5A0FA40A7F5373951F2772D16791A73EE44B84F9FFDD6DEB3CAFDFF',
    # This node name will be used when the data set is loaded
    nodeNames='Demo1'
  )

  # Demo2
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='Demo',
    sampleName='Demo2',
    thumbnailFileName=os.path.join(iconsPath, 'Demo2.png'),
    # Download URL and target file name
    uris="https://github.com/Samarth2028/Test/blob/a23d3d836d6eda239576ca1308e0dc42fe217d7a/ID00007637202177411956430_heart.nrrd",
    fileNames='Demo2.nrrd',
    checksums = 'SHA256:56DC4FC8C5A0FA40A7F5373951F2772D16791A73EE44B84F9FFDD6DEB3CAFDFF',
    # This node name will be used when the data set is loaded
    nodeNames='Demo2'
  )

#
# DemoWidget
#

class DemoWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  
  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False
    self.filename = './Resources/volume-2.nrrd';
    self.filetype = 'nrrd File';

    #***********************************
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup2()
      self.parent.show()
    #***********************************
#********************************************%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%***************************************************************

  def onSavePngButton(self):
    print("Inside onSavePngButton method");
    selectedOption = self.ui.pngComboBox.currentText
    print(selectedOption);
    if selectedOption == 'Capture 3D view as PNG with transparent background':
      renderWindow = slicer.app.layoutManager().threeDWidget(0).threeDView().renderWindow()
      renderWindow.SetAlphaBitPlanes(1)
      wti = vtk.vtkWindowToImageFilter()
      wti.SetInputBufferTypeToRGBA()
      wti.SetInput(renderWindow)
      writer = vtk.vtkPNGWriter()
      writer.SetFileName("saved3dview.png")
      writer.SetInputConnection(wti.GetOutputPort())
      writer.Write()
      print("3dsceneShot saved");
    elif selectedOption == "Capture all views as PNG":
      cap = ScreenCapture.ScreenCaptureLogic()
      cap.showViewControllers(False)
      cap.captureImageFromView(None, "allViewsShot.png")
      cap.showViewControllers(True)
      print("allViewsShot saved");
    elif selectedOption == "Capture full slicer Window":
      img = qt.QPixmap.grabWidget(slicer.util.mainWindow()).toImage()
      img.save("mainWindowShot.png")
      print("mainWindow saved");
    else:
      print("Select a valid Option");

  def onFetchButton(self):
    print('Fetch Button Pressed...............')
    #Clear the scene
    slicer.mrmlScene.Clear()
    #filename= r"C:\Users\jaski\Downloads\3dSlicer\Segmentation.seg.nrrd"
    #print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    
    import SampleData
    iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

    # CustomSegmentation1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='CustomSegmentation',
    sampleName='CustomSegmentation3',
    thumbnailFileName=os.path.join(iconsPath, 'CustomSegmentation3.png'),
    
    #uris=r"C:\Users\jaski\Downloads\3dSlicer",
    #uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
    uris="https://github.com/JassiGhuman/Segmentation/releases/download/SHA256/14b49c992e11d07d4e70873be53b45521be3ec0e857f83bec74a9c9598a77d8a",
    #uris="https://github.com/JassiGhuman/Segmentation/releases/download/SHA256/034cd56a0a16700f95c593561bdad23cfb69e3b6c7f562816f5f2bf654e8af9f"
    #uris="https://github.com/JassiGhuman/Segmentation/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
    fileNames='CustomSegmentation3.nrrd',
    #fileNames='Segmentation.seg.nrrd',
    # Checksum to ensure file integrity. Can be computed by this command:
    checksums = 'SHA256:14b49c992e11d07d4e70873be53b45521be3ec0e857f83bec74a9c9598a77d8a',
    #checksum = 'SHA256:034cd56a0a16700f95c593561bdad23cfb69e3b6c7f562816f5f2bf654e8af9f',
    #checksums = 'SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
    # This node name will be used when the data set is loaded
    nodeNames='CustomSegmentation3'
    )
    print('Start Loading data set')
    inputVolume = SampleData.downloadSample('CustomSegmentation3')
    print('Loaded data set')

    #inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    #self.assertEqual(inputScalarRange[0], 0)
    #self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    #logic = CustomSegmentationLogic()

    # Test algorithm with non-inverted threshold
    #logic.process(inputVolume, outputVolume, threshold, True)
    #outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    #self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    #self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    #logic.process(inputVolume, outputVolume, threshold, False)
    #outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    #self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    #self.assertEqual(outputScalarRange[1], inputScalarRange[1])
    #loadNodeFromFile(self,'C:/Users/samar/Desktop/CS/CustomModules/Demo/Resources/volume-2.nrrd','nrrd File');
    print('Fetch Completed')


  def onHistogramButton(self):
    iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')
    import numpy as np
    import SampleData
    # Get a volume from SampleData and compute its histogram
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='CustomSegmentation',
    sampleName='CustomSegmentation3',
    thumbnailFileName=os.path.join(iconsPath, 'CustomSegmentation3.png'),
    uris="https://github.com/JassiGhuman/Segmentation/releases/download/SHA256/14b49c992e11d07d4e70873be53b45521be3ec0e857f83bec74a9c9598a77d8a",
    fileNames='CustomSegmentation3.nrrd',
    checksums = 'SHA256:14b49c992e11d07d4e70873be53b45521be3ec0e857f83bec74a9c9598a77d8a',
    # This node name will be used when the data set is loaded
    nodeNames='CustomSegmentation3'
    )
    inputVolume = SampleData.downloadSample('CustomSegmentation3')

    #volumeNode = SampleData.SampleDataLogic().downloadMRHead()
    histogram = np.histogram(arrayFromVolume(inputVolume), bins=50)

    chartNode = slicer.util.plot(histogram, xColumnIndex = 1)
    chartNode.SetYAxisRangeAuto(False)
    chartNode.SetYAxisRange(0, 4e5)



  def onFetchButton2(self):
    loadedVolumeNode = slicer.util.loadVolume('C:/Users/samar/Desktop/CS/CustomModules/Demo/Resource/volume-2.nrrd')

  def onSaveScene(self,filename, properties={}):
    from slicer import app
    filetype = 'SceneFile'
    properties['fileName'] = filename
    return app.coreIOManager().saveNodes(filetype, properties)


  def loadNRRDFromFile(self, filename, filetype, properties={}, returnNode=False):

    from slicer import app
    from vtk import vtkCollection

    #types1 = [type(k) for k in properties.keys()];
    #types2 = [type(k) for k in properties.values()];
    #print(types1);
    #print(types2)
    #print(properties['fileName'])
    properties['fileName'] = filename;
    #properties.update(fileName = filename)

    loadedNodesCollection = vtkCollection()
    success = app.coreIOManager().loadNodes(filetype, properties, loadedNodesCollection)
    loadedNode = loadedNodesCollection.GetItemAsObject(0) if loadedNodesCollection.GetNumberOfItems() > 0 else None

    if returnNode:
      import logging
      logging.warning("loadNodeFromFile `returnNode` argument is deprecated. Loaded node is now returned directly if `returnNode` is not specified.")
      return success, loadedNode

    if not success:
      errorMessage = "Failed to load node from file: " + str(filename)
      raise RuntimeError(errorMessage)

    return loadedNode;


#**********************************************************
  def loadNrdFromFile(self, filename, filetype, properties={}, returnNode=False):
    """Load nodes into the scene from a file.
    It differs from `loadNodeFromFile` in that it returns loaded node(s) in an iterator.
    :param filename: full path of the file to load.
    :param filetype: specifies the file type, which determines which IO class will load the file.
    :param properties: map containing additional parameters for the loading.
    :return: loaded node(s) in an iterator object.
    :raises RuntimeError: in case of failure
    """
    from slicer import app
    from vtk import vtkCollection
    properties['fileName'] = filename

    loadedNodesCollection = vtkCollection()
    success = app.coreIOManager().loadNodes(filetype, properties, loadedNodesCollection)
    if not success:
      errorMessage = "Failed to load nodes from file: " + str(filename)
      raise RuntimeError(errorMessage)

    return iter(loadedNodesCollection)

#**********************************************************

      

#****************************%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*****************************************************
  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/Demo.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = DemoLogic()

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    self.ui.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.imageThresholdSliderWidget.connect("valueChanged(double)", self.updateParameterNodeFromGUI)
    self.ui.invertOutputCheckBox.connect("toggled(bool)", self.updateParameterNodeFromGUI)
    self.ui.invertedOutputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)

    # Buttons
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.ui.fetchButton.connect('clicked(bool)', self.onFetchButton)
    self.ui.histogramButton.connect('clicked(bool)', self.onHistogramButton)
    self.ui.saveMrbButton.connect('clicked(bool)', self.onSaveScene('saved_mrb_scene.mrb'));
    self.ui.saveMrmlButton.connect('clicked(bool)', self.onSaveScene('saved_mrml_scene.mrml'));
    self.ui.savePngButton.connect('clicked(bool)',self.onSavePngButton);
    #self.ui.fetchButton.connect('clicked(bool)', self.loadNRRDFromFile('./Resources/volume-2.nrrd','nrrd File'))
    #self.ui.fetchButton.connect('clicked(bool)', self.loadNrdFromFile('C:/Users/samar/Desktop/CS/CustomModules/Demo/Resources/volume-2.nrrd','nrrd File'))
    # Make sure parameter node is initialized (needed for module reload)
    self.initializeParameterNode()

  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())

    # Select default input nodes if nothing is selected yet to save a few clicks for the user
    if not self._parameterNode.GetNodeReference("InputVolume"):
      firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
      if firstVolumeNode:
        self._parameterNode.SetNodeReferenceID("InputVolume", firstVolumeNode.GetID())

  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True

    # Update node selectors and sliders
    self.ui.inputSelector.setCurrentNode(self._parameterNode.GetNodeReference("InputVolume"))
    self.ui.outputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume"))
    self.ui.invertedOutputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolumeInverse"))
    self.ui.imageThresholdSliderWidget.value = float(self._parameterNode.GetParameter("Threshold"))
    self.ui.invertOutputCheckBox.checked = (self._parameterNode.GetParameter("Invert") == "true")

    # Update buttons states and tooltips
    if self._parameterNode.GetNodeReference("InputVolume") and self._parameterNode.GetNodeReference("OutputVolume"):
      self.ui.applyButton.toolTip = "Compute output volume"
      self.ui.applyButton.enabled = True
    else:
      self.ui.applyButton.toolTip = "Select input and output volume nodes"
      self.ui.applyButton.enabled = False

    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

    self._parameterNode.SetNodeReferenceID("InputVolume", self.ui.inputSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID("OutputVolume", self.ui.outputSelector.currentNodeID)
    self._parameterNode.SetParameter("Threshold", str(self.ui.imageThresholdSliderWidget.value))
    self._parameterNode.SetParameter("Invert", "true" if self.ui.invertOutputCheckBox.checked else "false")
    self._parameterNode.SetNodeReferenceID("OutputVolumeInverse", self.ui.invertedOutputSelector.currentNodeID)

    self._parameterNode.EndModify(wasModified)

  def onApplyButton(self):
    """
    Run processing when user clicks "Apply" button.
    """
    try:

      # Compute output
      self.logic.process(self.ui.inputSelector.currentNode(), self.ui.outputSelector.currentNode(),
        self.ui.imageThresholdSliderWidget.value, self.ui.invertOutputCheckBox.checked)

      # Compute inverted output (if needed)
      if self.ui.invertedOutputSelector.currentNode():
        # If additional output volume is selected then result with inverted threshold is written there
        self.logic.process(self.ui.inputSelector.currentNode(), self.ui.invertedOutputSelector.currentNode(),
          self.ui.imageThresholdSliderWidget.value, not self.ui.invertOutputCheckBox.checked, showResult=False)

    except Exception as e:
      slicer.util.errorDisplay("Failed to compute results: "+str(e))
      import traceback
      traceback.print_exc()
    




#
# DemoLogic
#

class DemoLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("Threshold"):
      parameterNode.SetParameter("Threshold", "100.0")
    if not parameterNode.GetParameter("Invert"):
      parameterNode.SetParameter("Invert", "false")

  def process(self, inputVolume, outputVolume, imageThreshold, invert=False, showResult=True):
    """
    Run the processing algorithm.
    Can be used without GUI widget.
    :param inputVolume: volume to be thresholded
    :param outputVolume: thresholding result
    :param imageThreshold: values above/below this threshold will be set to 0
    :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
    :param showResult: show output volume in slice viewers
    """

    if not inputVolume or not outputVolume:
      raise ValueError("Input or output volume is invalid")

    import time
    startTime = time.time()
    logging.info('Processing started')

    # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
    cliParams = {
      'InputVolume': inputVolume.GetID(),
      'OutputVolume': outputVolume.GetID(),
      'ThresholdValue' : imageThreshold,
      'ThresholdType' : 'Above' if invert else 'Below'
      }
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
    # We don't need the CLI module node anymore, remove it to not clutter the scene with it
    slicer.mrmlScene.RemoveNode(cliNode)

    stopTime = time.time()
    logging.info('Processing completed in {0:.2f} seconds'.format(stopTime-startTime))

#
# DemoTest
#

class DemoTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_Demo1()

  def test_Demo1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    registerSampleData()
    inputVolume = SampleData.downloadSample('Demo1')
    self.delayDisplay('Loaded test data set')

    inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    self.assertEqual(inputScalarRange[0], 0)
    self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    logic = DemoLogic()

    # Test algorithm with non-inverted threshold
    logic.process(inputVolume, outputVolume, threshold, True)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    logic.process(inputVolume, outputVolume, threshold, False)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], inputScalarRange[1])

    self.delayDisplay('Test passed')