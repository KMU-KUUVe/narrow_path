#!/usr/bin/env python 
import rospy
import math
import actionlib

from std_msgs.msg import String
from obstacle_detector.msg import Obstacles
from obstacle_detector.msg import SegmentObstacle
from geometry_msgs.msg import Point
from ackermann_msgs.msg import AckermannDriveStamped

from mission_planner.msg import MissionPlannerAction, MissionPlannerGoal, MissionPlannerResult, MissionPlannerFeedback


#front x +
#left y +
class narrow_path:
	def __init__(self):
		rospy.init_node('narrow_path', anonymous=True)
				
		self.pub = rospy.Publisher('ackermann', AckermannDriveStamped, queue_size=10)		

		self.server = actionlib.SimpleActionServer('narrow_path', MissionPlannerAction, execute_cb=self.execute_cb, auto_start=False)
		self.server.start()
	
		self.wayPoint = Point(1,0,0)
		
		self.count = [0]
		self.control_factor = rospy.get_param("/narrow_path/control_factor", 104)
		self.right_steer_scale = rospy.get_param("/narrow_path/right_steer_scale", 2.0)	
		self.throttle = rospy.get_param("/narrow_path/throttle", 0)
		self.stop_count= rospy.get_param("/narrow_path/stop_count", 100)
		self.start_distance = rospy.get_param("/narrow_path/start_distance", 1.0)
		self.end_distance = rospy.get_param("/narrow_path/end_distance", 1.0)
		self.approach_left_offset = rospy.get_param("/narrow_path/approach_left_offset", 7)

		self.approach_flag = False

		self.start_flag = False
		self.finish_flag = False
	
	def updateParam(self):
		self.control_factor = rospy.get_param("/narrow_path/control_factor")
		self.right_steer_scale = rospy.get_param("/narrow_path/right_steer_scale")	
		print("control_factor: " + str(self.control_factor))	
		print("right_steer_scale: " + str(self.right_steer_scale))
	
	def execute_cb(self, goal):
		rospy.loginfo("narrow execute_cb")
		self.sub = rospy.Subscriber('narrow_path_raw_obstacles', Obstacles, self.obstacles_cb)
		self.sub2 = rospy.Subscriber('narrow_path_approach_raw_obstacles', Obstacles, self.approach_cb)

		result = MissionPlannerResult()

		self.start_flag = True

		r = rospy.Rate(100)
		while not rospy.is_shutdown():
			if(self.finish_flag == True):
				self.approach_flag = False

				# FIXME: for test
				acker_data = AckermannDriveStamped()
				acker_data.drive.speed = 0
				acker_data.drive.steering_angle = 0	 
				rospy.loginfo("finish narrow path")
				self.pub.publish(acker_data) 

				self.server.set_succeeded(result)	
				break
			r.sleep()

	def narrow_pathing(self, data):
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
		#if detect segment, up start signal and start mission
		self.start_signal = 1
		print("during narrow mission")
		print("#######################################################")
		acker_data = AckermannDriveStamped()
		acker_data.drive.speed = self.throttle		
		steer_angle = math.atan(self.wayPoint.y/self.wayPoint.x)
		acker_data.drive.steering_angle = int(-(self.control_factor*steer_angle)/math.pi)
		if self.start_flag == True and acker_data.drive.steering_angle < 0:
			acker_data.drive.steering_angle = acker_data.drive.steering_angle - self.approach_left_offset

		if (acker_data.drive.steering_angle > 0):
			acker_data.drive.steering_angle = int(acker_data.drive.steering_angle/self.right_steer_scale)
		if (acker_data.drive.steering_angle > 26):
			acker_data.drive.steering_angle = 26
		elif (acker_data.drive.steering_angle < -26):
			acker_data.drive.steering_angle = -26
		print("speed : " + str(acker_data.drive.speed))
		print("steering : " + str(acker_data.drive.steering_angle))

		if not self.finish_flag:
			self.pub.publish(acker_data)



	def approach_cb(self, data):
		if self.start_flag == True:
			rospy.loginfo("approaching")
			self.narrow_pathing(data)

			nearest_x = 100.0
			for segment_data in data.segments:
				if nearest_x > segment_data.first_point.x:
					nearest_x = segment_data.first_point.x
				if nearest_x > segment_data.last_point.x:
					nearest_x = segment_data.last_point.x
			rospy.loginfo("nearest_x: %f"%nearest_x)

			if nearest_x < self.start_distance:
				self.start_flag = False
				self.approach_flag = True

	def obstacles_cb(self, data):
		if self.approach_flag == True:
			rospy.loginfo("narrow_pathing")
			self.narrow_pathing(data)

			farthest_x = 0
			for segment_data in data.segments:
				if farthest_x < segment_data.first_point.x:
					farthest_x = segment_data.first_point.x
				if farthest_x < segment_data.last_point.x:
					farthest_x = segment_data.last_point.x

			rospy.loginfo("farthest_x: %f"%farthest_x)
			if farthest_x < self.end_distance:
				self.finish_flag = True
			
		
		
if __name__ == '__main__':
	try:
		narrow_mission = narrow_path()
		
		rospy.spin()
	except rospy.ROSInterruptException:
		print(error)
		pass			
				

