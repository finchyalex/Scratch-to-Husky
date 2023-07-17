#This is an interpreter for the Husky programming language.
#It takes a .husky file and converts it directly into python code that can be run on the robot. 
#I will make it possible to run directly on the robot or export to python code.
#Here is an example of a .husky file:
#MOVE 10
#TURN 90
#WAIT 5
#REPEAT 2
#   MOVE 10
#   TURN 90
#END

#To Initialize the interpreter, you must pass in the file name of the .husky file
#The interpreter must also be passed a value to represent a unit of length, for example, 1 unit of length could be 1 inch

from ..husky_python.husky import Husky

class Interpreter:
    def __init__(self, file_name, unit_of_length, target_husky : Husky, output_location=None):
        if(output_location) == None:
            self.output_location = file_name.split(".")[0] + ".py"
        if(target_husky == None):
            print("No target husky, outputting to python file")
        self.file_name = file_name
        self.unit_of_length = unit_of_length
        self.target_husky = target_husky

    def __validate__(self):
        #Open the file and check for syntax errors
        #If there are syntax errors, print them and exit
        #If there are no syntax errors, continue
        file = open(self.file_name, "r")
        lines = file.readlines()
        for line in lines:
            if(line.split(" ")[0] == "MOVE"):
                try:
                    int(line.split(" ")[1])
                except:
                    print("Syntax error on line: " + line)
                    exit()
            elif(line.split(" ")[0] == "TURN"):
                try:
                    int(line.split(" ")[1])
                except:
                    print("Syntax error on line: " + line)
                    exit()
            elif(line.split(" ")[0] == "WAIT"):
                try:
                    int(line.split(" ")[1])
                except:
                    print("Syntax error on line: " + line)
                    exit()
            elif(line.split(" ")[0] == "REPEAT"):
                try:
                    int(line.split(" ")[1])
                except:
                    print("Syntax error on line: " + line)
                    exit()
            elif(line.split(" ")[0] == "END"):
                continue
            else:
                print("Syntax error on line: " + line)
                exit()
            
            return True
        
    def interpret(self,write_to_file=False):
        if(not self.__validate__):
            print("Syntax error")
        file = open(self.file_name, "r")
        lines = file.readlines()
        self.run(lines)

    def run(self, lines):
        husky : Husky = self.target_husky 
        
        #For each line, either run it on the husky or write it to the output file
        if(self.target_husky == None):
            pass

        for line in lines:
            if(line.split(" ")[0] == "MOVE"):
                #Get the distance to move
                distance = float(line.split(" ")[1])
                if(distance > 0):
                    husky.MoveForward(distance*self.unit_of_length)
                elif(distance < 0):
                    husky.MoveBackward(distance*self.unit_of_length)
            elif(line.split(" ")[0] == "TURN"):
                husky.Rotate(float(line.split(" ")[1]))
            elif(line.split(" ")[0] == "WAIT"):
                husky.wait(float(line.split(" ")[1]))
            elif(line.split(" ")[0] == "REPEAT"):
                #Only repeat the lines in the REPEAT block
                #It starts with REPEAT and ends with END
                #The number of times to repeat is the number after REPEAT
                times = int(line.split(" ")[1])
                
                #Get the lines to repeat
                lines_to_repeat = []
                for i in range(lines.index(line), len(lines)):
                    if(lines[i].split(" ")[0] == "END"):
                        break
                    lines_to_repeat.append(lines[i])
                    #Remove the lines that are going to be repeated from the list of lines
                    lines.remove(lines[i])
                
                #Repeat the lines
                for i in range(times):
                    self.run(lines_to_repeat)

                


            elif(line.split(" ")[0] == "END"):
                continue
            else:
                print("Syntax error on line: " + line)
                exit()

        

        
        

