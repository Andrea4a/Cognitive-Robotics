#!/usr/bin/python3
from utils import Session
import rospy
from std_msgs.msg import String
import time

class AnimationNode:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.session = Session(ip, port)
        self.ar = self.session.get_service("ALAnimationPlayer")
        self.reset = self.session.get_service("ALRobotPosture")
        self.reset.goToPosture("Stand", 1.0)  # reset position

        rospy.Subscriber("animation_topic", String, self.run)
        rospy.loginfo("Animation server is listening on 'animation_topic'.")

    def run(self, msg):
        rospy.loginfo(f"Received request for action: {msg.data}")
        try:
            self.ar.runTag(msg.data)
            time.sleep(1)  # Let the animation finish
        except:
            rospy.logwarn("Reconnecting to ALAnimationPlayer...")
            self.session.reconnect()
            self.ar = self.session.get_service("ALAnimationPlayer")
            self.ar.runTag(msg.data)
            time.sleep(1)

if __name__ == "__main__":
    import time
    time.sleep(3)

    ip = "10.0.1.207"
    port = 9559
    rospy.init_node("animation_server")
    
    animation = AnimationNode(ip, port)
    rospy.spin()
