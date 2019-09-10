from blockMeshBuilder.src.block import Block

class Domain():
    
    def __init__(self,x_axis,y_axis,z_axis,x_sizes,y_sizes,z_sizes,gr_x,gr_y,gr_z):

        

        self.x_axis=x_axis
        self.y_axis=y_axis
        self.z_axis=z_axis

        self.x_sizes=x_sizes
        self.y_sizes=y_sizes
        self.z_sizes=z_sizes

        self.gr_x=gr_x
        self.gr_y=gr_y
        self.gr_z=gr_z
        
        self.check_sizes()
        self.check_gradings()
        
        self.points={}
        self.ancorPoints=[]
        self.blocks={}
        self.blockVertices={}
        self.boundary_points={}
        self.boundaryNames={}
        
        self.get_points()
        self.get_ancorPoints()
        self.get_block_divisions()
        self.get_blocks()
        self.update_centroid_relations()

        for L in [self.x_axis,self.y_axis,self.z_axis]:
            self.check_axis(L)


    def check_gradings(self):
        
        if len(self.gr_x) != len(self.x_axis)-1:
            print('x gradings list has too few or too many elements. \nMake sure gr_x has one less element than x_axis.')
            exit()
        if len(self.gr_y) != len(self.y_axis)-1:
            print('y gradings list has too few or too many elements. \nMake sure gr_y has one less element than y_axis.')
            exit()
        if len(self.gr_z) != len(self.z_axis)-1:
            print('z gradings list has too few or too many elements. \nMake sure gr_z has one less element than z_axis.')
            exit()
        

    def check_sizes(self):
        
        if len(self.x_sizes) != len(self.x_axis)-1:
            print('x cell size list has too few or too many elements. \nMake sure x_sizes has one less element than x_axis.')
            exit()
        if len(self.y_sizes) != len(self.y_axis)-1:
            print('y cell size list has too few or too many elements. \nMake sure y_sizes has one less element than y_axis.')
            exit()
        if len(self.z_sizes) != len(self.z_axis)-1:
            print('z cell size list has too few or too many elements. \nMake sure z_sizes has one less element than z_axis.')
            exit()


    def check_axis(self,L):
        
        if not all(x<y for x, y in zip(L, L[1:])):
            print('Lists containing axis definitions must monotonically increase.\nExample: x_axis=[0,1,2,3] not x_axis=[0,2,1,3].\nCheck them again and rerun.')

            exit()

    def get_block_divisions(self):
        
        self.x_divisions=[]
        self.y_divisions=[]
        self.z_divisions=[]
        
        
        for spacing in range(len(self.x_axis)-1):
            self.x_divisions.append(int(abs(round((self.x_axis[spacing+1]-self.x_axis[spacing])/self.x_sizes[spacing]))))
        print(self.x_divisions)

        for spacing in range(len(self.y_axis)-1):
            self.y_divisions.append(int(abs(round((self.y_axis[spacing+1]-self.y_axis[spacing])/self.y_sizes[spacing])))) 
            
        for spacing in range(len(self.z_axis)-1):
            self.z_divisions.append(int(abs(round((self.z_axis[spacing+1]-self.z_axis[spacing])/self.z_sizes[spacing])))) 
            
        
    def get_points(self):
        
        point=0
        for i in self.x_axis:
            for j in self.y_axis:
                for k in self.z_axis:
                    self.points['virtualVertex_'+str(point)]=[i,j,k]
                    point=point+1
        
        self.get_point_IDs()

    def get_point_IDs(self):
        self.pointID=[]
        count=0
        for key,point in self.points.items():
            self.pointID.append(str(count))
            count=count+1



    
    def get_ancorPoints(self):
        for z in self.z_axis:
            if z == self.z_axis[len(self.z_axis)-1]:
                continue
            for y in self.y_axis:
                if y == self.y_axis[len(self.y_axis)-1]:
                    continue
                for x in self.x_axis:
                    if x == self.x_axis[len(self.x_axis)-1]:
                        continue
                    else:
                        
                        self.ancorPoints.append([x,y,z])
        
    
    #Create class instance for each block
    def get_blocks(self):
        
        for count,ancor in enumerate(self.ancorPoints):
            

            x_index=self.x_axis.index(ancor[0])
            y_index=self.y_axis.index(ancor[1])
            z_index=self.z_axis.index(ancor[2])
            nmbrCells_x=str(self.x_divisions[x_index])
            nmbrCells_y=str(self.y_divisions[y_index])
            nmbrCells_z=str(self.z_divisions[z_index])
            gr_x=str(self.gr_x[x_index])
            gr_y=str(self.gr_y[y_index])
            gr_z=str(self.gr_z[z_index])    
            
            self.blocks["virtualBlock_"+str(count)+"_"]=Block(count,ancor,
                        self.x_axis,
                        self.y_axis,
                        self.z_axis,
                        nmbrCells_x,
                        nmbrCells_y,
                        nmbrCells_z,
						gr_x,
						gr_y,
						gr_z)
        
        self.update_blockID()
       
    def update_blockID(self):

        for count, block in enumerate(self.blocks):
            self.blocks[block].blockID= str(count)
               
        
    def update_centroid_relations(self):
        allBlockCentroids={}
        
        for key,block in self.blocks.items():
            allBlockCentroids[key]=block.blocksCentroid
        
        self.all_centroids_in_front={}
        self.all_centroids_in_back={}
        self.all_centroids_on_right={}
        self.all_centroids_on_left={}
        
        self.all_centroids_on_top={}
        self.all_centroids_on_bottom={}
        
        for key1,centroids in allBlockCentroids.items():
            
            x=centroids[0]
            y=centroids[1]
            z=centroids[2]
            
            centroids_in_front=[]
            centroids_in_back=[]
        
            centroids_on_right=[]
            centroids_on_left=[]
        
            centroids_on_top=[]
            centroids_on_bottom=[]
        
            for key2,block in allBlockCentroids.items():
        
                if y == block[1] and z == block[2] and block[0] > x:
                    centroids_in_front.append(key2)
                if y == block[1] and z == block[2] and block[0] < x:
                    centroids_in_back.append(key2)
            self.all_centroids_in_front[key1]=centroids_in_front
            self.all_centroids_in_back[key1]=centroids_in_back
        
            for key2,block in allBlockCentroids.items():
        
                if x == block[0] and z == block[2] and block[1] > y:
                    centroids_on_left.append(key2)
                if x == block[0] and z == block[2] and block[1] < y:
                    centroids_on_right.append(key2)
                    
            self.all_centroids_on_right[key1]=centroids_on_right
            self.all_centroids_on_left[key1]=centroids_on_left
        
            for key2,block in allBlockCentroids.items():
        
                if x == block[0] and y == block[1] and block[2] > z:
                    centroids_on_top.append(key2)
                if x == block[0] and y == block[1] and block[2] < z:
                    centroids_on_bottom.append(key2)
                    
            self.all_centroids_on_top[key1]=centroids_on_top
            self.all_centroids_on_bottom[key1]=centroids_on_bottom
            
            
            