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

class ActionSubmitScore(Action):
    def name(self) -> Text:
        return "action_submit_score"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Recupera lo slot 'group' (posizione nella classifica)
        group_slot = tracker.get_slot("group")
        
        if group_slot:
            try:
                # Carica i dati della classifica dal file JSON
                filename = "ranking.json"
                with open(filename, 'r') as f:
                    datastore = json.load(f)["results"]

                # Cerca il gruppo con la posizione specificata
                group_info = next((g for g in datastore if g["Position"] == int(group_slot)), None)

                if group_info:
                    # Estrai i membri e genera la risposta
                    score = group_info["AFS"]
                    dispatcher.utter_message(
                        f"The average score are: {score}."
                    )
                else:
                    # Nessun gruppo trovato per la posizione specificata
                    dispatcher.utter_message(f"I couldn't find any group in position {group_slot}°.")
                
            except FileNotFoundError:
                dispatcher.utter_message("The ranking file was not found.")
            except json.JSONDecodeError:
                dispatcher.utter_message("There was an error decoding the ranking file.")
            except Exception as e:
                dispatcher.utter_message(f"An unexpected error occurred: {str(e)}")
        else:
            # Lo slot 'group' non è stato impostato
            dispatcher.utter_message("It seems you didn't specify a group number.")

        return []

