from fuzzywuzzy import process, fuzz
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet

import json


def slots_and_correct_values():

    """
    Defines a dictionary mapping slot names to
    their correct values or predefined choices.
    :return: A dictionary representing slot names and
            their correct values or predefined choices.
    """

    with_values = [True, False]

    return {
        "hat": "hat",
        "bag": "bag",
        "gender": ["male", "female"],
        "is_with_hat": with_values,
        "hat_value": "hat",
        "is_with_bag": with_values,
        "bag_value": "bag",
        "is_with": with_values,
        "is_with_line_1": False,
        "is_with_line_2": False,
        "is_with_line_3": False,
        "is_with_line_4": False,
    }


def read_json() -> dict:

    filename = "entities.json"
    try:
        with open(filename, 'r') as f:
            return json.load(f)

    except Exception as e:
        print("error during loading json file")


def fuzzy_replace(text, category, db):
    """
    Performs fuzzy matching to find the best match
    for a given text within a category in a database.

    :param text: The text to find a match for.
    :param category: The category within the database to search for matches.
    :param db: The database containing possible choices for the given category.

    :return: A tuple containing the best matching choice,
             its score, and the category it belongs to.
             Returns None if no suitable match is found.
    """
    choices = db.get(category, [])

    ignore_words = ["the", "a", "an", "is", "of", "to"]
    if text.lower() in ignore_words:
        print(f"Skipping fuzzy match for ignored word: {text}")
        return text
    match, score = process.extractOne(text, choices)
    if score >= 65 and fuzz.ratio(text, match) > 60:
        return match, score + fuzz.ratio(text, match), category
    else:
        return None


def max_matching(word, db, slot_entity):

    """
    Finds the best matching key from a database for a given word and slot_entity.
    :param word: The word to find a match for.
    :param db: The database containing keys for potential matches.
    :param slot_entity: The specific slot entity for which the matching is performed.
    :return: The best matching key and its associated score.
    """

    matching_list = []

    slots_entities = {
        "hat": ["yes", "no", "hat"],
        "bag": ["yes", "no", "bag"],
        "gender": ["male", "female"],
        "is_with_hat": ["with", "without"],
        "hat_value": "hat",
        "is_with_bag": ["with", "without"],
        "bag_value": "bag",
        "is_with": ["with", "without"],
        "is_with_trajectory": ["not pass", "pass"],
        "trajectory" : "dynamic_list"
    }
    for key in db.keys():
        match = None
        if key in slots_entities[slot_entity]:
            match = fuzzy_replace(word, key, db)
        #print(match)
        if match is not None:
            matching_list.append(match)

    if len(matching_list) < 1:
        return None
    else:
        best_match = max(matching_list, key=lambda item: item[1])
        print(best_match)

        if best_match[2] == "adv":
            return best_match[0]
        else:
            return best_match[2]


def correct_values(word_value, db, key):
    """
    Correct a given word value based on a database and a specified key.
    :param word_value: The value to be corrected.
    :param db: The database containing relevant information for correction.
    :param key: The key indicating the context of the correction.
    :return: The corrected value.
    """

    matching = max_matching(word_value, db, key)  # Trova la miglior corrispondenza.

    if matching is None:
        return None


    # Interpretazione di valori booleani
    if matching == "with" or matching == "pass":
        return True
    elif matching == "without" or matching == "not pass":
        return False

    # Restituisci il valore matchato direttamente
    return matching


# called from action correct_entities_values.py
def correct_entities(values_slots) -> Dict[Text, Any]:
    """
    Corrects the values of specific slots in a given dictionary
    based on predefined entity values.
    :param values_slots: A dictionary containing slot names and their corresponding values to be corrected.
    :return: A dictionary with corrected slot values.
    """

    entities_db = read_json()  # Carica il database di entità.

    values_slots_correct = dict()  # Dizionario per i valori corretti.
    trajectory = ["trajectory","number","condition","group"]  # Slot esclusi dalla correzione.

    for key, slot_value in values_slots.items():
        if key not in trajectory:
            if (key == "gender" and slot_value.lower() == ["the", "mall"]):
                continue
            else:
                corrected_value = correct_values(slot_value, entities_db, key)  # Correggi il valore.
                values_slots_correct[key] = corrected_value

    return values_slots_correct



# called from validate_form.py
def validate_input_form(slot_name, slot_value):

    """
    Validates and corrects the input value for a given slot in a form.

    :param slot_name: The name of the slot being validated.
    :param slot_value: The value of the slot to be validated.
    :return: The validated and possibly corrected slot value.
    """

    entities_db = read_json()

    if slot_value is None:
        return slot_value

    elif slot_value is True or slot_value is False:
        return slot_value

    if slot_value not in entities_db["values"]:
        slot_value = correct_values(slot_value, entities_db, slot_name)

    return slot_value





