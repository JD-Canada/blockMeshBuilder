import blockMeshBuilder as block


x_axis=[0,0.005,0.04,0.395,0.4]
y_axis=[0,0.0275,0.0675,0.1025]
z_axis=[0,0.035,0.250]

x_sizes=[0.001,0.002,0.002,0.002]
y_sizes=[0.002,0.002,0.002]
z_sizes=[0.002,0.002]

gr_x=[1,1,1,1]
gr_y=[1,1,1]
gr_z=[1,1]

domain=block.Domain(x_axis,y_axis,z_axis,x_sizes,y_sizes,z_sizes,gr_x,gr_y,gr_z)
        
a=block.Render(domain)
a.show()





