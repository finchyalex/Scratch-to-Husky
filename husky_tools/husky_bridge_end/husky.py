import roslibpy
import time

class Husky:

    def __init__(self,HOST_IP,HOST_PORT,BOUNDS_WIDTH,BOUNDS_HEIGHT):

        self.husky_ros = roslibpy.Ros(host=HOST_IP, port=HOST_PORT)
        #Attempt to connect to the ros server
        print("Attempting to connect to: " + HOST_IP + ":" + str(HOST_PORT))
        try:
            self.husky_ros.run()
        except:
            print("Could not connect to ROS server")
            exit()
        if(self.husky_ros.is_connected):
            print("Connected to ROS server")
        #Create a publisher for the husky movement
        self.husky_movement_publisher = roslibpy.Topic(self.husky_ros, '/husky_velocity_controller/cmd_vel', 'geometry_msgs/Twist')
        self.husky_movement_publisher.advertise()
        #Create a subscriber for the husky odometry
        self.husky_odometry_subscriber = roslibpy.Topic(self.husky_ros, '/odometry/filtered', 'nav_msgs/Odometry')
        self.husky_odometry_subscriber.subscribe(self.odometry_callback)
        self.BOUDS_WIDTH = BOUNDS_WIDTH
        self.BOUNDS_HEIGHT = BOUNDS_HEIGHT
        #We will need some way to store the location and ensure it doesn't leave the bounds, maybe swap out my system for the Odom system later
        

    def move(self, distance):
        #We can only set the husky velocity we will need to do some math to figure out how long to move for
        #Lets make the husky move 1 meter per second

        time = distance
        #Create a message to send to the husky
        message = roslibpy.Message({
            'linear': {
                'x': 1,
                'y': 0,
                'z': 0
            },
            'angular': {
                'x': 0,
                'y': 0,
                'z': 0
            }
        })
        #Publish the message
        self.husky_movement_publisher.publish(message)
        #Wait for the husky to move
        time.sleep(time)
        #Stop the husky
        message = roslibpy.Message({
            'linear': {
                'x': 0,
                'y': 0,
                'z': 0
            },
            'angular': {
                'x': 0,
                'y': 0,
                'z': 0
            }
        })
        self.husky_movement_publisher.publish(message)


    def turn(self, angle):
        #We how to calculate how long to turn for
        #Lets make the husky turn 1 radian per second

        #Convert the angle to radians
        angle = angle * 0.0174533
        time = angle
        #Create a message to send to the husky
        message = roslibpy.Message({
            'linear': {
                'x': 0,
                'y': 0,
                'z': 0
            },
            'angular': {
                'x': 0,
                'y': 0,
                'z': 1
            }
        })
        #Publish the message
        self.husky_movement_publisher.publish(message)
        #Wait for the husky to move
        time.sleep(time)
        #Stop the husky
        message = roslibpy.Message({
            'linear': {
                'x': 0,
                'y': 0,
                'z': 0
            },
            'angular': {
                'x': 0,
                'y': 0,
                'z': 0
            }
        })
        self.husky_movement_publisher.publish(message)

    def setVelocity(self, linear, angular):
        #Create a message to send to the husky
        message = roslibpy.Message({
            'linear': {
                'x': linear,
                'y': 0,
                'z': 0
            },
            'angular': {
                'x': 0,
                'y': 0,
                'z': angular
            }
        })
        #Publish the message
        self.husky_movement_publisher.publish(message)

    def stop(self):
        #Create a message to send to the husky
        message = roslibpy.Message({
            'linear': {
                'x': 0,
                'y': 0,
                'z': 0
            },
            'angular': {
                'x': 0,
                'y': 0,
                'z': 0
            }
        })
        #Publish the message
        self.husky_movement_publisher.publish(message)

    def wait(self, time):
        time.sleep(time)