#This is my first time learn "class",so I take professor's code, make some notes and change a little,I'm not sure these notes are correct or not, so welcome to leave some comments!
from pylab import *
from math import *
g = 9.8
b2m = 1e-5
#init is a special method that get invoked when an object is instantiated.when you define an object in this class,it will be assigned these attributes
class flight_state:
    def __init__(self, _x = 0, _y = 0, _vx = 0, _vy = 0, _t = 0):#variables with _ at the beginning should be regarded as private variables, although they can be visited from outside 
        self.x = _x#stores the value of the parameter _x as an attribute of self
        self.y = _y
        self.vx = _vx
        self.vy = _vy
        self.t = _t

class cannon:
    def __init__(self, _fs = flight_state(0, 0, 0, 0, 0), _dt = 0.1):
        self.cannon_flight_state = []#set a list and store all the value of flight_state in it,five a group
        self.cannon_flight_state.append(_fs)
        self.dt = _dt
        print self.cannon_flight_state[-1].x, self.cannon_flight_state[-1].y, self.cannon_flight_state[-1].vx, self.cannon_flight_state[-1].vy

#calculate vi+1,xi+1,yi+1,and use it as a independent function
    def next_state(self, current_state):
        global g
        next_x = current_state.x + current_state.vx * self.dt
        next_vx = current_state.vx
        next_y = current_state.y + current_state.vy * self.dt
        next_vy = current_state.vy - g * self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)#the function "next_state" assign new value to flight_state

#fix the place where the cannon shell land
    def shoot(self):
        while not(self.cannon_flight_state[-1].y < 0):#while y>0
            self.cannon_flight_state.append(self.next_state(self.cannon_flight_state[-1]))#assign the value of current_state to next_state to calcute the new state,and put it in as cannon_flight_state[-1]
        print self.cannon_flight_state[-1].x, self.cannon_flight_state[-1].y, self.cannon_flight_state[-1].vx, self.cannon_flight_state[-1].vy
#donot put print in the whilr iteration, that will print lots of datas  
        r = - self.cannon_flight_state[-2].y / self.cannon_flight_state[-1].y#r=-yn/yn+1
        self.cannon_flight_state[-1].x = (self.cannon_flight_state[-2].x + r * self.cannon_flight_state[-1].x) / (r + 1)#fix the value of x when y=0
        self.cannon_flight_state[-1].y = 0

#a function use for plot
    def show_trajectory(self):
        x = []
        y = []
        for fs in self.cannon_flight_state:#we can rewrite "fs" as "t",it do not affect the result,because "fs" refers to a group of the five values (x,y,vx,vy,t)
            x.append(fs.x)
            y.append(fs.y)
        plot(x,y,label='tan$v_y/v_x=$'+str(self.cannon_flight_state[1].vy/self.cannon_flight_state[1].vx))
        legend(loc='best',prop={'size':11},frameon=False)
        title('The trajectory of a cannon shell')
        xlabel('x/m')
        ylabel('y/m')
        #show()

#consider the air resistance
class drag_cannon(cannon):#drag_cannon inherit cannon
    def next_state(self, current_state):
        global g, b2m#b2m is calculated from the isothermal approximation
        v = sqrt(current_state.vx * current_state.vx + current_state.vy * current_state.vy)
#if we calculate vx first and assign the value of next_vx to next_x, the result may be more precise                
        next_vx = current_state.vx - b2m * v * current_state.vx * self.dt
        next_x = current_state.x + next_vx* self.dt
        next_vy = current_state.vy - g * self.dt - b2m * v * current_state.vy * self.dt
        next_y = current_state.y + next_vy* self.dt
        #print next_x, next_y
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t + self.dt)#don't forget to assign new value to flight_state

#to calculate b2m with the isothermal approximation        

class iso_drag_cannon(cannon):
    def next_state(self,current_state):
        global b2m
        b2m2=b2m*exp(-current_state.y/1e+4)
        v=sqrt(current_state.vx*current_state.vx+current_state.vy*current_state.vy)
        next_vx=current_state.vx-b2m2*v*current_state.vx*self.dt
        next_x =current_state.x+ next_vx*self.dt
        next_vy=current_state.vy-b2m2*v*current_state.vy*self.dt
        next_y=current_state.y+ next_vy*self.dt
        return flight_state(next_x,next_y,next_vx,next_vy,current_state.t+self.dt)  


#with adiabatic approximation

class adiabatic_drag_cannon(cannon):
    def next_state(self, current_state):
        global g
        v=sqrt(current_state.vx * current_state.vx+current_state.vy * current_state.vy)
        next_vx = current_state.vx-(1-6.5e-3*current_state.y/300)**2.5 * v * current_state.vx * self.dt
        next_x = current_state.x+ next_vx*self.dt
        next_vy = current_state.vy - g*self.dt - (1-6.5e-3*current_state.y/300)**2.5 * v * current_state.vy *self.dt
        next_y = current_state.y + next_vy* self .dt
        return flight_state(next_x, next_y, next_vx, next_vy, current_state.t +self.dt)   

        pass#pass is a null operation, just to make the program complete
#once classes are defined, usage will be conveninent
a1 = cannon(flight_state(0,0,573.4,401.2,0),_dt=0.1)#vy/vx=tan35
a2 = cannon(flight_state(0,0,536.2,449.9,0),_dt=0.1)#vy/vx=tan40
a3 = cannon(flight_state(0,0,494.9,494.9,0),_dt=0.1)#vy/vx=tan45
a4 = cannon(flight_state(0,0,449.9,536.2,0),_dt=0.1)#vy/vx=tan50
a5 = cannon(flight_state(0,0,401.5,573.4,0),_dt=0.1)#vy/vx=tan50
a1.shoot()#the landing point
a2.shoot()
a3.shoot()
a4.shoot()
a5.shoot()

##b = drag_cannon(flight_state(0, 0, 700, 700, 0), _dt = 0.1)
##b.shoot()
##b.show_trajectory()
a1.show_trajectory()
a2.show_trajectory()
a3.show_trajectory()
a4.show_trajectory()
a5.show_trajectory()
show()
