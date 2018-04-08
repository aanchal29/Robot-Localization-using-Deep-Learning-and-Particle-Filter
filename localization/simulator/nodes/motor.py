#!/usr/bin/env python
import roslib; roslib.load_manifest('uml_hmm')
import rospy

import random

from geometry_msgs.msg import Twist

cmd_vel = rospy.Publisher('/stage/cmd_vel', Twist)

def got_cmd_vel(msg):
    global cmd_vel

    msg.linear.x = random.gauss(msg.linear.x, msg.linear.x / 3.0)
    msg.linear.y = 0
    msg.linear.z = 0

    msg.angular.x = 0
    msg.angular.y = 0
    msg.angular.z = 0

    cmd_vel.publish(msg)

rospy.init_node('motors')

rospy.Subscriber('/robot/cmd_vel', Twist, got_cmd_vel)

rospy.spin()
