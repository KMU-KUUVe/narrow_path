#include <ros/ros.h>

//#include <std_msgs/String.h>
#include <obstacle_detector/Obstacles.h>
#include <obstacle_detector/CircleObstacle.h>
#include <sensor_msgs/PointCloud2.h>
#include <geometry_msgs/Point.h>
#include <ackermann_msgs/AckermannDriveStamped.h>

#include <algorithm>
#include <stdlib.h>
#include <math.h>
#include <vector>
//#include <string>

using namespace std;

#define CONST_STEER 0;
#define CONST_SPEED 0;

namespace narrow_path{

class Narrow{
	public:
		NarrowPath();
		NarrowPath(ros::NodeHandle nh);
		void initSetup();
		void obstacle_cb(const obstacle_detector::Obstacles data);
	
		bool cmp(const obstacle_detector::CircleObstacle a, const obstacle_detector::CircleObstacle b);

	private:
		ros::NodeHandle nh;
		ros::Publisher pub;
		//ros::Subscriber sub = nh.subscribe("raw_obstacles", 1, obstacle_cb);
		//ros::Publisher pub = nh.advertise<ackermann_msgs::AckermannDriveStamped> ("ackermann", 100);
		int steer, speed;
		double mean_point_right_y, mean_point_left_y, mean_point_y;
		vector<obstacle_detector::CircleObstacle> right_circles;
		vector<obstacle_detector::CircleObstacle> left_circles;
};

		return (a.center.x < b.center.x);
}

}
