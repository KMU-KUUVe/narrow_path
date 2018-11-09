#!/usr/bin/env python
import rospy
import actionlib

from mission_planner.msg import MissionPlannerAction, MissionPlannerGoal, MissionPlannerResult, MissionPlannerFeedback
from narrow_path import narrow_path


def execute_cb(goal):
	rospy.loginfo("Goal Received")
	result = MissionPlannerResult()
	narrow_path_mission = narrow_path()
	action_server.set_succeeded(result)


if __name__ == '__main__':
    rospy.init_node('narrow_path', anonymous=True)
    try:
        action_name = 'narrow_path'
        action_server = actionlib.SimpleActionServer(action_name, 		MissionPlannerAction, execute_cb=execute_cb, auto_start=False)
        action_server.start()
        rospy.spin()
    except rospy.ROSInterruptException:
        print(error)
	pass
