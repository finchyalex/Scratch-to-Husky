def convertCommand(commandinput,husky_target): 


    commandmap = {
        "motion_movesteps": ["MOVE", "STEPS"],
        "motion_turnright": ["TURN", "DEGREES"],
        "motion_turnleft": ["TURN", "DEGREES"],
        "control_wait" : ["WAIT", "DURATION"],
        "control_repeat" : ["REPEAT", "TIMES"]
        #Add additional opcodes, and their inputs and the value the inputs represent
    }


    husky_command = commandmap.get(commandinput["opcode"])
    if(husky_command == None):
        print("The command " + commandinput["opcode"] + " is not allowed... ignoring")
        return None


    #We have to do something unique for the repeat command
    if commandinput["opcode"] == "control_repeat":
        #We have to get the number of times to repeat
        #Everything inside the substack should be repeated by the number of times
        #Get the number of times to repeat
        commandinput["inputs"]["TIMES"][1][1] = int(commandinput["inputs"]["TIMES"][1][1])
        #Get the substack
        substack = commandinput["inputs"]["SUBSTACK"]
        #Get the number of times to repeat
        times = commandinput["inputs"]["TIMES"][1][1]
        #Get everything in the substack
        
        #Run through the commands in the substack starting with substack[1]

        SubStackHasNext = True
        Substack = []
        Substack.append("REPEAT")
        #Substack[1] contains the first ID of the command in the substack
        #We should get this from the husky_target
        InitialSubStackID = substack[1]

        #We should get the command from the husky_target
        CurrentCommand = husky_target["blocks"][InitialSubStackID]
        husky_command = commandmap.get(CurrentCommand["opcode"])
        Substack.append(husky_command[0] + " " + str(CurrentCommand["inputs"][husky_command[1]][1][1]))
        while SubStackHasNext:
            if(CurrentCommand["next"] == None):
                SubStackHasNext = False
                break
            next_command_id = CurrentCommand["next"]
            next_command = husky_target["blocks"][next_command_id]
            CurrentCommand = next_command
            husky_command = commandmap.get(CurrentCommand["opcode"])
            Substack.append(husky_command[0] + " " + str(CurrentCommand["inputs"][husky_command[1]][1][1]))
        
        #We can end out substack by adding a number of repeats this code should be repeated
        NewTimingStructure = "TIMES " + str(times)
        Substack.append(NewTimingStructure)
        return Substack
            


    return [husky_command[0] + " " + str(commandinput["inputs"][husky_command[1]][1][1])]
    
