import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def output(experience,timeliness,support,interaction,quality,trouble):
    if (experience==4 and timeliness==4 and support==4 and interaction==4 and quality==4 and trouble==0):
        return 5
    elif (experience==1 and timeliness==1 and support==1 and interaction==1 and quality==1 and trouble==1):
        return 1
    elif (experience==2 and timeliness==2 and support==1 and interaction==1 and quality==1 and trouble==0):
        return 1.5
    elif (experience<=2 and timeliness<=2 and support>=3 and interaction<=3 and quality<=3 and trouble==1):
        return 2
    elif (experience<=2 and timeliness<=2 and support>=3 and interaction<=3 and quality<=3 and trouble==0):
        return 2.5
    elif (experience==3 and timeliness==2 and support==3 and interaction==1 and quality==2 and trouble==1):
        return 3
    elif (experience==3 and timeliness==3 and support<=3 and interaction<=3 and quality==3 and trouble==0):
        return 4.5
    elif (experience==3 and timeliness==3 and support<=3 and interaction<=3 and quality==3 and trouble==1):
        return 4
    else :
        return 3.5
   
 

# experience = int(input())
# timeliness = int(input())
# support=int(input())
# interaction= int(input())
# quality=int(input())
# trouble=int(input())


# op=output(experience,timeliness,support,interaction,quality,trouble)
# print(op)
