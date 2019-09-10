
class Block():
    
    def __init__(self,count,ancor,x_axis,y_axis,z_axis,nmbrCells_x,nmbrCells_y,nmbrCells_z,gr_x,gr_y,gr_z):
        
        self.x_axis=x_axis
        self.y_axis=y_axis
        self.z_axis=z_axis

        self.nmbrCells_x=nmbrCells_x
        self.nmbrCells_y=nmbrCells_y
        self.nmbrCells_z=nmbrCells_z

        self.gr_x=gr_x
        self.gr_y=gr_y
        self.gr_z=gr_z
        
        self.ancor=ancor
        self.blockID=None
             
        self.blocksPoints=self.blocksPoints()
        self.blocksCentroid=self.blocksCentroid()
        self.blocksDimensions=self.blocksDimensions()
        self.blocksFaces()

        
    def blocksPoints(self):
        
        
        i=self.x_axis.index(self.ancor[0])
        j=self.y_axis.index(self.ancor[1])
        k=self.z_axis.index(self.ancor[2])
        
        p1=[self.x_axis[i],self.y_axis[j],self.z_axis[k]]
        p2=[self.x_axis[i+1],self.y_axis[j],self.z_axis[k]]
        p3=[self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k]]
        p4=[self.x_axis[i],self.y_axis[j+1],self.z_axis[k]]
        
        p5=[self.x_axis[i],self.y_axis[j],self.z_axis[k+1]]
        p6=[self.x_axis[i+1],self.y_axis[j],self.z_axis[k+1]]
        p7=[self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k+1]]
        p8=[self.x_axis[i],self.y_axis[j+1],self.z_axis[k+1]]
        
        blocksPoints=[p1,p2,p3,p4,p5,p6,p7,p8]
        return blocksPoints

    def blocksDimensions(self):
        i=self.x_axis.index(self.ancor[0])
        j=self.y_axis.index(self.ancor[1])
        k=self.z_axis.index(self.ancor[2])
        
        x_length=abs(self.x_axis[i+1]-self.x_axis[i])
        y_length=abs(self.y_axis[j+1]-self.y_axis[j])
        z_length=abs(self.z_axis[k+1]-self.z_axis[k])
        
        return [x_length,y_length,z_length]

    def blocksCentroid(self):
        
        x_positions=[]
        y_positions=[]
        z_positions=[]
        
        for point in self.blocksPoints:
            x_positions.append(point[0])
            y_positions.append(point[1])
            z_positions.append(point[2])
            
        x_centroid=sum(x_positions)/len(x_positions)
        y_centroid=sum(y_positions)/len(y_positions)
        z_centroid=sum(z_positions)/len(z_positions)
        
        return [x_centroid,y_centroid,z_centroid]
    

    def blocksFaces(self):
        
        i=self.x_axis.index(self.ancor[0])
        j=self.y_axis.index(self.ancor[1])
        k=self.z_axis.index(self.ancor[2])
        
        self.blocksFaces={}
        
        self.blocksFaces['right']=[[self.x_axis[i],self.y_axis[j],self.z_axis[k]],
              [self.x_axis[i+1],self.y_axis[j],self.z_axis[k]],
              [self.x_axis[i+1],self.y_axis[j],self.z_axis[k+1]],
              [self.x_axis[i],self.y_axis[j],self.z_axis[k+1]]]
        
        self.blocksFaces['left']=[[self.x_axis[i],self.y_axis[j+1],self.z_axis[k]],
              [self.x_axis[i],self.y_axis[j+1],self.z_axis[k+1]],
              [self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k+1]],
              [self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k]]]      
        
        self.blocksFaces['front']=[[self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k]],
              [self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k+1]],
              [self.x_axis[i+1],self.y_axis[j],self.z_axis[k+1]],
              [self.x_axis[i+1],self.y_axis[j],self.z_axis[k]]]        
        
        self.blocksFaces['back']=[[self.x_axis[i],self.y_axis[j],self.z_axis[k]],
              [self.x_axis[i],self.y_axis[j],self.z_axis[k+1]],
              [self.x_axis[i],self.y_axis[j+1],self.z_axis[k+1]],
              [self.x_axis[i],self.y_axis[j+1],self.z_axis[k]]]           
        
        self.blocksFaces['top']=[[self.x_axis[i],self.y_axis[j],self.z_axis[k+1]],
              [self.x_axis[i+1],self.y_axis[j],self.z_axis[k+1]],
              [self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k+1]],
              [self.x_axis[i],self.y_axis[j+1],self.z_axis[k+1]]]   
              
        self.blocksFaces['bottom']=[[self.x_axis[i],self.y_axis[j],self.z_axis[k]],
              [self.x_axis[i],self.y_axis[j+1],self.z_axis[k]],
              [self.x_axis[i+1],self.y_axis[j+1],self.z_axis[k]],
              [self.x_axis[i+1],self.y_axis[j],self.z_axis[k]]]












                       