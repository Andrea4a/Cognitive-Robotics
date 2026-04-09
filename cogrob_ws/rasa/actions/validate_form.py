from typing import Any,Optional, Text, Dict, List

from rasa_sdk.events import EventType, SlotSet
from rasa_sdk import Tracker
from rasa_sdk import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from utils.correct_entities import validate_input_form


class ValidatePersonForm(FormValidationAction):
    _ask_intent = "ask_with_info"
    _unknown = "DOUBT"
    _unknown_intent = "doubt"
    _affirm_intent = ["affirm_with_entity", "affirm"]
    _deny_intent = ["deny_with_entity", "deny"]

    def name(self) -> Text:
        return "validate_person_form"
    
    def validate_trajectory(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        """
        Validates the 'trajectory' slot. Converts input into a list of integers.
        """

        # Check if 'is_with_trajectory' is false
        user_intent = tracker.get_intent_of_latest_message()
        if self._intent_not_know(user_intent):
            return {"trajectory": self._unknown}
        else:
            try:
                # Handle case where slot_value is a list with a single string element
                if isinstance(slot_value, list) and len(slot_value) == 1 and isinstance(slot_value[0], str):
                    slot_value = slot_value[0]  # Extract the string

                # Process string input to convert into a list of integers
                if isinstance(slot_value, str):
                    trajectory_list = [x.strip() for x in slot_value.split(",")]
                    return {"trajectory": trajectory_list}
                elif isinstance(slot_value, list):
                    # Validate that the list contains integers
                    trajectory_list = [str(x) for x in slot_value]
                    return {"trajectory": trajectory_list}
                else:
                    raise ValueError("Invalid trajectory format.")

            except ValueError:
                dispatcher.utter_message(text="Invalid trajectory format.")
                return {"trajectory": None}


    def validate_gender(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        invalid_genders = ["the"]

        if self._intent_not_know(user_intent):
            return {"gender": self._unknown}
        elif isinstance(slot_value, str) and slot_value.lower() in invalid_genders:
            return {}
        else:
            return {"gender": validate_input_form("gender", slot_value)}

    def validate_bag(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if user_intent in self._affirm_intent:
            return {"bag": "bag"}
        elif user_intent in self._deny_intent:
            return {"bag": False}

        if self._intent_not_know(user_intent):
            return {"bag": self._unknown}
        else:
            return {"bag": validate_input_form("bag", slot_value)}

    def validate_hat(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:

        user_intent = tracker.get_intent_of_latest_message()
        print(user_intent)

        if user_intent in self._affirm_intent:
            return {"hat": "hat"}
        elif user_intent in self._deny_intent:
            return {"hat": False}

        if self._intent_not_know(user_intent):
            return {"hat": self._unknown}
        else:
            return {"hat": validate_input_form("hat", slot_value)}





    def _intent_not_know(self, intent) -> bool:

        return True if self._unknown_intent in intent else False
