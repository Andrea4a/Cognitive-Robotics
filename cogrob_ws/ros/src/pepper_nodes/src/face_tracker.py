#!/usr/bin/python3

from utils import Session
from optparse import OptionParser
import rospy
from pepper_nodes.srv import WakeUp, Rest
import qi
import argparse
import sys


class TrackerNode:
    """
    This class implements a ROS node used to control the Pepper posture
    """

    def __init__(self, ip, port, faceSize):
        """
        The constructor creates a session to Pepper and initializes the services
        """
        self.ip = ip
        self.port = port
        self.session = Session(ip, port)
        self.faceSize = faceSize
        self.motion_proxy = self.session.get_service("ALMotion")
        self.posture_proxy = self.session.get_service("ALRobotPosture")
        self.tracker_service = self.session.get_service("ALTracker")
        self.basic_awareness_service = self.session.get_service("ALBasicAwareness")
        self.basic_awareness_service.startAwareness()
        self.basic_awareness_service.setStimulusDetectionEnabled("Sound", True)
        self.animation_player_service = self.session.get_service("ALAnimationPlayer")

    def stop(self, *args):
        """ 
        This method calls the ALMotion service and sets the robot to rest position
        """
        try:
            self.motion_proxy.rest()
            self.tracker_service.stopTracker()
        except:
            self.tracker_service = self.session.get_service("ALTracker")
            self.tracker_service.stopTracker()
        return "ACK"

    def start(self):
        """
        Starts the detection of the face
        """
        rospy.init_node("tracker_node")
        self.trackernode()
        rospy.Service("tracker", WakeUp, self.trackernode)
        rospy.spin()


    def trackernode(self, *args):
        """
        This method calls the ALMotion and ALRobotPosture services and it sets motors on and then it sets the robot posture to initial position
        """
        try:
            # Add target to track.
            targetName = "Face"
            faceWidth = self.faceSize
            self.tracker_service.registerTarget(targetName, faceWidth)
            # Then, start tracker.
            self.tracker_service.track(targetName)
        except:
            self.motion_proxy = self.session.get_service("ALMotion")
            self.posture_proxy = self.session.get_service("ALRobotPosture")
            self.tracker_service = self.session.get_service("ALTracker")
            self.animation_player_service = self.session.get_service("ALAnimationPlayer")
            self.basic_awareness_service = self.session.get_service("ALBasicAwareness")
            self.basic_awareness_service.setStimulusDetectionEnabled("Sound", True)
        return "ACK"

    def reset_head(self):

        if not self.basic_awareness_service.isTrackingEnabled():
            print("Nessun tracciamento")
            self.motion_proxy.setAngles(["HeadYaw","HeadPitch"], [0.0,0.0], 0.1)
        else:
            print("Tracciamento attivo") 
            
    def shutdown_callback(self):
        """
        Callback function triggered on node shutdown.
        Stops tracking, stops basic awareness, and sets the robot to rest position.
        """
        rospy.loginfo("Shutting down TrackerNode...")
        try:
            self.basic_awareness_service.stopAwareness()
            self.tracker_service.stopTracker()
            self.motion_proxy.rest()
        except Exception as e:
            rospy.logerr(f"Error during shutdown: {e}")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.207")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        node = TrackerNode(options.ip, int(options.port), 0.1)
        node.start()
    except rospy.ROSInterruptException:
        node.stop()
