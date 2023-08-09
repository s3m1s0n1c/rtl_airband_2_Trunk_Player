#!/bin/bash

#### Configuration ####

## Directory of convert2tp.py (No Trailing /) ##
script_dir="/home/radio/convert"

## Trunk-Player Directory ##
tp_dir="/home/radio/trunk-player"

## Full Path of CSV File ##
csv_file="/home/radio/convert/channels.csv"

## Web Url (This is the Path minus the first folder to the mp3/json files ##

weburl="uhfcb-A/"

## System Number in TP ##
system=0

## Source Number in TP ##
source=0


file=$(basename ${1})
filename=${file%.*}
filepath=$(dirname ${1})

echo "Filename without Extension: $filepath/$filename" >> $script_dir/convert2tp.log

#### Run Convert Script to Generate Json Files for TP ####
echo "Running Convert Script" >> $script_dir/convert2tp.log

/usr/bin/python3 $script_dir/convert2tp.py ${1} $csv_file $system $source >> $script_dir/convert2tp.log
echo /usr/bin/python3 $script_dir/convert2tp.py ${1} $csv_file $system $source >> $script_dir/convert2tp.log


echo "Convert Script Done" >> $script_dir/convert2tp.log

#### Set Enviroment Up for TP ####

echo "Adding file to TP" >> $script_dir/convert2tp.log
cd $tp_dir

echo "Setting up Virtual Enviroment" >> $script_dir/convert2tp.log
source env/bin/activate

#### Add file To TP ####
echo "Adding file to TP" >> $script_dir/convert2tp.log
./manage.py add_transmission $filepath/$filename --web_url=$weburl >> $script_dir/convert2tp.log
echo ./manage.py add_transmission $filepath/$filename --web_url=$weburl >> $script_dir/convert2tp.log

#### Cleaning up Files ####
echo "Cleaning up Json Files.."
echo "Removing" $filepath/$filename.json >> $script_dir/convert2tp.log
rm $filepath/$filename.json >> $script_dir/convert2tp.log
