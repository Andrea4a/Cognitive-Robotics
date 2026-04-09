from rasa_sdk import Tracker
import re

doubt_string = "doubt"


def check_gender(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the gender requirement.
    :param person: The person to check the gender
    :param tracker: Tracker used to get the gender
    :return: True if the person satisfies the gender requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person gender attribute and gender requirement
    gender: str = tracker.get_slot("gender")
    gender = gender.lower() if gender is not None else None
    person_gender: str = person["gender"].lower()

    # checking if the person satisfies the gender requirement
    if gender is not None:
        if gender == doubt_string:
            return True
        if gender != person_gender:
            return False

    return True

def check_hat(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the hat requirement.
    :param person: The person to check the hat
    :param tracker: Tracker used to get the hat
    :return: True if the person satisfies the hat requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person hat attribute and hat requirement
    hat: str = tracker.get_slot("hat")
    hat = str(hat).lower() if hat is not None else None
    person_hat: str = person["hat"].lower()

    if hat is not None:
        if hat == doubt_string:
            return True

    is_with_hat = tracker.get_slot("is_with_hat")

    if hat is not None and hat != "false" and is_with_hat is None:
        is_with_hat = "true"
    elif hat is not None and hat != "hat" and is_with_hat is None:
        is_with_hat = "false"

    # checking if the person satisfies the hat requirement
    if is_with_hat is not None:
        if is_with_hat != person_hat:
            return False

    return True

def convert_time_in_seconds(string: str) -> int:
    """
    Converts the string in input in seconds, the string must contain a integer number and also the type of time (e.g.
    seconds, hour, minute).
    :param string: The string to convert the value of
    :return: An integer representing the time in seconds
    """
    regex = re.findall(r'\d+', string)

    # setting the time initially and checking if at least one occurrence of the regex exists,
    # if so takes the first value
    time: int = 0
    if len(regex) > 0:
        time = int(regex[0])

    # check if time is in seconds, minutes or hours
    if "second" in string:
        return time
    elif "minute" in string:
        return time*60
    elif "hour" in string:
        return time*60*60
    else:
        # if no type is given, return the time
        return time

def check_trajectory(person: dict, tracker: Tracker) -> bool:
    """
    Verifica se tutti i punti nella traiettoria fornita dall'utente sono presenti nella traiettoria della persona.
    La traiettoria della persona può contenere altri punti, ma deve includere quelli specificati dall'utente.
    :param person: Dizionario che rappresenta la persona con una chiave "trajectory".
    :param tracker: Tracker che contiene gli slot "trajectory" e "is_with_trajectory".
    :return: True se la persona soddisfa il requisito della traiettoria, False altrimenti.
    """

    line_mapping = {
    "line one": 1,
    "line two": 2,
    "line three": 3,
    "line four": 4,
    }

    # Recupera gli slot dal tracker
    trajectory = tracker.get_slot("trajectory")
    is_with_trajectory = tracker.get_slot("is_with_trajectory")
    person_points_count = 0
    number = tracker.get_slot("number")
    condition = tracker.get_slot("condition")

    # Se la traiettoria non è specificata, considera il controllo superato
    if not trajectory:
        return True
    
    if trajectory is not None:
        if trajectory == doubt_string:
            return True

    # Converte la traiettoria in una lista di interi
    try:
        trajectory = [int(x) for x in trajectory]
    except ValueError:
        return True

    # Recupera la traiettoria della persona
    person_trajectory = person.get("trajectory", [])
    if not isinstance(person_trajectory, list):
        return False
    
    # Logica basata su is_with_trajectory
    if str(is_with_trajectory).lower() == "false":
        # Assicura che NESSUNO dei punti specificati sia presente nella traiettoria della persona
        if any(point in person_trajectory for point in trajectory):
            return False
    else:
        # Assicura che TUTTI i punti specificati siano presenti nella traiettoria della persona
        if not all(point in person_trajectory for point in trajectory):
            return False

    if number or condition:
        try:
            number = int(number)
        except ValueError:
            return False
        
        person_points_count = sum(person_trajectory.count(point) for point in trajectory)

        if number and condition:
            if condition.lower() == "more":
                # Controlla che i punti specificati siano presenti almeno 'number' volte
                if person_points_count < number + 1:
                    return False
            elif condition.lower() == "less":
                # Controlla che i punti specificati siano presenti al massimo 'number' volte
                if person_points_count > number:
                    return False
            elif condition.lower() == "exactly":
                if person_points_count != number:
                    return False
        elif number and not condition:
            if person_points_count < number:
                return False

    return True


def check_bag(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies the bag requirement.
    :param person: The person to check the bag
    :param tracker: Tracker used to get the bag
    :return: True if the person satisfies the bag requirement or if no requirement about this attribute is given,
    otherwise False
    """

    # getting person bag attribute and bag requirement
    bag: str = tracker.get_slot("bag")
    bag = str(bag).lower() if bag is not None else None
    person_bag: str = person["bag"].lower()

    if bag is not None:
        if bag == doubt_string:
            return True

    is_with_bag = tracker.get_slot("is_with_bag")

    if bag is not None and bag != "false" and is_with_bag is None:
        is_with_bag = "true"
    elif bag is not None and bag != "bag" and is_with_bag is None:
        is_with_bag = "false"

    # checking if the person satisfies the bag requirement
    if is_with_bag is not None:
        if is_with_bag != person_bag:
            return False

    return True

def check_person(person: dict, tracker: Tracker) -> bool:
    """
    Checks if the person satisfies all the requirements.
    :param person: The person to check the requirements
    :param tracker: Contains the information given by the user
    :return: True if the person satisfies all the requirements, otherwise False
    """
    if not check_gender(person=person, tracker=tracker):
        return False

    if not check_hat(person=person, tracker=tracker):
        return False

    if not check_bag(person=person, tracker=tracker):
        return False

    if not check_trajectory(person=person, tracker=tracker):
        return False

    return True

def convert_time_in_seconds(string: str) -> int:
    """
    Converts the string in input in seconds, the string must contain a integer number and also the type of time (e.g.
    seconds, hour, minute).
    :param string: The string to convert the value of
    :return: An integer representing the time in seconds
    """
    regex = re.findall(r'\d+', string)

    # setting the time initially and checking if at least one occurrence of the regex exists,
    # if so takes the first value
    time: int = 0
    if len(regex) > 0:
        time = int(regex[0])

    # check if time is in seconds, minutes or hours
    if "second" in string:
        return time
    elif "minute" in string:
        return time*60
    elif "hour" in string:
        return time*60*60
    else:
        # if no type is given, return the time
        return time

def check_all_doubt(tracker: Tracker):
    """
    Checks if all the slots are set to the doubt string.
    :param tracker: Contains the information given by the user
    :return: True if all the doubt slots are set to the doubt string, otherwise False
    """
    doubt_slots = ["gender", "hat", "bag", "trajectory", "is_with_hat", "is_with_bag"]

    for slot in doubt_slots:
        slot_value: str = tracker.get_slot(slot)
        if slot_value is None:
            return False
        if str(slot_value).lower() != doubt_string:
            return False

    return True
