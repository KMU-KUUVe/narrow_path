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

#define CONST_STEER 0
#define CONST_SPEED 6
//#define DEBUG

namespace narrow_path{

class NarrowPath{
	public:
		NarrowPath();
		NarrowPath(ros::NodeHandle nh);
		void initSetup();
		void obstacle_cb(const obstacle_detector::Obstacles data);
		void run();
		void calculate_points();
		void publish();
	
		static bool cmp(const obstacle_detector::CircleObstacle a, const obstacle_detector::CircleObstacle b){
			return (a.center.x < b.center.x);
		}

	private:
		ros::NodeHandle nh_;
		ros::Publisher pub;
		ros::Subscriber sub;

		int steer;
		int speed;
		double mean_point_right_y;
		double mean_point_left_y;
		double mean_point_y;
		bool end_flag;

		vector<obstacle_detector::CircleObstacle> rava_circles;
		vector<obstacle_detector::CircleObstacle> right_circles;
		vector<obstacle_detector::CircleObstacle> left_circles;
		ackermann_msgs::AckermannDriveStamped msg;
};
}
