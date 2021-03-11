#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose
from copy import deepcopy

class MoveItCartesianDemo:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)

        rospy.init_node('moveit_cartesian_demo', anonymous=True)

        # enable using planning in  cartesian space
        cartesian = rospy.get_param('~cartesian', True)
                      
        arm = MoveGroupCommander('manipulator')
        
        arm.allow_replanning(True)
        
        arm.set_pose_reference_frame('base_link')
                
        arm.set_goal_position_tolerance(0.001)
        arm.set_goal_orientation_tolerance(0.001)
        
        arm.set_max_acceleration_scaling_factor(0.2)
        arm.set_max_velocity_scaling_factor(0.2)
        
        end_effector_link = arm.get_end_effector_link()

       	joint_positions = [0, -1.57, -1.57, -1.57, 1.57, 0]
        arm.set_joint_value_target(joint_positions)
        arm.go()
        rospy.sleep(1)
                                               
        start_pose = arm.get_current_pose(end_effector_link).pose

        waypoints = []

        # add start pose to waypoints list
        if cartesian:
            waypoints.append(start_pose)
        
	# let the end_link go 0.1m on -z
        wpose = deepcopy(start_pose)
        wpose.position.z -= 0.1

        if cartesian:
            waypoints.append(deepcopy(wpose))
        else:
            arm.set_pose_target(wpose)
            arm.go()
            rospy.sleep(1)

        wpose.position.x += 0.15

        if cartesian:
            waypoints.append(deepcopy(wpose))
        else:
            arm.set_pose_target(wpose)
            arm.go()
            rospy.sleep(1)
        
        wpose.position.y += 0.15

        if cartesian:
            waypoints.append(deepcopy(wpose))
        else:
            arm.set_pose_target(wpose)
            arm.go()
            rospy.sleep(1)

        wpose.position.x -= 0.15
        wpose.position.y -= 0.15

        if cartesian:
            waypoints.append(deepcopy(wpose))
        else:
            arm.set_pose_target(wpose)
            arm.go()
            rospy.sleep(1)

        if cartesian:
		fraction = 0.0  
		maxtries = 100   
		attempts = 0     
		
		arm.set_start_state_to_current_state()
	 
		while fraction < 1.0 and attempts < maxtries:
		    (plan, fraction) = arm.compute_cartesian_path (
		                            waypoints,   
		                            0.01,        
		                            0.0,         
		                            True)        

		    attempts += 1
		    

		    if attempts % 10 == 0:
		        rospy.loginfo("Still trying after " + str(attempts) + " attempts...")
		             

		if fraction == 1.0:
		    rospy.loginfo("Path computed successfully. Moving the arm.")
		    arm.execute(plan)
		    rospy.loginfo("Path execution complete.")

		else:
		    rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")  

		rospy.sleep(1)

       	joint_positions = [0, -1.57, -1.57, -1.57, 1.57, 0]
        arm.set_joint_value_target(joint_positions)
        arm.go()
        rospy.sleep(1)
        
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

if __name__ == "__main__":
    try:
        MoveItCartesianDemo()
    except rospy.ROSInterruptException:
        pass
