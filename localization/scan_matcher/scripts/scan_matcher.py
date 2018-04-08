#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import tf.transformations
import tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from copy import copy
import numpy as np
import os
from keras.models import model_from_json
from keras.callbacks import ModelCheckpoint
import math
import os.path, time

#LOAD NETWORK
netname="ScanMatchin"
if not os.path.isfile(netname+'.h5') or not os.path.isfile(netname+'.json'):
   print('Nothing to load')
else:
    print('Loading existing network')
    model = model_from_json(open(netname+'.json').read())
    model.load_weights(netname+'.h5')
    model.compile(loss='mse',optimizer='adam')
weights= netname+'.h5'


FLaser= []
BLaser= []


def Fcallback(Dvalue):
    global FLaser
    FLaser =copy(Dvalue.ranges)

def Bcallback(Dvalue):
    global BLaser
    BLaser=copy(Dvalue.ranges)


def AngleN(tValue):

    while tValue<-math.pi:
	    tValue = tValue + 2*math.pi
    while tValue> math.pi:
	    tValue = tValue - 2*math.pi
    return tValue

def both():
    global FLaser
    global BLaser
    global model
    pub = rospy.Publisher('scan_matcher_pose', PoseStamped, queue_size=1)
    pub_contour = rospy.Publisher('scan_matcher_contour', Marker, queue_size=1)
    rospy.init_node('scan_matcher', anonymous=True)
    rospy.Subscriber('scan_front', LaserScan, Fcallback)
    rospy.Subscriber('scan_rear', LaserScan, Bcallback)
    rate = rospy.Rate(10) 
    rospy.sleep(2.)
    time_last_update = rospy.Time.now()
    update_weights_freq= rospy.Duration(10).to_sec()
    init_net=os.path.getmtime(weights)

    while not rospy.is_shutdown():
        diff_time=rospy.Time.now()-time_last_update

        if(diff_time.to_sec()>=update_weights_freq and init_net!=os.path.getmtime(weights)):
            init_net=os.path.getmtime(weights)
            print('Loading network')
            model = model_from_json(open(netname+'.json').read())
            model.load_weights(weights)
            model.compile(loss='mse', optimizer='adam')
            time_last_update = rospy.Time.now()

        Dvalue = np.hstack((  BLaser,  FLaser))
        X_test=np.reshape(Dvalue , (1, 362))
        predicted_output = model.predict(X_test, batch_size=1)
        pValue=PoseStamped()
        pValue.header.frame_id = "/map";
        pValue.pose.position.x= predicted_output[0][0]
        pValue.pose.position.y= predicted_output[0][1]
        tValue =  AngleN(predicted_output[0][2])
        quat=tf.transformations.quaternion_from_euler(0,0,tValue)
        pValue.pose.orientation.z=quat[2]
        pValue.pose.orientation.w=quat[3] 
        pub.publish(pValue)   
        
        mValue = Marker()
        mValue.header.frame_id = "/map"
        mValue.header.stamp =rospy.Time(0)
        mValue.id = 1
        mValue.type =Marker.LINE_STRIP
        mValue.action =Marker.ADD

        mValue.color.a = 1.0
        mValue.color.r = 1.0
        mValue.color.g = 0.0
        mValue.color.b = 0.0
 
        mValue.scale.x = 0.025
        mValue.scale.y = 0.025
        mValue.scale.z = 0.025

        point1=Point()
        point1.x = np.cos(tValue)* (-0.5) -np.sin(tValue)*(-0.55) +pValue.pose.position.x
        point1.y = np.sin(tValue)*(-0.5)+np.cos(tValue)*(-0.55)+ pValue.pose.position.y
        mValue.points.append(point1);
        point2=Point()
        point2.x = np.cos(tValue)* (-0.5) -np.sin(tValue)*(0.55) +pValue.pose.position.x
        point2.y = np.sin(tValue)*(-0.5)+np.cos(tValue)*(0.55)+ pValue.pose.position.y
        mValue.points.append(point2);
        point3=Point()
        point3.x = np.cos(tValue)* (1.75) -np.sin(tValue)*(0.55) +pValue.pose.position.x
        point3.y = np.sin(tValue)*(1.75)+np.cos(tValue)*(0.55)+ pValue.pose.position.y
        mValue.points.append(point3);
        point4=Point()
        point4.x = np.cos(tValue)* (1.75) -np.sin(tValue)*(-0.55) +pValue.pose.position.x
        point4.y = np.sin(tValue)*(1.75)+np.cos(tValue)*(-0.55)+ pValue.pose.position.y
        mValue.points.append(point4);
        point5=Point()
        point5.x = np.cos(tValue)* (-0.5) -np.sin(tValue)*(-0.55) +pValue.pose.position.x
        point5.y = np.sin(tValue)*(-0.5)+np.cos(tValue)*(-0.55)+ pValue.pose.position.y
        mValue.points.append(point5);

        pub_contour.publish(mValue)
    rospy.spin()

if __name__ == '__main__':
     print('Start processing')
     both()
