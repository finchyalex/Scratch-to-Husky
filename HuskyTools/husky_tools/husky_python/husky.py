import rospy
import time
import os
from geometry_msgs.msg import Twist
import datetime


class Husky:

    def __init__(self,BOUNDS_WIDTH,BOUNDS_HEIGHT,husky_ip):
        rospy.init_node('husky', anonymous=True)
        self.pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(200)
        self.BOUNDS_WIDTH = BOUNDS_WIDTH
        self.BOUNDS_HEIGHT = BOUNDS_HEIGHT
        self.ip = husky_ip

    
    def move(self,linear,angular):
        print("Moving")
        velocity = 0.2
        twist = Twist()
        if(linear < 0):
            twist.linear.x = -velocity
        else:
            twist.linear.x = velocity
        linear = abs(linear)
        twist.angular.z = angular
        for i in range(0,linear):
            self.pub.publish(twist)
            self.rate.sleep()
        twist.linear.x = 0
        twist.angular.z = 0
        self.pub.publish(twist)
        

    def moveTime(self,time,velocity):
        print("Moving")
        twist = Twist()
        twist.linear.x = velocity
        current_time = datetime.datetime.now()
        while((datetime.datetime.now() - current_time).total_seconds() < time):
            self.pub.publish(twist)
            self.rate.sleep()
        self.pub.publish(twist)


        
        