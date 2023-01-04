import json
from datetime import date
counter_json_str = "counter.json"


def get_counter():
    try:
        with open(counter_json_str, 'r') as counter_json:
            return json.load(counter_json)
    except json.decoder.JSONDecodeError:
        return {}


def init_counter(counter):
    if str(date.today()) not in counter.keys():
        counter[str(date.today())] = 0
    with open(counter_json_str, 'w') as counter_json:
        json.dump(counter, counter_json, indent=4)
    return counter


def increment_counter(counter):
    with open(counter_json_str, 'w') as counter_json:
        counter[str(date.today())] += 1
        json.dump(counter, counter_json, indent=4)
