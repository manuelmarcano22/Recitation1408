from visual import*
from visual.graph import *



# setup (do not edit these components)
pos_init=vector(0,0,0) 
vel_init=vector(0,0,0) 
pos2_init=vector(0,0,0) 
vel2_init=vector(0,0,0) 

#####################################
##
## EDIT KINEMATICS PARAMETERS HERE
##
##
pos_init.x=0.0
vel_init.x=1.0
def acc(t,x,v):
    return vector(0.,0.,0.)

pos2_init.x=0.0
vel2_init.x=1.0
def acc2(t,x,v):
    return vector(-0.2,0.,0.)

# color scheme
#
BW=1
if BW==0:
    fgcolor=color.black; bgcolor=color.white
else:
    fgcolor=color.white; bgcolor=color.black
b1color=color.red
b2color=(0,.75,0)

#
# setup main scene
#
scene=display(
    title="1-dimensional kinematics",
    width=500,height=600,
    x=250, y=0,
    autoscale=0,
    range=(3,3,3),
    foreground=fgcolor,
    background=bgcolor
    )
scene.lights = [vector(0,0.3,0) ]; scene.ambient = 0.7

scene.forward=vector(0.1,-.10,0.)
scene.fov=1e-14  # pseudo-orthogonal


#
# track
#
tracklength=20
track = box(pos=(tracklength/2,-0.05,0), axis=( 1 , 0 ,0),
        length=tracklength, height=.1, width=2, color=color.orange) 

##tick marks on the track
c=[]
for x in arange(tracklength):
    cu = curve( z = arange(-1,2,1) ,color=(0.25,0.25,1.0))
    c.append(cu)
    c[x].y = 0.01
    c[x].x = x

#
# blocks
#
block_height=0.25

# setup initial POSITIONS (sit on track)
pos_init.y=block_height/2. ; pos_init.z=-0.5
pos2_init.y=block_height/2. ; pos2_init.z=0.5


block = box(pos=pos_init, axis=track.axis,
        length=0.50, height=block_height, width=.50, color=b1color)
block2 = box(pos=pos2_init, axis=track.axis,
         length=0.50, height=block_height, width=.50, color=b2color)

block.vel = vel_init
block2.vel = vel2_init


#
# kinematic graphs
#
pos_graph = gdisplay(x=0, y=000, width=250, height=200, 
             title='Position vs. Time', xtitle='t(s)', ytitle='x (m)', 
             xmax=10., xmin=0., ymax=20, ymin=-4, 
             foreground=fgcolor, background=bgcolor)
pos_Plot = gcurve(color=b1color)
pos2_Plot = gcurve(color=b2color)


vel_graph = gdisplay(x=0, y=200, width=250, height=200, 
             title='Velocity vs. Time', xtitle='t(s)', ytitle='v (m/s)', 
             xmax=10., xmin=0., ymax=2, ymin=-2, 
             foreground=fgcolor, background=bgcolor)
vel_Plot = gcurve(color=b1color)
vel2_Plot = gcurve(color=b2color)


acc_graph = gdisplay(x=0, y=400, width=250, height=200, 
             title='Acceleration vs. Time', xtitle='t(s)', ytitle='a (m/s^2)', 
             xmax=10., xmin=0., ymax=2, ymin=-2, 
             foreground=fgcolor, background=bgcolor)
acc_Plot = gcurve(color=b1color)
acc2_Plot = gcurve(color=b2color)


#
#SETUP ANIMATION
#
time = 0.
counter=0

count_tick=100              #for ticks at 1-second intervals
count_subtick=count_tick/5  #for ticks at 0.2-second intervals
dt=1./count_tick

scene.mouse.getclick() #wait for click


while time <= 10:  #run for 10 seconds
    rate(50)

    #CLICK TO PAUSE, THEN CLICK AGAIN TO CONTINUE
    if scene.mouse.clicked:
        scene.mouse.getclick()
        scene.mouse.getclick()
    
    a = acc(time,block.pos,block.vel)        
    a2= acc2(time,block2.pos,block2.vel)
        
    block.acc =  a
    block2.acc = a2

    block.pos +=  block.vel*dt
    block.vel +=  block.acc*dt

    block2.pos += block2.vel*dt
    block2.vel += block2.acc*dt

        

    ### MARK MOTION WITH TICKS
    if counter%count_tick == 0:
        box(pos=block.pos, axis=track.axis, size=(0.075,0.075,0.075), color=b1color)
        box(pos=block2.pos, axis=track.axis, size=(0.075,0.075,0.075), color=b2color)
        if mag(block.vel)>0:
            arrow(pos=block.pos,axis=block.vel/2.,color=b1color,fixedwidth = 1)
        if mag(block2.vel)>0:
            arrow(pos=block2.pos,axis=block2.vel/2.,color=b2color,fixedwidth = 1)
    elif counter%count_subtick == 0:
        box(pos=block.pos, axis=block.vel, size=(0.05,0.05,0.05), color=b1color)
        box(pos=block2.pos, axis=block2.vel, size=(0.05,0.05,0.05), color=b2color)

    if counter%count_subtick == 0:
        acc_Plot.plot(pos=(time,block.acc.x))
        vel_Plot.plot(pos=(time,block.vel.x))
        pos_Plot.plot(pos=(time,block.pos.x))
        acc2_Plot.plot(pos=(time,block2.acc.x))
        vel2_Plot.plot(pos=(time,block2.vel.x))
        pos2_Plot.plot(pos=(time,block2.pos.x))


    scene.center=vector(block.pos.x,0,0)  #keep block in view

    time = time + dt
    counter += 1



#Now... WHEN AN OBJECT IS PICKED,
#TRANSLATE THE scene.center TO THE OBJECT'S POSITION        
while 1:
    rate(5)
    if scene.mouse.clicked:
        scene.mouse.getclick()
        newPick=scene.mouse.pick
        if newPick !=None:
            ### ANIMATE TO SELECTED POSITION
            tempcolor=newPick.color
            newPick.color=color.yellow
            target=newPick.pos
            step=(target-scene.center)/20.
            for i in arange(1,20,1):
                rate(10)
                scene.center +=step
            newPick.color=tempcolor
