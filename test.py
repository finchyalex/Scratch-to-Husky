from HuskyTools.husky_tools.husky_python.husky import Husky
import time

husky = Husky(10,10,"localhost")
#Repeat 5 times
for i in range(5):
    husky.moveTime(1,2)
    husky.moveTime(1,-2)


