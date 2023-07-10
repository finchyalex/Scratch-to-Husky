import rospy
import time
from geometry_msgs.msg import Twist


class Husky:

    def __init__(self,BOUNDS_WIDTH,BOUNDS_HEIGHT):
        rospy.init_node('husky', anonymous=True)
        self.pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10) # 10hz
        self.BOUNDS_WIDTH = BOUNDS_WIDTH
        self.BOUNDS_HEIGHT = BOUNDS_HEIGHT
    
    def move(self,linear,angular):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.pub.publish(twist)
        for i in range(0,10):
            self.pub.publish(twist)

        
        