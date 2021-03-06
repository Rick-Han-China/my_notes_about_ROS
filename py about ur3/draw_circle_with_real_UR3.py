#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, sys
import moveit_commander
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose, PoseStamped
from copy import deepcopy

import math
import numpy

class MoveItCircleDemo:
    def __init__(self):
        # initialize move_group API
        moveit_commander.roscpp_initialize(sys.argv)

        # initialize node
        rospy.init_node('moveit_clrcle_demo', anonymous=True)
                        
        # initialize arm group in move group
        arm = MoveGroupCommander('manipulator')
        
        # enable replanning
        arm.allow_replanning(True)
        
        # set frame
        reference_frame = 'base_link'
        arm.set_pose_reference_frame('base_link')
                
        # set error tolerance
        arm.set_goal_position_tolerance(0.001)
        arm.set_goal_orientation_tolerance(0.001)
        
        # set scaling_factor of acceleration and velocity
        arm.set_max_acceleration_scaling_factor(1)
        arm.set_max_velocity_scaling_factor(1)
        
        # get eef
        end_effector_link = arm.get_end_effector_link()

        # go to a start position you like
        joint_positions = [0, -1.57, -1.57, -1.57, 1.57, 0]
        arm.set_joint_value_target(joint_positions)
	arm.go()
        rospy.sleep(1)
                                               
	#target_pose is center of a circle
        target_pose = PoseStamped()
        target_pose.header.frame_id = reference_frame
        target_pose.header.stamp = rospy.Time.now()     
        target_pose.pose.position.x = -0.298775992708
        target_pose.pose.position.y = 0.11217155461
        target_pose.pose.position.z = 0.313829003447
        target_pose.pose.orientation.x = -0.706809527727
        target_pose.pose.orientation.y = -0.000946885614452
        target_pose.pose.orientation.z = 0.707403270153
        target_pose.pose.orientation.w = 9.11041120084e-05
        
        # set target and go
        arm.set_pose_target(target_pose, end_effector_link)
        arm.go()

        # waypoints list
        waypoints = []
                
        # ????????????????????????????????????
        waypoints.append(target_pose.pose)

        centerA = target_pose.pose.position.x
        centerB = target_pose.pose.position.y
        radius = 0.1
		
	#after testinf on real UR3???0.00013rad is the smallest step I can achieve
        for th in numpy.arange(0, 6.28, 0.005):
            target_pose.pose.position.x = centerA + radius * math.cos(th)
            target_pose.pose.position.y = centerB + radius * math.sin(th)
            wpose = deepcopy(target_pose.pose)
            waypoints.append(deepcopy(wpose))

            #print('%f, %f' % (Y, Z))

        fraction = 0.0   # rate
        maxtries = 100   # 100 times to try
        attempts = 0     # number of attempts already made
        
        arm.set_start_state_to_current_state()
 
        # trying planning a road in cartesian space  
        while fraction < 1.0 and attempts < maxtries:
            (plan, fraction) = arm.compute_cartesian_path (
                                    waypoints,
                                    0.01,        # eef_step
                                    0.0,         # jump_threshold
                                    True)        # enalbe avoid_collisions
            
            attempts += 1
            
            # print information when planning
            if attempts % 10 == 0:
                rospy.loginfo("Still trying after " + str(attempts) + " attempts...")
                     
        # if success, run the robot
        if fraction == 1.0:
            rospy.loginfo("Path computed successfully. Moving the arm.")
            arm.execute(plan)
            rospy.loginfo("Path execution complete.")
        # print information if fails
        else:
            rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")  

        rospy.sleep(1)

        # return home pose
        #arm.set_named_target('home')
        #arm.go()
        #rospy.sleep(1)
        
        # quit
        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

if __name__ == "__main__":
    try:
        MoveItCircleDemo()
    except rospy.ROSInterruptException:
        pass
