#!/usr/bin/env python
import rospy





class test:
	def __init__(self):
		rospy.init_node('test', anonymous=True)	
		self.num = 0
		self.n = 0

	def num_plus(self):
		while(self.n < 10):		
			self.num = self.num + 1
			self.n = self.n + 1			
			print(self.num)
			



if __name__ == '__main__':
	try: 
		test_ = test()
		
		while(test_.n < 8):
			rospy.spin()
		test_.num_plus()
		
	except rospy.ROSInterruptException:
		print(error)
		pass		
