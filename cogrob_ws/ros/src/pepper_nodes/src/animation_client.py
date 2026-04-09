#!/usr/bin/python3

import rospy
from std_msgs.msg import String

class Handler:
    def __init__(self):
        self.pub = rospy.Publisher("animation_topic", String, queue_size=10)
        rospy.Subscriber("bot_answer", String, self.call)
        rospy.loginfo("Animation client initialized and listening to bot_answer topic.")

    def call(self, text):
        rospy.loginfo(f"Publishing animation request: {text.data}")
        self.pub.publish(text.data)  # Pubblica il testo sul topic "animation_topic"

if __name__ == "__main__":
    rospy.init_node("animation_client")
    handler = Handler()
    rospy.spin()
