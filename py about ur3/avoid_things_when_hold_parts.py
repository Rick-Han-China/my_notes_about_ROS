#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
#adding objects in virtual world and avoid them when holding parts automatically

import rospy, sys
import thread, copy
import moveit_commander
from moveit_commander import RobotCommander, MoveGroupCommander, PlanningSceneInterface
from geometry_msgs.msg import PoseStamped, Pose
from moveit_msgs.msg import CollisionObject, AttachedCollisionObject, PlanningScene
from math import radians
from copy import deepcopy

class MoveAttachedObjectDemo:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        
        rospy.init_node('moveit_attached_object_demo')
        
        # initialize scene
        scene = PlanningSceneInterface()
        rospy.sleep(1)
                                
        arm = MoveGroupCommander('manipulator')
        
        end_effector_link = arm.get_end_effector_link()
        
        arm.set_goal_position_tolerance(0.1)
        arm.set_goal_orientation_tolerance(0.05)
       
        arm.allow_replanning(True)
        arm.set_planning_time(10)

       	joint_positions = [0, -1.57, -1.57, -1.57, 1.57, 0]
        arm.set_joint_value_target(joint_positions)
        arm.go()
        
        # remove objects in last run
        scene.remove_attached_object(end_effector_link, 'tool')
        scene.remove_world_object('table') 
        scene.remove_world_object('target')

        # set height of table
        table_ground = -0.85
        
        # set sizes of table、tool、pillar
        table_size = [0.84, 0.84, 0.85]
        tool_size = [0.232, 0.232, 0.226]
        
        # get pose position and orientation of tool
        p = PoseStamped()
        p.header.frame_id = end_effector_link
        
        p.pose.position.x = 0.116 # tool_size[0] / 2.0 - 0.025
        p.pose.position.y = 0
        p.pose.position.z = 0
        p.pose.orientation.x = 0
        p.pose.orientation.y = 0
        p.pose.orientation.z = 0
        p.pose.orientation.w = 1
        
        # attach tool to the end of robot
        scene.attach_box(end_effector_link, 'tool', p, tool_size)

        # add table to world
        table_pose = PoseStamped()
        table_pose.header.frame_id = 'base_link'
        table_pose.pose.position.x = 0.0
        table_pose.pose.position.y = -0.515
        table_pose.pose.position.z = -0.425 # table_ground + table_size[2] / 2.0
        table_pose.pose.orientation.w = 1.0
        scene.add_box('table', table_pose, table_size)
        
        rospy.sleep(2)  

        # add pillar
        pillar_pose = PoseStamped()
        pillar_pose.header.frame_id = 'base_link'
        pillar_pose.pose.position.x = 0.0
        pillar_pose.pose.position.y = 0.0
        pillar_pose.pose.position.z = -0.425
        table_pose.pose.orientation.w = 1.0
        scene.add_box('pillar', pillar_pose, pillar_size)
        
        rospy.sleep(2)  

        # update pose
        arm.set_start_state_to_current_state()

        # set target position
        joint_positions = [0.827228546495185, 0.29496592875743577, 1.1185644936946095, -0.7987583317769674, -0.18950024740190782, 0.11752152218233858]
        arm.set_joint_value_target(joint_positions)
                 
        arm.go()
        rospy.sleep(1)
        
        arm.set_named_target('home')
        arm.go()


        joint_positions = [0, -1.57, -1.57, -1.57, 1.57, 0]
        arm.set_joint_value_target(joint_positions)
                 
        arm.go()
        rospy.sleep(1.5)

        joint_positions = [0.827228546495185, 0.29496592875743577, 1.1185644936946095, -0.7987583317769674, -0.18950024740190782, 0.11752152218233858]
        arm.set_joint_value_target(joint_positions)
                 
        arm.go()
        rospy.sleep(1)
        
        arm.set_named_target('home')
        arm.go()



        moveit_commander.roscpp_shutdown()
        moveit_commander.os._exit(0)

if __name__ == "__main__":
    MoveAttachedObjectDemo()

    
