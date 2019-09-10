import vtk
import numpy as np

class UserInteraction(vtk.vtkInteractorStyleTrackballCamera):
 
    def __init__(self,render,parent=None):
        
        self.render=render
        
        self.deletedActors=self.render.deletedActors
        self.AddObserver("RightButtonPressEvent",self.RightButtonPressEvent)
        self.AddObserver("MiddleButtonPressEvent",self.MiddleButtonPressEvent)
        self.AddObserver("KeyPressEvent",self.KeyPress)

        
        self.LastPickedActor = None
        self.selectedActors=[]
        
        self.deletedActors=[]
        self.deletedActorProperties=[]
        
        self.previouslySelectedActorProperties=[]
        self.previouslySelectedActors=[]

    def removeBlockActors(self):

        self.actors=self.render.renderer.GetActors()
        
        for actor in self.actors:
            
            if "Block" in actor.key:
                self.render.renderer.RemoveActor(actor)
                self.render.balloonWidget.RemoveBalloon(actor)
                
                
        self.render.renwin.Render()      

    def removePointActors(self):

        self.actors=self.render.renderer.GetActors()
        
        for actor in self.actors:
            
            if "Vertex" in actor.key:
                self.render.renderer.RemoveActor(actor)
                self.render.balloonWidget.RemoveBalloon(actor)
                
                
        self.render.renwin.Render()  

    def removeBoundaryActors(self):

        self.actors=self.render.renderer.GetActors()
        
        for actor in self.actors:
            
            if "_boundary" in actor.key:
                self.render.renderer.RemoveActor(actor)
                self.render.balloonWidget.RemoveBalloon(actor)
                
        self.render.renwin.Render()      

    def RightButtonPressEvent(self,obj,event):
        
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
        
        # get the new
        self.NewPickedActor = picker.GetActor()
        if self.NewPickedActor in self.selectedActors:
            return
        LastPickedProperty = vtk.vtkProperty()
        # If something was selected
        if self.NewPickedActor:

            self.selectedActors.append(self.NewPickedActor)
            LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            self.previouslySelectedActorProperties.append(LastPickedProperty)
            
            # Highlight the picked actor by changing its properties
            self.NewPickedActor.GetProperty().SetColor(1.0, 0.0, 0.0)
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            self.previouslySelectedActors.append(self.NewPickedActor)
            

        self.OnRightButtonDown()

        return 


    def MiddleButtonPressEvent(self,obj,event):
        
   
        try:
            self.previouslySelectedActors[-1].GetProperty().DeepCopy(self.previouslySelectedActorProperties[-1])
    
            del self.selectedActors[-1]
            del self.previouslySelectedActors[-1]
            del self.previouslySelectedActorProperties[-1]
            
            self.render.renwin.Render()
            
        except IndexError:
            print('No selection to undo!')


    def delete_actors(self):
        
        for count,actorToRemove in enumerate(self.selectedActors):
            
            # self.deletedActors.append(actorToRemove)
            # self.deletedActorProperties.append(actorToRemove.GetProperty())
            
            #check if coordinates associated with vertex
            
            if actorToRemove.key in self.render.points:
                for key,block in self.render.blocks.items():
                    for point in block.blocksPoints:
                        if self.render.domain.points[actorToRemove.key] == point:
                            print("A selected vertex belongs to a block, can't delete it. Delete block first.")
                            self.selectedActors.clear()
                            self.previouslySelectedActors[count].GetProperty().DeepCopy(self.previouslySelectedActorProperties[count])
                            self.render.renwin.Render()
                            return
    
            if actorToRemove.key in self.render.points:
                del self.render.points[actorToRemove.key]
                self.render.domain.get_point_IDs()
                self.render.add_points()

            self.render.renderer.RemoveActor(actorToRemove)
            self.render.balloonWidget.RemoveBalloon(actorToRemove)
            
            if actorToRemove.key in self.render.blocks:
                
                del self.render.blocks[actorToRemove.key]
                self.render.domain.update_centroid_relations()
                self.render.domain.update_blockID()
            
        self.selectedActors.clear()
        

    def undo_delete_actors(self):

        self.render.renderer.AddActor(self.deletedActSelectedActors[-1])
        self.previouslySelectedActors[-1].GetProperty().DeepCopy(self.previouslySelectedActorProperties[-1])
        self.render.renwin.Render()
        

    def KeyPress(self,obj,event):
        
        key = self.render.parent.GetKeySym()

        if key == 'w':

            #if self.render.mode == 0:
            actors = self.render.renderer.GetActors()
            actors.InitTraversal()
            actor = actors.GetNextItem()
            while actor:
                actor.GetProperty().SetRepresentationToWireframe()
                actor = actors.GetNextItem()
        
            self.render.renderer.Render()

            #if self.render.mode == 1:
            #    print("Wireframe toggle not available in Boundary edit mode.")         

        if key == 's':

            #if self.render.mode == 0:
            actors = self.render.renderer.GetActors()
            actors.InitTraversal()
            actor = actors.GetNextItem()
            while actor:
                actor.GetProperty().SetRepresentationToSurface()
                actor = actors.GetNextItem()
        
            self.render.renderer.Render()

            #if self.render.mode == 1:
             #   print("Surface toggle not available in Boundary edit mode.")    

        if key == 'b':
            
            self.selectedActors=[]
            
            if self.render.mode == 1:
                self.render.modeTextEdit("Block & Point")
                self.render.mode = 0
                self.removeBoundaryActors()
                self.render.add_blocks()
                self.render.renwin.Render() 

        if key == 'f':
            

            if self.render.mode == 0:
                self.render.modeTextEdit("Boundary")
                self.render.mode = 1
                self.removeBlockActors()
                self.render.add_boundary_faces()
                self.render.renwin.Render()        

        if key == 'd':

            if self.render.mode == 0:
                self.delete_actors()
                self.removeBlockActors()
                self.render.add_blocks()
                self.removePointActors()
                self.render.add_points()
                self.render.renwin.Render()
            else:
                print("Cannot delete points or boundary faces in Boundary edit mode.")

        # if key == 'h':
            
        #     self.actors=self.render.renderer.GetActors()
            
        #     for actor in self.actors:
                
        #         if "_boundary" in actor.key:
        #             self.render.renderer.RemoveActor(actor)
                    
        #     self.render.renwin.Render()

        if key == 'n':
            
            check=1
            
            if len(self.selectedActors)==0:
                check=0
                
            for actor in self.selectedActors:
                
                if "_boundary" in actor.key:
                    continue
                else:
                    check=0
                    
            if check == 1:
                
                self.render.interactor.RemoveObservers('CharEvent')

                patchName = input("Enter patch name for selected faces (no spaces): ")
                patchName=patchName.replace(" ","")
                
                
                if patchName in self.render.domain.boundaryNames:
                    
                    print('Patch name already defined, appending selection(s) to existing boundary patch.' )
                    
                    temp_boundary=[]
                    
                    for actor in self.selectedActors:
                        
                        if 'boundary' in actor.key:
                            
                            self.render.balloonWidget.AddBalloon(actor, "Boundary: %s" % patchName)
                           
                            block_id='_'+''.join(x for x in actor.key if x.isdigit())+'_'
                            
                            for block, value in self.render.blocks.items():
                                
                                if block_id in block:
                                    
                                    if 'right' in actor.key:
                                        temp_boundary.append(value.blocksFaces['right'])
                                    if 'left' in actor.key:
                                        temp_boundary.append(value.blocksFaces['left'])
                                    if 'top' in actor.key:
                                        temp_boundary.append(value.blocksFaces['top'])                                
                                    if 'bottom' in actor.key:
                                        temp_boundary.append(value.blocksFaces['bottom'])                             
                                    if 'front' in actor.key:
                                        temp_boundary.append(value.blocksFaces['front'])                               
                                    if 'back' in actor.key:
                                        temp_boundary.append(value.blocksFaces['back'])   

                    for face in temp_boundary:
                        if face in self.render.domain.boundary_points[patchName]:
                            
                            print('At least one selection already added to %s boundary! Nothing new added ...' %patchName)
                            continue
                        else:
                            self.render.domain.boundary_points[patchName].append(face) 
                            print("Selected faces added to boundary patch: %s" %patchName)
                    
                else:
                    
                    patchType = input("Enter patch type for selected faces: ")
                    
                    temp_boundary=[]
                    
                    self.render.domain.boundaryNames[patchName]=patchType
                
                    for actor in self.selectedActors:
                        
                        self.render.balloonWidget.AddBalloon(actor, "Boundary: %s" % patchName)
                        
                        if 'boundary' in actor.key:
                           
                            block_id='_'+''.join(x for x in actor.key if x.isdigit())+'_'
                            
                            for block, value in self.render.blocks.items():
                                
                                if block_id in block:
                                    
                                    if 'right' in actor.key:
                                        temp_boundary.append(value.blocksFaces['right'])
                                    if 'left' in actor.key:
                                        temp_boundary.append(value.blocksFaces['left'])
                                    if 'top' in actor.key:
                                        temp_boundary.append(value.blocksFaces['top'])                                
                                    if 'bottom' in actor.key:
                                        temp_boundary.append(value.blocksFaces['bottom'])                             
                                    if 'front' in actor.key:
                                        temp_boundary.append(value.blocksFaces['front'])                               
                                    if 'back' in actor.key:
                                        temp_boundary.append(value.blocksFaces['back'])   
                            
                            self.render.domain.boundary_points[patchName]=temp_boundary
                
                    print("Selected faces added to boundary patch: %s" %patchName)
                
                for i in range(len(self.selectedActors)):
                    self.selectedActors[i].GetProperty().SetColor(49/255, 145/255, 30/255)
#                    self.previouslySelectedActors[i].GetProperty().DeepCopy(self.previouslySelectedActorProperties[i])
        
                self.selectedActors=[]
                self.previouslySelectedActors=[]
                self.previouslySelectedActorProperties=[]
                
                self.render.renwin.Render()


                    
            elif check ==0:
                print("Oops, no boundary faces selected ...")
                print("or, at least one selected item is not a boundary! Cannot assign patch name.")
                    

        if key == 'p':
            
            
            f= open('./system/blockMeshDict',"w+")
            f.write("FoamFile\n")
            f.write("{\n")
            f.write("    version      2.0;\n")
            f.write("    format       ascii;\n")
            f.write("    class        dictionary;\n")
            f.write("    object       blockMeshDict;\n")
            f.write("}\n")
            f.write("\n")
            f.write("convertToMeters 1;\n")
            f.write("\n")
            f.close()
            
            
            """ready vertices for write"""
            
            self.render.vertices=[]
            
            for key, value in self.render.points.items():
                self.render.vertices.append(value)
            
            self.render.vertices=np.asarray(self.render.vertices)
            
            if self.render.vertices.shape[1]==3:
                
                f= open('./system/blockMeshDict',"a+")
                    
                f.write("vertices\n")
                f.write("(\n")
                
                for i in range(self.render.vertices.shape[0]):
                    
                    f.write("(%.5f %.5f %.5f) // %s\n" % (self.render.vertices[i][0],
                            self.render.vertices[i][1],
                            self.render.vertices[i][2],
                            self.render.domain.pointID[i]))
                
                f.write(");")
                f.close()
                print('Successfully wrote vertices list to file.')            
            
            
            
#            writeVerticesList(self.render.vertices,'.','testing.txt')
            
            
            """Associate vertex coords with a number"""
            self.render.verticeIdsOfPatch={}
            
            for boundary, value in self.render.domain.boundary_points.items():
                
                temp=[]
                for face in value:
                    
                    temp2=[]
                    for vertex in face:
                        
                        temp2.append(np.where((self.render.vertices == vertex).all(axis=1))[0][0])
                    temp.append(temp2)
                    
                self.render.verticeIdsOfPatch[boundary]=temp

            
            """ready blocks for write"""
            f= open('./system/blockMeshDict',"a+")
            f.write("\n")
            f.write("\n")
            f.write("blocks\n")
            f.write("(\n")
            
            for block_id, blockData in self.render.blocks.items():
                
                temp=[]
                for vertex in blockData.blocksPoints:
                    
                    temp.append(np.where((self.render.vertices == vertex).all(axis=1))[0][0])
                f.write("    hex (%s %s %s %s %s %s %s %s) (%s %s %s) simpleGrading (%s %s %s)\n" % (temp[0],
                        temp[1],
                        temp[2],
                        temp[3],
                        temp[4],
                        temp[5],
                        temp[6],
                        temp[7],
                        blockData.nmbrCells_x,
                        blockData.nmbrCells_y,
                        blockData.nmbrCells_z,
						blockData.gr_x,
						blockData.gr_y,
						blockData.gr_z))
                
                self.render.domain.blockVertices[block_id]=temp
            
            f.write(");")
            f.close()
             
            print('Successfully wrote blocks to file.')            

            

            """ready boundary for write"""

            f= open('./system/blockMeshDict',"a+")
            f.write("\n")
            f.write("\n")
            f.write("boundary\n")
            f.write("(\n")
        
            if len(self.render.domain.boundary_points.items()) == 0:
                print("However, no boundary definitions were written because none were defined!\nIf desired, define boundary patches and press (p) again.")
                f.write(");\n")
                f.write("\n")  
            else:
                for boundary, boundaryVertices in self.render.domain.boundary_points.items():
                    
    #                print(boundary)
                    f.write("    %s\n" %boundary)
                    f.write("    {\n")
                    f.write("        type %s;\n" %self.render.domain.boundaryNames[boundary])
                    f.write("        faces\n")
                    f.write("        (\n")   
                    
                    for piece in boundaryVertices:
    #                    print(piece)
                        temp=[]
            
                        for vertex in piece:
    #                        print(vertex)
    #                        print(vertex)
                            temp.append(np.where((self.render.vertices == vertex).all(axis=1))[0][0])
            
                        f.write("         (%s %s %s %s) \n" % (temp[0],temp[1],temp[2],temp[3]))   
                    
                    f.write("        );\n")
                    f.write("    }\n")
                        
                f.write(");\n")
                f.write("\n")   
                
                print('Successfully wrote boundaries to file.')    

            f.write("\n")
            f.write("edges\n")
            f.write("(\n")
            f.write(");\n")
            f.write("\n")
            
            f.write("edges\n")
            f.write("(\n")
            f.write(");\n")
            f.close() 
            
        if key == 'u':
            pass

#            self.style.undo_delete_actors()


#    def Wireframe(self):
#        actors = self.render.GetActors()
#        actors.InitTraversal()
#        actor = actors.GetNextItem()
#        while actor:
#            actor.GetProperty().SetRepresentationToWireframe()
#            actor = actors.GetNextItem()
#    
#        self.render.Render()




