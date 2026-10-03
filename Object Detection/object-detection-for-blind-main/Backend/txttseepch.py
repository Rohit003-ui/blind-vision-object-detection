import pyttsx3
from basic_code import *

t_s=pyttsx3.init()

obs=str(classNames[classId-1])
t_s.say(obs)
t_s.runAndWait()
