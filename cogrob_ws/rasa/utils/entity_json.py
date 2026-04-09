import json
import random

def main():
    # number of people to generate

    filename = "entities.json"

    db = dict()

    with open(filename, "r") as infile:
        db = json.load(infile)

    print(type(db))
    for key, value in db.items():
        print(key, value)

if __name__ == '__main__':
    main()
