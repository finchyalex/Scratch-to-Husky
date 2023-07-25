import rospy
import time
import os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import datetime
import math
from tf.transformations import  euler_from_quaternion

class Husky:


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
        self.last_odem = Odometry()
        self.rotation = 0
        self.expected_rotation = 0
        self.expected_x = None
        self.expected_y = None
        self.inital_x = None
        self.inital_y = None
        #Code for Bounds
        self.max_x = None
        self.max_y = None
        self.min_x = None
        self.min_y = None
        #Code to see if Husky is moving
        self.is_moving = False
        self.was_moving = False

        #Add a system to adjust the rotation of the husky

    

    def __del__(self):
        #Stop the husky when the program is ended
        twist = Twist()
        self.pub.publish(twist)
        #Remove the publisher and subscriber
        self.pub.unregister()
        self.odom_sub.unregister()

    #Callback for the odometry topic
    def odom_callback(self,msg):
        self.last_odem = self.odom
        self.odom = msg
        self.rotation = self.get_rotation(msg)

        if(self.inital_x == None):
            self.inital_x = msg.pose.pose.position.x
            self.inital_y = msg.pose.pose.position.y
            #Using this and our bounds, we can determine the max x and y values
            self.max_x = self.inital_x + self.BOUNDS_WIDTH/2
            self.max_y = self.inital_y + self.BOUNDS_HEIGHT/2
            self.min_x = self.inital_x - self.BOUNDS_WIDTH/2
            self.min_y = self.inital_y - self.BOUNDS_HEIGHT/2

        #Check if the husky is moving by comparing the current position to the last position
        #There will be a certain amount of error
        #If the error is too small, we can assume the husky is not moving

        error = 0.001
        if(abs(self.odom.pose.pose.position.x - self.last_odem.pose.pose.position.x) < error and abs(self.odom.pose.pose.position.y - self.last_odem.pose.pose.position.y) < error):
            self.is_moving = False
        else:
            self.is_moving = True
        



    def PremovementCheck(self,distance):
        #Get the husky position
        #We can use the square root of the sum of the squares of the x and y coordinates to get the distance

        current_pos = self.odom.pose.pose.position
        current_x = current_pos.x
        current_y = current_pos.y

        #End Location
        end_x = current_x + distance*math.cos(self.rotation)
        end_y = current_y + distance*math.sin(self.rotation)

        #Check if the end location is out of bounds
        if(end_x > self.max_x or end_x < self.min_x or end_y > self.max_y or end_y < self.min_y):
            return False
        else:
            return True

        #Get the distance from the inital position
        
        #See if the distance in that direction would take us out of bounds

    def MovementHandler(self,distance,rotation,wait_time=10):

        #Wait time in milliseconds
        #Check if the husky is moving
        while(self.is_moving):
            self.rate.sleep()
        #Check if the movement is valid
        #This should block the main thread until the movement is complete
            
        



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
        
    #Move the husky for a certain amount of time at a certain velocity
    def moveTime(self,time,velocity):
        print("Moving")
        twist = Twist()
        twist.linear.x = velocity
        current_time = datetime.datetime.now()
        while((datetime.datetime.now() - current_time).total_seconds() < time):
            self.pub.publish(twist)
            self.rate.sleep()
        self.pub.publish(twist)


    #Move the husky forwards a certain distance
    def MoveForward(self,distance):
        self.MovementHandler(distance,0)
        print("Moving")
        #Use Odometry to move forward
        #Move forward  for a certain distance
        distance_to_move = distance
        twist = Twist()
        twist.linear.x = 2
        min_vel = 0.1
        current_x = self.odom.pose.pose.position.x
        current_y = self.odom.pose.pose.position.y

        #Calculate our expected x and y
        self.expected_x = current_x + distance*math.cos(self.rotation)
        self.expected_y = current_y + distance*math.sin(self.rotation)
        #TODO Finish writing a system to adjust the rotation and location of the husky when it is not moving

        #Move forward until the distance is reached
        #Should probably add a magnitude to the velocity, it's okay for now
        while(distance_to_move > 0):
            twist.linear.x = 2 * distance_to_move
            if(twist.linear.x < min_vel):
                twist.linear.x = min_vel
            self.pub.publish(twist)
            self.rate.sleep()
            distance_to_move = distance - math.sqrt((self.odom.pose.pose.position.x - current_x)**2 + (self.odom.pose.pose.position.y - current_y)**2)
            os.system('clear')
            print("Moving Forward")
            print("Remaining Distance: " + str(distance_to_move))
        twist.linear.x = 0
        self.pub.publish(twist)
        print("Done")

    #Move the husky forwards a certain distance
    def MoveBackward(self,distance):
        self.MovementHandler(distance,0)
        print("Moving")
        #Use Odometry to move backward
        #Move backward for a certain distance
        distance_to_move = distance
        twist = Twist()
        twist.linear.x = -2
        min_vel = -0.1
        current_x = self.odom.pose.pose.position.x
        current_y = self.odom.pose.pose.position.y
        #Move backward until the distance is reached
        while(distance_to_move > 0):
            #Slow down when we are close to the target
            twist.linear.x = -2 * distance_to_move
            if(twist.linear.x > min_vel):
                twist.linear.x = min_vel
            self.pub.publish(twist)
            self.rate.sleep()
            distance_to_move = distance - math.sqrt((self.odom.pose.pose.position.x - current_x)**2 + (self.odom.pose.pose.position.y - current_y)**2)
            #Clear the screen
            os.system('clear')
            print("Moving Backward")
            print("Remaining Distance: " + str(distance_to_move))
        twist.linear.x = 0
        self.pub.publish(twist)
        print("Done")



    def Rotate(self,angle): #Rotate the husky by a certain angle
        self.MovementHandler(0,angle)
        self.RotateConstant(angle)
        return #This function is not used yet just for testing
        #JUST FOR TESTING
        #Use the current angle and the target angle to calculate the angle to rotate
        #Use Odometry to rotate
        #Rotate until the angle is reached
        twist = Twist()
        vel = 0.5
        current_angle = self.rotation
        input_angle = angle*math.pi/180
        target_rad = current_angle + input_angle        #Ensure the target angle is between -pi and pi
        if(target_rad > math.pi):
            target_rad = target_rad - 2*math.pi
        elif(target_rad < -math.pi):
            target_rad = target_rad + 2*math.pi
        res = 0.1
        print("target=" + target_rad, " rotation=" + self.rotation)

        while not rospy.is_shutdown():
            #quat = quaternion_from_euler (roll, pitch,yaw)
            #print quat
            twist.angular.z = vel * (target_rad-self.rotation)
            self.pub.publish(twist)

            self.rate.sleep()
        
        twist.angular.z = 0
        self.pub.publish(twist)
        print("Done")


    def RotateTo(self,angle):
        pass

    def RotateConstant(self,angle):
        #This is used to rotate and will slow down when it gets close to the target angle
        print("Rotating")
        twist = Twist()
        vel = 1
        #Depending on the angle, we need to rotate clockwise or counterclockwise
        vel_magnitude = 0
        if(angle > 0):
            vel_magnitude = vel
        else:
            vel_magnitude = -vel
        #Use Odometry to rotate
        current_angle = self.rotation
        input_angle = angle*math.pi/180
        target_rad = current_angle + input_angle
        self.expected_rotation = target_rad
        #Our target can't be more than 2pi or less than -2pi
        if(target_rad > math.pi):
            target_rad = target_rad - 2*math.pi
        elif(target_rad < -math.pi):
            target_rad = target_rad + 2*math.pi
        res = 0.01
        #0.01 radians is about 0.5 degrees
        min_vel = 0.3
        print(f"Our target is {target_rad} and our current angle is {self.rotation}")
        #Ensure the target angle is between -pi and pi
        

        while not rospy.is_shutdown():
            print(f"target={target_rad} current:{self.rotation}")
            #We need to stop the spinning when we reach the target angle
            #Perhaps start slowing down when we are close to the target angle
            twist.angular.z = vel * abs(target_rad-self.rotation) * vel_magnitude
            if(twist.angular.z < abs(min_vel)):
                twist.angular.z = min_vel * vel_magnitude


            if(abs(target_rad-self.rotation) < res):
                twist.angular.z = 0
                self.pub.publish(twist)
                break

            #quat = quaternion_from_euler (roll, pitch,yaw)
            #print quat

            self.pub.publish(twist)
            self.rate.sleep()

            
    def wait(self,time):
        #Wait for a certain amount of time
        time.sleep(time)

        
        