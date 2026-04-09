from typing import Any, Text, Dict, List

from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionAllSlotsReset(Action):
    def name(self) -> Text:
        return "action_all_slots_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [AllSlotsReset()]
