#include "narrow_path_action.h"
//#include <actionlib/server/simple_action_server.h>
//#include <action_with_smach/MissionPlannerAction.h>

int main(int argc, char* argv[]) {
	ros:: init(argc, argv, "narrow_path_node");
	narrow_path_action::NarrowPathAction node("narrow_path");
	ros::spin();

	cout << "node start" << endl;
	//ros::Subscriber sub = nh.subscribe("raw_obstacles", 1, obstacle_cb);
	//pub = nh.advertise<ackermann_msgs::AckermannDriveStamped> ("ackermann", 100);
	//pub = nh.advertise<std_msgs::String>("write", 1000);
	//ros::spin();
}
