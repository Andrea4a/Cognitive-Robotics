from typing import Any, Text, Dict, List

from rasa_sdk.events import FollowupAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import json
from utils.check_requirements import *
from rasa_sdk.events import SlotSet

def debug(info):
    print("DEBUG:")
    for key, value in info:
        print(f"ENTITY: {key} - EXTRACTED VALUE: {value} - TYPE: {type(value)}")

def print_group_info(group, group_slot, dispatcher: CollectingDispatcher):
    # Stampa solo il vincitore
    if group['Group'] == 1:
        string = f"The winner is {group['Group']} Group."
    else:
        string = f"The {group_slot}° is {group['Group']} Group."

    dispatcher.utter_message(string)

class ActionSubmitGroup(Action):
    def name(self) -> Text:
        return "action_submit_group"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        group_slot = tracker.get_slot("group")

        try:
            filename = "ranking.json"

            with open(filename, 'r') as f:
                datastore = json.load(f)["results"]

            group_info = next((g for g in datastore if g["Position"] == int(group_slot)), None)

            if group_slot is not None:
                group_slot = int(group_slot)

            # bot says the results of the research
            if group_slot > 14:
                dispatcher.utter_message("The number of the groups is 14.")
            elif len(datastore) > 1:
                print_group_info(group_info, group_slot, dispatcher)  # Passa il vincitore
            else:  # if no person was found
                dispatcher.utter_message("I'm so sorry, I've not found any person that satisfies the requirements...")
                dispatcher.utter_message(response="utter_ask_new_search")
                return [AllSlotsReset()]
            
        except Exception as e:
            # if an exception is found, it utters a "don't understand" message and resets all the slots
            dispatcher.utter_message(response="utter_dont_understand")
            return []
