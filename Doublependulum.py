import matplotlib.pyplot as plt
import numpy as np
import pygame
import math
from scipy.integrate import odeint


White=(255,255,255)
Black=(0,0,0)
Green=(0,255,0)
Width=600
Height=200
Point=[]

gameDisplay=pygame.display.set_mode((1200,800))

A=False

# Defining Function To Draw Pendulum At Specific Given Position

def Pendulum(L1,theta1,L2,theta2):

    Width=600
    Height=200
    # theta1+=0.1
    # theta2+=0.1
    pygame.draw.line(gameDisplay,White,(Width,Height),((L1)*math.sin(theta1)+Width,(L1)*math.cos(theta1)+Height),3)
    pygame.draw.circle(gameDisplay,White,(L1*math.sin(theta1)+Width,L1*math.cos(theta1)+Height),5,4)
    Width=L1*math.sin(theta1)+Width
    Height=L1*math.cos(theta1)+Height
    pygame.draw.line(gameDisplay,White,(Width,Height),((L2)*math.sin(theta2)+Width,(L2)*math.cos(theta2)+Height),3)
    pygame.draw.circle(gameDisplay,White,(L2*math.sin(theta2)+Width,L2*math.cos(theta2)+Height),5,4)
    return (L2*math.sin(theta2)+Width,L2*math.cos(theta2)+Height)
        
# INTEGRATION PART 

def Fun(Y,t,m1,m2,g,L1,L2):
    
    theta1,Avel1,theta2,Avel2=Y
    
    num1 = - g*(2*m1+m2)*math.sin(theta1)                           
    num2 = - m2*g*math.sin(theta1-2*theta2)
    num3 = - 2*math.sin(theta1-theta2) * m2
    num4 =   pow(Avel1,2)*L2 + pow(Avel2,2) *L1*math.cos(theta1-theta2)
    den  =   L1*(2*m1+m2-m2*math.cos(2*theta1-2*theta2))

    Aacc1 = (num1 + num2 +num3*num4)/den

    num11 = 2*math.sin(theta1-theta2)
    num12 = (pow(Avel1,2)*L1*(m1+m2))
    num13 = g*(m1+m2)*math.cos(theta1)
    num14 = pow(Avel2,2)*L2*m2*math.cos( theta1-theta2 )

    Aacc2 = (num11*(num12+num13+num14))/den*L2/L1

    dYdt=  [ Avel1, Aacc1,Avel2,Aacc2]

    return dYdt

# TRACING PATH OF PENDULUM

def drawpoint(k):

    Point.append(k)

    if len(Point)>=10000:
        Point.pop(1)

    for i in range(len(Point)):
        gameDisplay.set_at((int(Point[i][0]),int(Point[i][1])),Green)


m1=20                                  #  Mass of First Pendulum
m2=40                                  #  Mass of First Pendulum
g=9.81                                 #  Gravity Of Simulation
L1=200                                 #  Length  Of first Arm 
L2=200                                 #  Length  Of first Arm 
t=[]                                   #  Time Array
i=0                                                     
initialcondition=[np.pi/2,0,np.pi/2,0]  # InitialConditions = [angle of first Pendulum , initial Velocity of first Pendulum ,angle of second Pendulum , initial Velocity of second Pendulum ]

#  Display Update Loop

while True:

    gameDisplay.fill(Black)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            A=True
            
    pygame.draw.line(gameDisplay,White,(550,200),(650,200))

    if A==True:
        
        t.append(i)
    if len(t)>1:

        F=odeint(Fun,initialcondition,t,args=(m1,m2,g,L1,L2))

        F=np.delete(F,0,0)
        theta1=initialcondition[0]
        theta2=initialcondition[2]
        J= Pendulum(L1=L1,theta1=theta1,L2=L2,theta2=theta2)
        drawpoint(J)
        initialcondition=F[0]
        t.pop(0)
        F=np.delete(F,1,1)
        F=np.delete(F,1,1)
        i+=0.05
        # print(F)
    pygame.display.update()

#Created by Harsh Maurya with 💖 ............ :)