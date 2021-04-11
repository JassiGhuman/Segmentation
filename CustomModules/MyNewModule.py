# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:39:59 2021

@author: isand
"""

from __main__ import vtk, qt, ctk, slicer

#
# HelloPython
#

class MyNewModule:
  def __init__(self, parent):
    parent.title = "PythonModule"
    parent.categories = ["New Categories"]
    parent.dependencies = []
    parent.contributors = ["Jaskirat"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    Example of scripted loadable extension for the HelloPython tutorial.
    """
    parent.acknowledgementText = "" # replace with organization, grant and thanks.
    self.parent = parent

#
# qHelloPythonWidget
#

class MyNewModuleWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    # Collapsible button
    sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    sampleCollapsibleButton.text = "A collapsible button"
    self.layout.addWidget(sampleCollapsibleButton)

    # Layout within the sample collapsible button
    self.sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)
    #volume selector
    self.formFrame = qt.QFrame(sampleCollapsibleButton)
    #set the layout to horizontal
    self.formFrame.setLayout(qt.QHBoxLayout())
    #add it to the layout
    self.sampleFormLayout.addWidget(self.formFrame)
    
    #create new volume selector
    self.inputSelector = qt.QLabel("input label: ", self.formFrame)
    self.formFrame.layout().addWidget(self.inputSelector)
    
    self.inputSelector = slicer.qMRMLNodeComboBox(self.formFrame)
    #self.inputSelector.nodeTypes = (("vtkMRMLScalarVolumeNode"),"")
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    self.formFrame.layout().addWidget(self.inputSelector)
    
    #a button
    button = qt.QPushButton("Create a Plane")
    #button.toolTip = "Displays the path of the selected volume"
    #button.connect("clicked(bool)",self.setInformationButtonClicled)
    button.connect("clicked(bool)",self.setCreatePlaneButtonClicked)
    self.formFrame.layout().addWidget(button)
    
    #textfiled
    self.textfiled = qt.QTextEdit()
    self.textfiled.setReadOnly(True)
    self.formFrame.layout().addWidget(self.textfiled)
    
    self.layout.addStretch(1)
    

  # def setInformationButtonClicled(self):
  #      n = slicer.util.getNode(self.inputSelector.currentNode().GetName())
  #      nSN = n.GetStorageNode()
  #      path = nSN.GetFileName()
  #      self.textfiled.insertPlainText(path)
  def setCreatePlaneButtonClicked(self):
       inputVolume = self.inputSelector.currentNode()
       # reader = vtk.vtkSTLReader()
       # plane = vtk.vtkPlane()
       # plane.SetOrigin(inputVolume.GetOutput().GetCenter())
       #plane.SetNormal(1, 0, 1)
       planex = vtk.vtkPlane()
       planex.SetOrigin(inputVolume.GetOutput().GetCenter())#the pPlane[0] is a point in the plane A
       planex.SetNormal(1,0,1)#the anVector is the normal of the plane A
    
       planexSample = vtk.vtkSampleFunction()
       planexSample.SetImplicitFunction(planex)
       planexSample.SetModelBounds(-100,100,-100,100,-100,100)
       planexSample.SetSampleDimensions(100,100,100)
       planexSample.ComputeNormalsOff()
       plane1 = vtk.vtkContourFilter()
       plane1.SetInput(planexSample.GetOutput())
        
        
        # Create model Plane A node
       planeA = slicer.vtkMRMLModelNode()
       planeA.SetScene(slicer.mrmlScene)
       planeA.SetName("PlaneA")
       planeA.SetAndObservePolyData(plane1.GetOutput())
        
        # Create display model Plane A node
       planeAModelDisplay = slicer.vtkMRMLModelDisplayNode()
       planeAModelDisplay.SetColor(1,0,1)
       planeAModelDisplay.SetScene(slicer.mrmlScene)
       slicer.mrmlScene.AddNode(planeAModelDisplay)
       planeA.SetAndObserveDisplayNodeID(planeAModelDisplay.GetID())
        
        #Add to scene
       planeAModelDisplay.SetInputPolyData(plane1.GetOutput())
       slicer.mrmlScene.AddNode(planeA)
    


