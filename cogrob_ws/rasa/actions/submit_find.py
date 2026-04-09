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


def print_person_info(person, dispatcher: CollectingDispatcher):
    string=""

    subj = "it"
    pron = "it"

    # Determinare il genere
    if person["gender"] == "male":
        subj = "he"
        pron = "him"
    else:
        subj = "she"
        pron = "her"

    # Ottenere i passaggi nelle regioni di interesse
    n_pass_line_1 = person["trajectory"].count(1)
    n_pass_line_2 = person["trajectory"].count(2)
    n_pass_line_3 = person["trajectory"].count(3)
    n_pass_line_4 = person["trajectory"].count(4)

    # Calcolo delle descrizioni delle linee attraversate
    line_passages = [
        f"line 1 {number_to_words(n_pass_line_1)}" if n_pass_line_1 > 0 else None,
        f"line 2 {number_to_words(n_pass_line_2)}" if n_pass_line_2 > 0 else None,
        f"line 3 {number_to_words(n_pass_line_3)}" if n_pass_line_3 > 0 else None,
        f"line 4 {number_to_words(n_pass_line_4)}" if n_pass_line_4 > 0 else None
    ]
    filtered_passages = [p for p in line_passages if p is not None]

    # Generazione della frase basata sulle linee attraversate
    if len(filtered_passages) > 0:
        if len(filtered_passages) == 1:
            string += f"{pron} should have passed close to {filtered_passages[0]}."
        elif len(filtered_passages) == 2:
            string += f"{pron} should have passed close to {filtered_passages[0]} and {filtered_passages[1]}."
        else:
            locations = ", ".join(filtered_passages[:-1])
            string += f"{pron} should have passed close to {locations}, and {filtered_passages[-1]}."
    else:
        string += f"{pron} does not seem to have passed any of the locations."


    # Risposta del bot
    dispatcher.utter_message(string)



class ActionSubmitFind(Action):
    def name(self) -> Text:
        return "action_submit_find"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # extracting info from the slots that are set
        info = [(key, tracker.get_slot(key)) for key in tracker.slots]
        # ----- TO REMOVE -----
        debug(info)

        if check_all_doubt(tracker):
            dispatcher.utter_message(response="utter_dont_understand")
            return [AllSlotsReset()]
        # if no info is extracted, the search in the database is not performed
        if len(info) == 0:
            dispatcher.utter_message(response="utter_dont_understand")
            return []
        try:
            filename = "output.json"
            with open(filename, 'r') as f:
                datastore = json.load(f)["people"]

            tmp_datastore = datastore.copy()
            for person in datastore:
                if not check_person(person=person, tracker=tracker):
                    tmp_datastore.remove(person)
            datastore = tmp_datastore.copy()
            ids_formatted = ", ".join([f"ID {person['id']}" for person in datastore])
            # bot says the results of the research
            if len(datastore) == 1:
                dispatcher.utter_message(f"Let me check in my database. There is only one person that satisfies your requirements. The person found have {ids_formatted}")
                return []
            elif len(datastore) > 1:
                dispatcher.utter_message(f"Let me check in my database. I found {len(datastore)} people that satisfy the description. The people found have {ids_formatted}")
                return []
            else:  # if no person was found
                dispatcher.utter_message("Let me check in my database. I'm so sorry, I've not found any person that satisfies the requirements...")
                return [AllSlotsReset()]
            
            



        except Exception as e:
            # if an exception is found, it utters a "don't understand" message and resets all the slots
            dispatcher.utter_message("ding")
            dispatcher.utter_message(response="utter_dont_understand")
            return []
