#!/usr/bin/env python
import roslib; roslib.load_manifest('uml_hmm')
import rospy
import random

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

# laser is 360 deg in 2 deg increments (180 scans)
# 0 deg (index 0) is directly behind us
# index 45 is to our right
# index 90 is straight ahead
# index 135 is to our left

# maximum sum is 51
# minimum sum is 44.1856887341
# laser scans that see the wall are between 118 to 152

# scale this range so thresh is  44.18 = .10 
#                                51 = .9
# P(door) = (rand < thres)

WALL_RAW = 44.1856887341
DOOR_RAW = 120

reading = "foo"

def got_scan(msg):
    global reading

    raw= 0
    for i in range(118,152):
        raw+= msg.ranges[i]

    thresh = 0.1 + 0.8 * ((raw - WALL_RAW) / (DOOR_RAW - WALL_RAW))
    reading = "Wall" if (thresh< random.random()) else "Door"

def wall_door_sensor():
    global reading

    pub = rospy.Publisher('/robot/wall_door_sensor', String)
    rospy.init_node('wall_door_sensor')
    
    while not rospy.is_shutdown():
            rospy.loginfo(reading)
            pub.publish(String(reading))
            rospy.sleep(0.1)

rospy.Subscriber('/stage/base_scan', LaserScan, got_scan)
        

if __name__ == '__main__':
    try:
        wall_door_sensor()
    except rospy.ROSInterruptException: pass
