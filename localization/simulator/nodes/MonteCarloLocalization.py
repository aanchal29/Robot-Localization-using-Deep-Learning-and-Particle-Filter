#!/usr/bin/env python

import sys, os
import roslib;
import rospy
import numpy as np
import sensing_model_and_map as senseModelMap
import threading
import random
import pygame
from collections import namedtuple
from math import *
from rospy import sleep
from geometry_msgs.msg import Twist
from std_msgs.msg import String

#bg pic thing
pic_tag = '../map/mapfile.png'

# pygame code
pygame.init()
breadth = 650
length = 150
screen = pygame.display.set_mode((breadth, length))

Particle = namedtuple('Particle', ['x', 'w'])
no_of_ptcls = 2200
ptcls = [random.randint(0, 599) for a in xrange(no_of_ptcls)]

#for left right
if 'left' in [arg.lower() for arg in sys.argv]:
    vel = -4.0
else:
    vel = 4.0

#helper method for displaying 
def printing(background = None):
    global screen, breadth, length

    screen.fill((255,255,255))

    size_scling = 02
    box = np.array([0.0 for a in xrange(600)])
    for s in ptcls:
        b = int(s)
        gap = s - b 
        box[b] += (1.-gap)*size_scling 
        if b < 599:
            box[b+1] += gap*size_scling

    for a, b in enumerate(box):
        pygame.draw.line(screen, (0, 0, 0), (a, length-b), (a, length))

    pygame.display.flip()
    return

#helper method for caling the printhing method to run in lop
def printing_ring(background = None):
    while True:
        printing(background)
        sleep(0.2)
    return

#helper method for data receied from snsrs
def snsr_hndlr(snsr_rdng_data):
    monteCarloLocalization(ptcls, vel, snsr_rdng_data.data)
    return 

#helper method for printing the given data
def print_data(rdng):
    print rdng.data

#helper method for implementing monte carlo localization
def monteCarloLocalization(previous_bel, control, measurement):

    #defining right hand side border
    def rght_border(x):
        if x > 600:
            return random.randint(0, 599)
        else:
            return x

    #defining left hand side border
    def lft_border(x):
        if x <= 0:
            return random.randint(0, 599)
        else:
            return x 

    #if else loop to update the boder values
    if vel > 0:
	border = rght_border
    else:
	border = lft_border

    #if else loop to update pValue_X
    if measurement == 'Wall':
	pValue_X = senseModelMap.p_wall
    else:
	pValue_X = senseModelMap.p_door

    mvmnt_modl_data = [border(s + random.gauss(control, 0.75)) for s in previous_bel]
   
    measrmnt_modl_data = [pValue_X(s/10.0) for s in mvmnt_modl_data]


    qty_begin = random.randint(0, no_of_ptcls-1)
    measrmnt_modl_data = np.array(measrmnt_modl_data[qty_begin:] + measrmnt_modl_data[:qty_begin],
                       dtype = float)
    mvmnt_modl_data = mvmnt_modl_data[qty_begin:] + mvmnt_modl_data[:qty_begin]

    cumulative_sum = measrmnt_modl_data.cumsum() 
    value = cumulative_sum[-1]
    cumulative_sum /= value

    smpl_values = np.random.random(no_of_ptcls)
    mvnt_modl_data_value = cumulative_sum.searchsorted(smpl_values, side='right')
    Pbblty = [mvmnt_modl_data[a] for a in mvnt_modl_data_value]
    
    # putting Pbblty in global variable
    global ptcls
    ptcls = Pbblty

    return

# helper methd to pblsh the cmd
def pblsh_topic():
    while True:
        controller.publish(cmd)
        sleep(0.2)
    return 

#starting of main loop 
if __name__ == '__main__':
    random.seed()

    rospy.init_node('particle_filter')

    controller = rospy.Publisher('/cmd_vel', Twist)
    cmd = Twist()
    cmd.linear.x = vel 
    cmd_thread = threading.Thread(target = pblsh_topic)
    cmd_thread.start()

    rospy.Subscriber('robot/wall_door_sensor', String, snsr_hndlr)

    bckgrnd_pic = os.path.abspath(pic_tag)

    try:
        temp_pic_tag = pygame.image.load(bckgrnd_pic)
        bgPic = temp_pic_tag.convert()
    except pygame.error, message:
        bgPic = None

    vis_thread = threading.Thread(target = printing_ring, args=(bgPic,))
    vis_thread.start()

    rospy.spin()
