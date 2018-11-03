#!/usr/bin/env python
import rospy
import math

from std_msgs.msg import String
from obstacle_detector.msg import Obstacles
from obstacle_detector.msg import SegmentObstacle
from geometry_msgs.msg import Point
from ackermann_msgs.msg import AckermannDriveStamped

#front x +
#left y +
class narrow_path:
	def __init__(self):
		self.pub = rospy.Publisher('ackermann', AckermannDriveStamped, queue_size=10)		
		self.sub = rospy.Subscriber('raw_obstacles', Obstacles, self.obstacles_cb)
		rospy.init_node('narrow_path', anonymous=True)	
		self.wayPoint = Point(1,0,0)
		self.control_factor = rospy.get_param("/narrow_path/control_factor", 104)
		self.right_steer_scale = rospy.get_param("/narrow_path/right_steer_scale", 2.0)	
		self.throttle = rospy.get_param("/narrow_path/throttle", 0)	
		self.end_signal = 0
                self.start_signal = 0 	
	def updateParam(self):
		self.control_factor = rospy.get_param("/narrow_path/control_factor")
		self.right_steer_scale = rospy.get_param("/narrow_path/right_steer_scale")	
		print("control_factor: " + str(self.control_factor))	
		print("right_steer_scale: " + str(self.right_steer_scale))
	def obstacles_cb(self, data):
		self.updateParam()
		
		x_center = 0
		y_center = 0
		#find wayPoint 
		for segment_data in data.segments:
			x_center = x_center + segment_data.first_point.x
			x_center = x_center + segment_data.last_point.x
			y_center = y_center + segment_data.first_point.y
			y_center = y_center + segment_data.last_point.y
		x_center = x_center/len(data.segments)
		y_center = y_center/len(data.segments)
		self.wayPoint = Point(x_center,y_center,0)
               
		print(self.wayPoint)
		#if not detect segment go front
		if ((self.wayPoint.x == 0) and (self.end_signal == 0)): 
			print("anything detection!! mission not start")
			acker_data = AckermannDriveStamped()
			acker_data.drive.speed = self.throttle 
			acker_data.drive.steering_angle = 0	 
			print("speed : " + str(acker_data.drive.speed))
			print("steering : " + str(acker_data.drive.steering_angle))
			self.pub.publish(acker_data)      
			#continue
		#check	
		else:
			#if detect segment, up start signal and start mission
			self.start_signal = 1
			print("during narrow mission")
			print("#######################################################")
			acker_data = AckermannDriveStamped()
			acker_data.drive.speed = self.throttle		
			steer_angle = math.atan(self.wayPoint.y/self.wayPoint.x)
			acker_data.drive.steering_angle = int(-(self.control_factor*steer_angle)/math.pi)
			if (acker_data.drive.steering_angle > 0):
				acker_data.drive.steering_angle = int(acker_data.drive.steering_angle/self.right_steer_scale)
			if (acker_data.drive.steering_angle > 26):
				acker_data.drive.steering_angle = 26
			elif (acker_data.drive.steering_angle < -26):
				acker_data.drive.steering_angle = -26
			print("speed : " + str(acker_data.drive.speed))
			print("steering : " + str(acker_data.drive.steering_angle))
			self.pub.publish(acker_data)
			if (self.wayPoint.x == 0):
				self.end_signal = 1
		                print("end signal is 1. finish narrow path mission!!")
				print("##################################################")
		
		
if __name__ == '__main__':
	try:
		narrow_mission = narrow_path()
		
		while((narrow_mission.end_signal != 1) and (narrow_mission.start_signal != 1)):
			rospy.spin()
		
	except rospy.ROSInterruptException:
		print(error)
		pass			
				
	
