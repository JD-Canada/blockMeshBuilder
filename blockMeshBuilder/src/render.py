import vtk 
import numpy as np
import random

from blockMeshBuilder.src.userInteraction import UserInteraction

class Render():
    
    def __init__(self,domain):
        # A renderer and render window
        
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.parent = self.interactor
        
        self.domain=domain
        
        self.blocks=domain.blocks
        self.points=domain.points
        self.toRemove=[]
        self.deletedActors=[]
        
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.2, 0.4, 0.6 )
        self.pointRadius=0.001
        # self.pointRadius=min(0.01*abs(self.domain.x_axis[-1]-self.domain.x_axis[0]),
                             # 0.01*abs(self.domain.y_axis[-1]-self.domain.y_axis[0]),
                             # 0.01*abs(self.domain.z_axis[-1]-self.domain.z_axis[0]))
        
        self.renwin = vtk.vtkRenderWindow()
        
        self.renwin.AddRenderer(self.renderer)
        self.renwin.SetSize(500, 500)
        
        # An interactor
        self.interactor.SetRenderWindow(self.renwin)
        
        # add the custom style
        self.style = UserInteraction(self)
        self.style.SetDefaultRenderer(self.renderer)
        self.interactor.SetInteractorStyle(self.style)

        self.mode = 0 #default to block & point edit mode
        self.print_main_header()

    def print_main_header(self):
        print('\n')
        print('       ****** blockMeshBuilder version 0.0.1 *******')
        print('                       _________ ')
        print('                      |\         \\ ')
        print('                      | \         \\')
        print('                      |  \_________\\')
        print('              ________|  |         |_______')
        print('            |\         \ |         |       \\')
        print('            | \         \|         |        \\')
        print('            |  \ ________|_________|_________\\')
        print('            |   |        |\         \        |')
        print('             \  |        | \         \       |')
        print('              \ |        |  \ ________\      |')
        print('               \|________|   |        |______|') 
        print('                          \  |        |') 
        print('                           \ |        |')
        print('                            \|________|')
        print('                     Jason Duguay May, 2019')
        print('\n')
        print('You are in Block & Point edit mode where you can select and delete')
        print('any unwanted blocks by pressing "d". Select items with a right click.')
        print('Delete blocks first, then isolated points, then press "f" to switch') 
        print('to Boundary mode where you can select multiple block faces and assign') 
        print('them to a boundary patch by pressing "n" and following the instructions')
        print('in the terminal. Get back to Block & Point edit by pressing "b".')
        print('\n')

    def add_blocks(self):
        
        for key,block in self.blocks.items():
            
            cube = vtk.vtkCubeSource()
            cube.SetXLength(block.blocksDimensions[0])
            cube.SetYLength(block.blocksDimensions[1])
            cube.SetZLength(block.blocksDimensions[2])
        
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(cube.GetOutputPort())
        
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            # random_color=random.randint(30,70)/100.0
            actor.GetProperty().SetColor(0.4, 0.4, 0.4)
            actor.SetPosition(block.blocksCentroid[0], block.blocksCentroid[1],block.blocksCentroid[2])
            actor.key = key
            
            self.balloonWidget.AddBalloon(actor, "Block %s" %block.blockID)
           

            try:
                if actor.key in self.toRemove:
                    continue
                else:
                    self.renderer.AddActor(actor)
            except NameError:
                self.renderer.AddActor(actor)
                continue
        
    def add_points(self):
        
        count=0

        for key, point in self.points.items():

            source = vtk.vtkSphereSource()
            
            x = point[0]
            y = point[1]
            z = point[2]
            
            source.SetRadius(self.pointRadius)
            source.SetCenter(x, y, z)
            source.SetPhiResolution(11)
            source.SetThetaResolution(21)
            
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(source.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.key = key

            self.balloonWidget.AddBalloon(actor, "Vertex %s" %self.domain.pointID[count])

            r = 66.0/255.0
            g = 75.0/255.0
            b = 244.0/255.0
            actor.GetProperty().SetDiffuseColor(r, g, b)
            actor.GetProperty().SetDiffuse(.8)
            actor.GetProperty().SetSpecular(.5)
            actor.GetProperty().SetSpecularColor(1.0,1.0,1.0)
            actor.GetProperty().SetSpecularPower(30.0)
            count=count+1
            try:
                
                if actor.key in self.toRemove:
                    continue
                else:
                    self.renderer.AddActor(actor)
            except NameError:
                self.renderer.AddActor(actor)
                continue
        
    def add_block_centroids(self):
        
        # Add block centroids
        for key,block in self.blocks.items():
            source = vtk.vtkSphereSource()
        
            # random position and radius
            x = block.blocksCentroid[0]
            y = block.blocksCentroid[1]
            z = block.blocksCentroid[2]
            
            source.SetRadius(self.pointRadius)
            source.SetCenter(x, y, z)
            source.SetPhiResolution(11)
            source.SetThetaResolution(21)
            
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(source.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.key = key
            
            r = 0.0
            g = 0.0
            b = 0.0
            actor.GetProperty().SetDiffuseColor(r, g, b)
            actor.GetProperty().SetDiffuse(.8)
            actor.GetProperty().SetSpecular(.5)
            actor.GetProperty().SetSpecularColor(1.0,1.0,1.0)
            actor.GetProperty().SetSpecularPower(30.0)
            
            try:
                
                if actor.key in self.toRemove:
                    continue
                else:
                    self.renderer.AddActor(actor)
            except NameError:
                self.renderer.AddActor(actor)
                continue

    def add_boundary_faces(self):
        
        self.currentBlockAncors=[]
        for thisBlock, blockData in self.domain.blocks.items():
            self.currentBlockAncors.append(blockData.ancor)
#        print(self.currentBlockAncors)
        
        for thisBlock, blockData in self.domain.blocks.items():
            
            x_idx=self.domain.x_axis.index(blockData.ancor[0])
            y_idx=self.domain.y_axis.index(blockData.ancor[1])
            z_idx=self.domain.z_axis.index(blockData.ancor[2])
            
            front_idx=[self.domain.x_axis[x_idx+1],self.domain.y_axis[y_idx],self.domain.z_axis[z_idx]]
            back_idx=[self.domain.x_axis[x_idx-1],self.domain.y_axis[y_idx],self.domain.z_axis[z_idx]]
            left_idx=[self.domain.x_axis[x_idx],self.domain.y_axis[y_idx+1],self.domain.z_axis[z_idx]]
            right_idx=[self.domain.x_axis[x_idx],self.domain.y_axis[y_idx-1],self.domain.z_axis[z_idx]]
            top_idx=[self.domain.x_axis[x_idx],self.domain.y_axis[y_idx],self.domain.z_axis[z_idx+1]]
            bottom_idx=[self.domain.x_axis[x_idx],self.domain.y_axis[y_idx],self.domain.z_axis[z_idx-1]]


            if not front_idx in self.currentBlockAncors:

                self.coords = self.domain.blocks[thisBlock].blocksFaces['front']
                self.faceName='front'
                self.thisBlock=thisBlock
                self.add_polygon()

            if not back_idx in self.currentBlockAncors:

                self.coords = self.domain.blocks[thisBlock].blocksFaces['back']
                self.faceName='back'
                self.thisBlock=thisBlock
                self.add_polygon()

            if not left_idx in self.currentBlockAncors:

                self.coords = self.domain.blocks[thisBlock].blocksFaces['left']
                self.faceName='left'
                self.thisBlock=thisBlock
                self.add_polygon()

            if not right_idx in self.currentBlockAncors:

                self.coords = self.domain.blocks[thisBlock].blocksFaces['right']
                self.faceName='right'
                self.thisBlock=thisBlock
                self.add_polygon()

            if not top_idx in self.currentBlockAncors:

                self.coords = self.domain.blocks[thisBlock].blocksFaces['top']
                self.faceName='top'
                self.thisBlock=thisBlock
                self.add_polygon()    
                
            if not bottom_idx in self.currentBlockAncors:

                self.coords = self.domain.blocks[thisBlock].blocksFaces['bottom']
                self.faceName='bottom'
                self.thisBlock=thisBlock
                self.add_polygon()
                
                
    def add_polygon(self):
        
                colors = vtk.vtkNamedColors()
                points = vtk.vtkPoints()
                points.InsertNextPoint(self.coords[0][0], self.coords[0][1], self.coords[0][2])
                points.InsertNextPoint(self.coords[1][0], self.coords[1][1], self.coords[1][2])
                points.InsertNextPoint(self.coords[2][0], self.coords[2][1], self.coords[2][2])
                points.InsertNextPoint(self.coords[3][0], self.coords[3][1], self.coords[3][2])
            
                # Create the polygon
                polygon = vtk.vtkPolygon()
                polygon.GetPointIds().SetNumberOfIds(4)  # make a quad
                polygon.GetPointIds().SetId(0, 0)
                polygon.GetPointIds().SetId(1, 1)
                polygon.GetPointIds().SetId(2, 2)
                polygon.GetPointIds().SetId(3, 3)
            
                # Add the polygon to a list of polygons
                polygons = vtk.vtkCellArray()
                polygons.InsertNextCell(polygon)
            
                # Create a PolyData
                polygonPolyData = vtk.vtkPolyData()
                polygonPolyData.SetPoints(points)
                polygonPolyData.SetPolys(polygons)
            
                # Create a mapper and actor
                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputData(polygonPolyData)
            
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                
                r = random.randint(200,235)/255.0 
                g = random.randint(200,255)/255.0
                b = 19/255.0
                
                actor.GetProperty().SetDiffuseColor(r, g, b)
                
#                actor.GetProperty().SetColor(colors.GetColor3d("Green"))
                actor.key=self.thisBlock+"_"+self.faceName+"_boundary"
            
                self.renderer.AddActor(actor)
                self.renderer.Render()  
                
    def show(self):
        
        axesActor = vtk.vtkAxesActor();
        axes = vtk.vtkOrientationMarkerWidget()
        axes.SetOrientationMarker(axesActor)
        axes.SetInteractor(self.interactor)
        axes.EnabledOn()
        self.interactor.RemoveObservers('CharEvent')


        self.balloonRep = vtk.vtkBalloonRepresentation()
        self.balloonRep.SetBalloonLayoutToImageRight()
        self.balloonRep = vtk.vtkBalloonRepresentation()
        self.balloonRep.SetBalloonLayoutToImageRight()
        self.balloonWidget = vtk.vtkBalloonWidget()
        self.balloonWidget.SetInteractor(self.interactor)
        self.balloonWidget.SetRepresentation(self.balloonRep)
        self.balloonWidget.EnabledOn()

        self.add_blocks()
        self.add_points()

        self.renwin.Render() 
        self.renwin.SetWindowName("blockMeshBuilder v0.0.1")


        self.modeTextEdit("Block & Point")

        self.interactor.Initialize()
        self.interactor.Start()
        
    def modeTextEdit(self,text):    

        try:
            self.renderer.RemoveActor(self.modeText)   
            self.modeText = vtk.vtkTextActor()
            self.modeText.SetInput("Edit mode: %s" % text)
            txtprop=self.modeText.GetTextProperty()
            txtprop.SetFontFamilyToTimes()
            txtprop.SetFontSize(18)
            txtprop.SetColor(1,1,1)
            self.modeText.SetDisplayPosition(5,5)
            self.renderer.AddActor(self.modeText)      
        
        except AttributeError:
            self.modeText = vtk.vtkTextActor()
            self.modeText.SetInput("Edit mode: %s" % text)
            txtprop=self.modeText.GetTextProperty()
            txtprop.SetFontFamilyToTimes()
            txtprop.SetFontSize(18)
            txtprop.SetColor(1,1,1)
            self.modeText.SetDisplayPosition(5,5)

            self.renderer.AddActor(self.modeText)     


