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

def number_to_words(n):
    """Converte un numero in parole."""
    words = {
        1: "one time",
        2: "two times",
        3: "three times",
        4: "four times",
        5: "five times",
        6: "six times",
        7: "seven times",
        8: "eight times",
        9: "nine times",
        10: "ten times"
    }
    return words.get(n, f"{n} times")  # Fallback per numeri maggiori di 10

def print_id(id_info, n_id, dispatcher: CollectingDispatcher):

    string=""

    # Stampa solo il vincitore
    wh_b = ""
    wh_h = ""
    if id_info['bag'] == "false":
        wh_b = "without"
    elif id_info["bag"] == "true":
        wh_b = "with"

    if id_info["hat"] == "false":
        wh_h = "without"
    elif id_info["hat"] == "true":
        wh_h = "with"


    string += f"The person with ID {n_id} is a {id_info['gender']} {wh_b} a bag and {wh_h} a hat."

    # Ottenere i passaggi nelle regioni di interesse
    n_pass_line_1 = id_info["trajectory"].count(1)
    n_pass_line_2 = id_info["trajectory"].count(2)
    n_pass_line_3 = id_info["trajectory"].count(3)
    n_pass_line_4 = id_info["trajectory"].count(4)

    line_passages = [
        f"line 1 {number_to_words(n_pass_line_1)}" if n_pass_line_1 > 0 else None,
        f"line 2 {number_to_words(n_pass_line_2)}" if n_pass_line_2 > 0 else None,
        f"line 3 {number_to_words(n_pass_line_3)}" if n_pass_line_3 > 0 else None,
        f"line 4 {number_to_words(n_pass_line_4)}" if n_pass_line_4 > 0 else None
    ]
    filtered_passages = [p for p in line_passages if p is not None]

    if len(filtered_passages) > 0:
        if len(filtered_passages) == 1:
            string += f"The person should have passed close to {filtered_passages[0]}."
        elif len(filtered_passages) == 2:
            string += f"The person should have passed close to {filtered_passages[0]} and {filtered_passages[1]}."
        else:
            locations = ", ".join(filtered_passages[:-1])
            string += f"The person should have passed close to {locations}, and {filtered_passages[-1]}."
    else:
        string += f"The person does not seem to have passed any of the locations."

    dispatcher.utter_message(string)

class ActionSubmitID(Action):
    def name(self) -> Text:
        return "action_submit_id"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        n_id = tracker.get_slot("id")

        try:
            filename = "output.json"

            with open(filename, 'r') as f:
                datastore = json.load(f)["people"]

            id_info = next((i for i in datastore if i["id"] == int(n_id)), None)

            if n_id is not None:
                n_id = int(n_id)
            # bot says the results of the research
            if n_id > 21:
                dispatcher.utter_message("The number of the people is 21.")
            elif len(datastore) > 1:
                print_id(id_info, n_id, dispatcher)  # Passa il vincitore
            else:  # if no person was found
                dispatcher.utter_message("I'm so sorry, I've not found any person that satisfies the requirements...")
                dispatcher.utter_message(response="utter_ask_new_search")
                return [AllSlotsReset()]
            
        except Exception as e:
            # if an exception is found, it utters a "don't understand" message and resets all the slots
            dispatcher.utter_message(response="utter_dont_understand")
            return []
