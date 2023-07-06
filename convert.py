#Get a file input and convert it from a scratch JSON to a .txt file
#We are only looking for a entry with the name husky
#Here is an example of the JSON file
#{"targets":[{"isStage":true,"name":"Stage","variables":{"`jEk@4|i[#Fk?(8x)AV.-my variable":["my variable",0]},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[{"assetId":"cd21514d0531fdffb22204e0ec5ed84a","name":"backdrop1","md5ext":"cd21514d0531fdffb22204e0ec5ed84a.svg","dataFormat":"svg","rotationCenterX":240,"rotationCenterY":180}],"sounds":[{"assetId":"83a9787d4cb6f3b7632b4ddfebf74367","name":"pop","dataFormat":"wav","format":"","rate":48000,"sampleCount":1123,"md5ext":"83a9787d4cb6f3b7632b4ddfebf74367.wav"}],"volume":100,"layerOrder":0,"tempo":60,"videoTransparency":50,"videoState":"on","textToSpeechLanguage":null},{"isStage":false,"name":"Husky","variables":{},"lists":{},"broadcasts":{},"blocks":{"~?@[e|@xX(*PI%Bfz#u8":{"opcode":"motion_movesteps","next":null,"parent":"DwXo36s]-)q(qX|ukG^l","inputs":{"STEPS":[1,[4,"10"]]},"fields":{},"shadow":false,"topLevel":false},"DwXo36s]-)q(qX|ukG^l":{"opcode":"event_whenflagclicked","next":"~?@[e|@xX(*PI%Bfz#u8","parent":null,"inputs":{},"fields":{},"shadow":false,"topLevel":true,"x":196,"y":80}},"comments":{},"currentCostume":0,"costumes":[{"assetId":"35070c1078c4eec153ea2769516c922c","name":"Retro Robot a","bitmapResolution":1,"md5ext":"35070c1078c4eec153ea2769516c922c.svg","dataFormat":"svg","rotationCenterX":55.04000000000008,"rotationCenterY":85.55},{"assetId":"d139f89665962dcaab4cb2b246359ba1","name":"Retro Robot b","bitmapResolution":1,"md5ext":"d139f89665962dcaab4cb2b246359ba1.svg","dataFormat":"svg","rotationCenterX":50.49583299552708,"rotationCenterY":87.39},{"assetId":"53398a713b144ecda6ec32fb4a8d28e1","name":"Retro Robot c","bitmapResolution":1,"md5ext":"53398a713b144ecda6ec32fb4a8d28e1.svg","dataFormat":"svg","rotationCenterX":70.61999999999998,"rotationCenterY":90.3795}],"sounds":[{"assetId":"1da43f6d52d0615da8a250e28100a80d","name":"computer beeps1","dataFormat":"wav","format":"","rate":48000,"sampleCount":83591,"md5ext":"1da43f6d52d0615da8a250e28100a80d.wav"},{"assetId":"28c76b6bebd04be1383fe9ba4933d263","name":"computer beeps2","dataFormat":"wav","format":"","rate":48000,"sampleCount":41517,"md5ext":"28c76b6bebd04be1383fe9ba4933d263.wav"}],"volume":100,"layerOrder":1,"visible":true,"x":-197,"y":120,"size":30,"direction":90,"draggable":false,"rotationStyle":"all around"}],"monitors":[],"extensions":[],"meta":{"semver":"3.0.0","vm":"0.2.0-prerelease.20220222132735","agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Scratch/3.29.1 Chrome/94.0.4606.81 Electron/15.3.1 Safari/537.36"}}
#The file is a JSON file, so we need to import the JSON library
import json
#We need to import the sys library to get the file input
import sys
#We need to import the os library to get the file output
import os
#Get the file as an achive
#Unzip the file

from translation import convertCommand


import zipfile

allowed_commands = ["event_whenflagclicked","motion_movesteps","motion_turnright","motion_turnleft","control_wait","control_repeat"] #These are the allowed scratch commands I might include more later
#These will be translated to a middle language that the next program to control the robot will understand

#Map each allowed command to an output command later

#Get the file input
#Check if sys.argv[1] exists
if len(sys.argv) < 2:
    print("No file input")
    exit()
file_input = sys.argv[1]
#If the file input is not a JSON file, then exit

#see if file exists
if not os.path.exists(file_input):
    print("File does not exist")
    exit()

zip = zipfile.ZipFile(file_input)

#Get the name of the file
file_name = os.path.basename(file_input)
#Remove the extension
file_name = os.path.splitext(file_name)[0]

zip.extractall(file_name)
#get the json file from the zip file
#Remove all the files except the json file
for file in os.listdir(file_name):
    if not file.endswith(".json"):
        os.remove(os.path.join(file_name, file))
file_input = file_name + "/project.json"


print("Converting file: " + file_input)

#Convert the file to a json object
json_file = open(file_input)
json_object = json.load(json_file)

#The object is a list of targets
#Print the name of each target

#Lets see if the husky target exists
husky_target = None
for target in json_object["targets"]:
    if target["name"] == "Husky":
        husky_target = target
        break

if husky_target == None:
    print("The husky target does not exist")
    exit()

#Now let's figure out the movement commands in order, the first command should be the event_whenflagclicked command

#get the event_whenflagclicked command
event_whenflagclicked_command = None
for command in husky_target["blocks"]:
    if husky_target["blocks"][command]["opcode"] == "event_whenflagclicked":
        event_whenflagclicked_command = husky_target["blocks"][command]
        break

if event_whenflagclicked_command == None:
    print("There is no start command")
    exit()

#Now we need to get the next command

#Continue getting next command until the next command is null
CurrentCommand = event_whenflagclicked_command
IsNextCommand = True

Commands = []

while IsNextCommand:
    if(CurrentCommand["next"] == None):
        IsNextCommand = False
        break
    next_command_id = CurrentCommand["next"]
    next_command = husky_target["blocks"][next_command_id]
    CurrentCommand = next_command
    #Get Inputs of the current command
    OutputCommands = convertCommand(CurrentCommand, husky_target)
    Commands.extend(OutputCommands)

    #Add the command to a list we can output later

#Write the commands to a file
#The command with be .husky
#Create new file
file_output = file_input.split(".")[0] + ".husky"
print("Writing to file: " + file_output)
output_file = open(file_output, "w+")
#Write the commands to the file
print(Commands)
for command in Commands:
    output_file.write(command + "\n")
#Close the file
output_file.close()
#Delete the scratch project