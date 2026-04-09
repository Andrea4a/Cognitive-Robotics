from typing import Any, Text, Dict, List

from rasa_sdk.events import FollowupAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import json
from utils.check_requirements import *
from rasa_sdk.events import SlotSet

top_mapping = {
    "top one": 1,
    "top two": 2,
    "top three": 3,
    "top four": 4,
    "top five": 5,
    "top six": 6,
    "top seven": 7,
    "top eight": 8,
    "top nine": 9,
    "top ten": 10
}

def debug(info):
    print("DEBUG:")
    for key, value in info:
        print(f"ENTITY: {key} - EXTRACTED VALUE: {value} - TYPE: {type(value)}")

class ActionSubmitRanking(Action):
    def name(self) -> Text:
        return "action_submit_ranking"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Ottieni il valore di n_top dallo slot
        n_top = tracker.get_slot("n_top")
        if n_top is not None:
            if n_top in top_mapping:
                n_top = top_mapping[n_top]
            n_top = int(n_top)

        try:
            filename = "ranking.json"

            with open(filename, 'r') as f:
                datastore = json.load(f)["results"]

            # Ordinare i gruppi in base al punteggio LFS (decrescente)
            ranked_groups = sorted(datastore, key=lambda x: x["LFS"], reverse=True)

            # Selezionare i primi n_top gruppi
            top_groups = ranked_groups[:n_top]
            
            # Creare un messaggio con la classifica
            message = f"Here are the top {n_top} groups based on LFS score:\n"
            for idx, group in enumerate(top_groups, start=1):
                message += f"\n{idx}. Group {group['Group']} with a LFS Score: {group['LFS']}\n"

            # Inviare il messaggio
            dispatcher.utter_message(message)

        except Exception as e:
            dispatcher.utter_message(response="utter_dont_understand")
            return []
