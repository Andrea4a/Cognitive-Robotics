from typing import Any, Text, Dict, List

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from utils.correct_entities import correct_entities, read_json


class ActionCorrectEntitiesValues(Action):

    def name(self) -> Text:
        return "action_correct_entities_values"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Update slots with correct values
        :param dispatcher:
        :param tracker:
        :param domain:
        :return: updated slots or None
        """

        all_values = tracker.current_slot_values()

        entities_values = dict()
        entities_db = read_json()

        for i in all_values:
            slot_value = tracker.get_slot(i)

            if slot_value is None:
                slot_value = "None"

            elif slot_value is True or slot_value is False:
                slot_value = str(slot_value).lower()

            if slot_value not in entities_db["values"]:
                entities_values[i] = slot_value

        if len(entities_values) > 0:
            correct_slot = correct_entities(entities_values)

            print("correct entities values: ", correct_slot)
            return [SlotSet(key, value) for key, value in correct_slot.items()]

        return []

    # def _obtain_values_entities(self, values) -> Dict[Text, Any]:
    #     """
    #     Extract and organize relevant information
    #     from entities in the latest message.

    #     :param values: List of entities extracted from the latest user message.
    #     :return: A dictionary containing organized information
    #             related to 'roi', 'duration', and 'number'.
    #     """
    #     all_values = {
    #         "trajectory": [["line_1", -1, -1], ["line_2", -1, -1], ["line_3", -1, -1], ["line_4", -1, -1]]
    #     }

    #     index_traj  = 0
    #     for i, element in enumerate(values):
    #         if element["entity"] == "trajectory" and element["group"] == "line_2_group":
    #             all_values["trajectory"][0] = ["line_2", element["start"], index_traj]
    #             index_traj += 1
    #         elif element["entity"] == "trajectory" and element["group"] == "line_1_group":
    #             all_values["trajectory"][1] = ["line_1", element["start"], index_traj]
    #             index_traj += 1
    #         elif element["entity"] == "trajectory" and element["group"] == "line_3_group":
    #             all_values["trajectory"][2] = ["line_3", element["start"], index_traj]
    #             index_traj += 1
    #         elif element["entity"] == "trajectory" and element["group"] == "line_4_group":
    #             all_values["trajectory"][3] = ["line_4", element["start"], index_traj]
    #             index_traj += 1

    #     return all_values



