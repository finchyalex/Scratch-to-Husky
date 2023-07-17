import rospy
import time
import os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import datetime
import math
from tf.transformations import  euler_from_quaternion

class Husky:

    #TODO HUSKY SHELL WORKS FINE TO CONTROL HUSKY
    #HOWEVER, WHEN RUNNING FROM SCRATCH ISSUES ARISE

    def __init__(self,BOUNDS_WIDTH,BOUNDS_HEIGHT,husky_ip):
        rospy.init_node('husky', anonymous=True)
        self.pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(200)
        self.BOUNDS_WIDTH = BOUNDS_WIDTH
        self.BOUNDS_HEIGHT = BOUNDS_HEIGHT
        self.ip = husky_ip
        #Subscribe to the odometry topic
        self.odom_sub = rospy.Subscriber('/odometry/filtered', Odometry, self.odom_callback)
        self.odom = Odometry()
        self.rotation = 0

    def __del__(self):
        #Stop the husky when the program is ended
        twist = Twist()
        self.pub.publish(twist)
        #Remove the publisher and subscriber
        self.pub.unregister()
        self.odom_sub.unregister()

    #Callback for the odometry topic
    def odom_callback(self,msg):
        self.odom = msg0
        self.rotation = self.get_rotation(msg)

    def get_rotation(self,msg):
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        return yaw
    
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

    def MoveForward(self,distance):
        print("Moving")
        #Use Odometry to move forward
        #Move forward  for a certain distance
        distance_to_move = distance
        twist = Twist()
        twist.linear.x = 2
        current_x = self.odom.pose.pose.position.x
        current_y = self.odom.pose.pose.position.y
        #Move forward until the distance is reached
        while(distance_to_move > 0):
            self.pub.publish(twist)
            self.rate.sleep()
            distance_to_move = distance - math.sqrt((self.odom.pose.pose.position.x - current_x)**2 + (self.odom.pose.pose.position.y - current_y)**2)
            print(distance_to_move)
        twist.linear.x = 0
        self.pub.publish(twist)
        print("Done")

    def MoveBackward(self,distance):
        print("Moving")
        #Use Odometry to move backward
        #Move backward for a certain distance
        distance_to_move = distance
        twist = Twist()
        twist.linear.x = -2
        current_x = self.odom.pose.pose.position.x
        current_y = self.odom.pose.pose.position.y
        #Move backward until the distance is reached
        while(distance_to_move > 0):
            self.pub.publish(twist)
            self.rate.sleep()
            distance_to_move = distance - math.sqrt((self.odom.pose.pose.position.x - current_x)**2 + (self.odom.pose.pose.position.y - current_y)**2)
        twist.linear.x = 0
        self.pub.publish(twist)
        print("Done")



    def Rotate(self,angle): #Rotate the husky by a certain angle

        self.RotateConstant(angle)
        return
        #JUST FOR TESTING
        #Use the current angle and the target angle to calculate the angle to rotate
        #Use Odometry to rotate
        #Rotate until the angle is reached
        twist = Twist()
        vel = 0.5
        current_angle = self.rotation
        input_angle = angle*math.pi/180
        target_rad = current_angle + input_angle
        print("target={target_rad} current:{self.rotation}", target_rad,self.rotation)
        #Ensure the target angle is between -pi and pi
        if(target_rad > math.pi):
            target_rad = target_rad - 2*math.pi
        elif(target_rad < -math.pi):
            target_rad = target_rad + 2*math.pi
        res = 0.1
        print("target={target_rad} current:{self.rotation}", target_rad,self.rotation)

        while not rospy.is_shutdown():
            #quat = quaternion_from_euler (roll, pitch,yaw)
            #print quat
            twist.angular.z = vel * (target_rad-self.rotation)
            self.pub.publish(twist)

            self.rate.sleep()
        
        twist.angular.z = 0
        self.pub.publish(twist)
        print("Done")

    def RotateConstant(self,angle):
        #This is used to rotate at a constant speed
        print("Rotating")
        twist = Twist()
        vel = 1
        current_angle = self.rotation
        input_angle = angle*math.pi/180
        target_rad = current_angle + input_angle
        #Our target can't be more than 2pi or less than -2pi
        if(target_rad > math.pi):
            target_rad = target_rad - 2*math.pi
        elif(target_rad < -math.pi):
            target_rad = target_rad + 2*math.pi
        res = 0.001
        #Ensure the target angle is between -pi and pi
        

        while not rospy.is_shutdown():
            if(target_rad-self.rotation < res):
                break
            #quat = quaternion_from_euler (roll, pitch,yaw)
            #print quat
            twist.angular.z = vel
            self.pub.publish(twist)
            print("taeget={} current:{}", target_rad,self.rotation)
            self.rate.sleep()

            
    def wait(self,time):
        #Wait for a certain amount of time
        time.sleep(time)

        
        