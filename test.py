from husky_tools.husky_python.husky import Husky
import time

husky = Husky(10,10)
husky.moveTime(1,2)
time.sleep(2)
husky.moveTime(1,-2)


