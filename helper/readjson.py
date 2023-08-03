import json


def append_data_to_json_file(data):
    try:
        with open('caps.json', 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        print("Error!!!! : ", e)
        json_data = {}

    last_key = str(max(map(int, json_data.keys()), default=0) + 1)
    json_data[last_key] = data

    try:
        with open('caps.json', 'w') as file:
            json.dump(json_data, file, indent=2)
        print("Data appended to JSON file successfully.")
    except Exception as e:
        print(f"Failed to append data to JSON file: {str(e)}")


def get_first_key():
    try:
        with open('caps.json', 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        print("Error!!!! : ", e)
        json_data = {}
        
    if json_data == 0:
        return
    first_key = list(json_data.keys())[0]
    return first_key


def get_emuid() -> dict:

    with open('./caps.json', 'r') as f:
        data = json.load(f)
    key_list = list(data.keys())
    return key_list


def get_emudata(emuid) -> dict:
    with open('./caps.json', 'r') as f:
        data = json.load(f)

    tartget_data = data.get(emuid)
    if tartget_data:
        data_list = list(tartget_data.items())
        return data_list
    else:
        return []

    emudata = data


def getcaps() -> dict:
    with open("./caps.json", 'r') as f:
        data = json.load(f)

    list = []
    for key, value in data.items():
        temp_data = (value.get('udid'), value.get(
            'devicename'), value.get('systemport'))
        list.append(temp_data)

    return list


def remove_key_value_pair(json_file, key_to_remove):
    try:
        with open(json_file, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error while decoding JSON: {str(e)}")
        return

    if key_to_remove in json_data:
        del json_data[key_to_remove]
        try:
            with open(json_file, 'w') as file:
                json.dump(json_data, file, indent=2)
            print(f"Key '{key_to_remove}' and its value removed successfully.")
        except Exception as e:
            print(f"Failed to update JSON file: {str(e)}")
    else:
        print(f"Key '{key_to_remove}' not found in the JSON data.")


def putcaps(udid, devicename, systemport) -> None:
    new_data = {
        'udid': udid,
        'devicename': devicename,
        'systemport': systemport
    }

    append_data_to_json_file(new_data)


def getapps() -> dict:
    try:
        with open('./apps.json', 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print("not??? file")


def setapps(packagename, activityname) -> None:
    app_data = {
        'package': packagename,
        'activity': activityname
    }

    try:
        with open('./apps.json', 'w') as f:
            json.dump(app_data, f, indent=4)
    except Exception as e:
        print("not??? file", e)
