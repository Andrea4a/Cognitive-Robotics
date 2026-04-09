#!/usr/bin/python3


import rospy


from std_msgs.msg import String, Bool
from pepper_nodes.srv import Text2Speech
from std_msgs.msg import Bool
import time

def main():
    print('Starting tts client...')

    rospy.init_node('speaking_node')
    rospy.wait_for_service('/tts')
    tts_service = rospy.ServiceProxy('/tts', Text2Speech)
    synchronize_speech = rospy.Publisher('is_pepper_speaking', Bool, queue_size=10)

    while not rospy.is_shutdown():
        txt = rospy.wait_for_message("bot_answer", String)

        # pepper starts to talk, stop speech recognition
        synchronize_speech.publish(True)
        
        msg: str = txt.data
        msg = msg.replace(",", "\\pau=100\\")
        msg = msg.replace(".", "\\pau=200\\")

        tts_service(msg)
        time.sleep(1)

        # pepper finishes to talk, starting again speech recognition
        synchronize_speech.publish(False)


if __name__ == '__main__':
    try: 
        main()
    except rospy.ROSInterruptException:
        pass
    