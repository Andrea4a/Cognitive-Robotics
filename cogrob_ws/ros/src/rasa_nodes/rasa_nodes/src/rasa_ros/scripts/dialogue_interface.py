#!/usr/bin/env python3

import rospy
from rasa_ros.srv import Dialogue, DialogueResponse
from std_msgs.msg import String
from std_msgs.msg import Bool
from vision_msgs.msg import Detection2DArray




class TerminalInterface:
    '''Class implementing a terminal i/o interface. 

    Methods
    - get_text(self): return a string read from the terminal
    - set_text(self, text): prints the text on the terminal

    '''

    def __init__(self):
        self.pub_answer = rospy.Publisher('bot_answer', String, queue_size=10)  # Publisher of the RASA answer
        #self.sub_det = rospy.Subscriber('detection', Detection2DArray, self.detection_callback, queue_size=1)

    def get_text(self):
        print("Waiting the speech...")
        txt = None
        while txt is None:
            try:
                txt = rospy.wait_for_message("voice_txt", String)
            except:
                pass

        # prints on terminal the input message
        print("[IN]:", txt.data)

        return str(txt.data)

    def set_text(self, text):
        # prepares the text in input for publication, then it publishes it
        data_to_send = String()
        data_to_send.data = text
        self.pub_answer.publish(data_to_send)

        # prints on terminal the received output message 
        print("[OUT]:", text)
    '''
    def get_text(self):
        return input("[IN]:  ") 

    def set_text(self,text):
        print("[OUT]:",text)
        '''

def main():
    rospy.init_node('writing')
    rospy.wait_for_service('dialogue_server')
    dialogue_service = rospy.ServiceProxy('dialogue_server', Dialogue)

    terminal = TerminalInterface()

    while not rospy.is_shutdown():
        message = terminal.get_text()
        if message == 'exit': 
            break
        try:
            bot_answer = dialogue_service(message)
            terminal.set_text(bot_answer.answer)
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

if __name__ == '__main__':
    try: 
        main()
    except rospy.ROSInterruptException:
        pass