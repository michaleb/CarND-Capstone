## CarND-Capstone Project
### Self-Driving Car Engineer Nanodegree Program

[//]: # (Image References)

[image1]:./imgs/capstone_ros_graph.png "ROS topics - Car sub-systems"

### Team7 - members

|Name                       	|Submission email         |
|:------------------------------|:------------------------|
|Michale Bailey             	|                         | 
|Wenhan Yang (Team Lead)       	| wenhan_yuan@hotmail.com |   
|Qianqiao Zhang             	| zhangqianqiao@outlook.com|
|Simon Miyingo              	|simonpetermiyingo@gmail.com| 

## Introduction

The two term SDCND program that commenced in October 2018 culminated with members of this cohort working in teams to tackle the capstone project of programming a real self driving car. The aim is to have the car follow waypoints along a track in a simulator travelling within a given speed limit and to make adjustments to the velocity component of those waypoints to gradually bring the car to a full stop at the stopline of the closest red traffic light observed ahead. The car would have successfully complete 1 lap around the track if it observed the speed limit and behaved according to the state of the traffic lights it encountered.

The task of programming all the systems of a Self-Driving car, in such a small timeframe,  would be quite daunting and so the requirements given to us were relagated to writing code for only three of the car's sub-systems as outlined in the diagram below.

The inter-communication between the car's sub-systems is acheived using the Robot Operating System (ROS) topics, this was my introduction to ROS and so I had to go from 0 -> 60 pretty quickly *(which generated some amount of Jerk)*. 

![alt text][image1]

## Overview

For the project of interest are the Perception, Planning and Control subsystems. In this implementation the focus was on the traffic light detection node in the Perception subsystem, the waypoint updater node in the Planning subsystem and the Drive by wire (DBW) node of the Control subsystem.

**1.** In the **Perception** subsystem only traffic lights were observed. The traffic light detection node consists of a traffic light detector module (tl_detector) and traffic light classifier module (tl_classifer).

subscribes to : **/base_waypoints**, **/current_pose**, **/image_color**
publishes to : **/traffic_waypoint** 

I implemented the 'process_traffic_light' method of the tl_detector and it uses the car's current position to determine which base_waypoints are closest to the car and subsequently determines, from a list of traffic light coordinates, which traffic light is closest and ahead of the car. Once this is ascertained the tl_classifier executes the clasification of the images from the **/image_color** messages to obtain the color of the traffic light and if it is RED publishes its waypoint index. The tl_classifier was implemented using SSD and was done by Qianqiao and Wenhan (Team Lead).				

**2.** The **Planning** subsystem provides the trajectory for the car to follow, it comprises the waypoint loader and the waypoint updater nodes.

The waypoint loader node has no subscribers and only publishes to: **/base_waypoints**

These base_waypoints are published once and are all the waypoints for the given track. They comprise of (x, y, z) coordinates of points on the track and the velocity and heading (yaw) the car should maintain at those points or locations.

The waypoint updater node

subscribes to: **/base_waypoints**, **/current_pose** and **/traffic_waypoints**
publishes to: **/final_waypoints**

I also implemented this node and it updates the velocity component of the base waypoints based on traffic light conditions. If the closest traffic light ahead of the car is showing RED then the velocities of all base waypoints between the car's current position up to the LOOKAHEAD_WPS limit will be altered to facilitate the deceleration of the car to 0 m/s at the stopline. Any other traffic light condition and the car will travel at the reference velocities of these base waypoints.

There are two main functions in the node, 'generate_lane' and 'decelerate_waypoints'. Once the closest waypoint index is ascertained, by finding the index of the waypoint that is just ahead of the car's position, in the 'generate_lane' function it is used to select a subset of waypoints that will form the lane message that is then published to **/final_waypoints** message.

If the subscriber **/traffic_waypoints** message has a base waypoint index of [-1] or an index greater than the LOOKAHEAD limit that indicates that the traffic light is not RED or not in the current trajectory given by the subset of base waypoints then the lane message is published with unaltered velocities and the car continues at its current velocity. However, if the subscriber has an index value that falls within the subset of base waypoints the 'decelerate_waypoints' function is called and it creates a new waypoint message and adds new velocities for all the base waypoints within the range. It does this by calculating velocities that are proportiional to the reducing distances as the car moves towards the stopline which are then compared to the reference velocities and the lower selected as the car decelerates. These base waypoints with their velocities adjusted are then published to final_waypoints message.

**3.** The **Control** subsystem comprises the DBW and waypoint_follower nodes. The waypoint_follower code is from Autoware and 
subscribes to: **/final_waypoints**, **/current_pose** and **/current_velocity**
publishes to: **/twist_cmd**

The final waypoints are used to generate the linear and angular velocities required by the DBW node which publishes the steering, brake and throttle values that allows the car to follow the trajectory based on the final waypoints. This module was completed by Simon.

### Udacity's initial Readme

This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images
