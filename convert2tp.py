import os
import csv
import json
import time
import sys
import argparse
from mutagen.mp3 import MP3


#Big Thanks to "TheGreatCodeholio" for help with this script - https://github.com/TheGreatCodeholio/


#Function for creating Json File
def create_json(mp3_filename, mp3_directory,mp3_url, system_config):
    print("Creating Json File for Trunk-Player")
    csv_headers = ["talkgroup_decimal", "channel_frequency", "pl_tone", "talkgroup_alpha_tag", "talkgroup_name",
                   "talkgroup_service_type", "talkgroup_group", "channel_enable"]
    
    with open(talkgroup_csv_path, 'r') as csv_file:
        csv_data = csv_file.read()
        reader = csv.DictReader(csv_data.splitlines(), fieldnames=csv_headers)
        channel_data = [row for row in reader]
        
    call_data = {
        "system": 0,
        "source": 0,
        "filename": "",
        "freq": 0,
        "start_time": 0,
        "stop_time": 0,
        "emergency": 0,
        "encrypted": 0,
        "call_length": 0,
        "talkgroup": 0,
        "talkgroup_tag": "",
        "talkgroup_description": "",
        "talkgroup_group_tag": "",
        "talkgroup_group": "",
        "audio_type": "analog",
        "short_name": "",
        "freqList": [],
        "srcList": []
    }
    # Split file name to extract data.
    parts = mp3_filename.split('_')

    # Extract the first, second, and third parts
    short_name = parts[0]
    timestamp_part = parts[1]
    frequency_part = int(parts[2].replace(".mp3", ""))

    # Load the MP3 file
    audio = MP3(os.path.join(mp3_directory, mp3_filename))

    # Get the duration in seconds
    duration_sec = audio.info.length

    # Get Start/End Time in UnixTime
    start_time = int(audio.info.length)
    end_time = 0

    start_unixtime = int(time.time()) - start_time
    stop_unixtime = int(time.time()) - end_time


    #Pull Data together for json file
    for tg in channel_data:
        if int(tg["channel_frequency"]) == frequency_part:
            talkgroup_data = tg
            break
    call_time = time.time() - duration_sec
    call_data["system"] = system
    call_data["source"] = source
    call_data["talkgroup"] = int(talkgroup_data["talkgroup_decimal"])
    call_data["start_time"] = start_unixtime
    call_data["stop_time"] = stop_unixtime
    call_data["call_length"] = duration_sec
    call_data["filename"] = mp3_url
    call_data["freq"] = int(frequency_part)
    call_data["talkgroup_tag"] = talkgroup_data["talkgroup_alpha_tag"]
    call_data["talkgroup_description"] = talkgroup_data["talkgroup_name"]
    call_data["talkgroup_group"] = talkgroup_data["talkgroup_group"]
    call_data["talkgroup_group_tag"] = talkgroup_data["talkgroup_service_type"]
    call_data["short_name"] = short_name
    call_data["freqList"].append({"freq": int(frequency_part), "time": call_time, "pos": 0.00, "len": duration_sec, "error_count": "0", "spike_count": "0"}),
    call_data["srcList"].append({"src": -1, "time": call_time, "pos": 0.00, "emergency": 0, "signal_system": "", "tag": ""})

    #Get Mp3 Filename to use for Json filename
    json_path = mp3_directory + "/" + os.path.splitext(mp3_filename)[0] + ".json"

    #Create Json file with data set
    with open(json_path, "w+") as f:
        json.dump(call_data, f, indent=4)
    f.close()

    print("JSON file created successfully!")


# We make nice command arguments here
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Non Trunk-Player file to Trunk-Player")

    parser.add_argument("mp3_url", type=str, help="URL of the MP3 file")
    parser.add_argument("talkgroup_csv_path", type=str, help="Path to the CSV file containing talkgroup data")
    parser.add_argument("system", type=int, help="System number")
    parser.add_argument("source", type=int, help="Source number")

    args = parser.parse_args()

    mp3_url = args.mp3_url
    mp3_filename = os.path.basename(mp3_url)
    mp3_directory = os.path.dirname(mp3_url)
    talkgroup_csv_path = args.talkgroup_csv_path
    system = args.system
    source = args.source

# Call function to run
print("Running Program To Make Files for Trunk-Player")
create_json(mp3_filename, mp3_directory, mp3_url, talkgroup_csv_path)
print("File have been created and ready to upload to Trunk-Player")



