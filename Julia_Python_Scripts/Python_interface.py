## Testing a possible Python Interface for NuXmv
## Ongoing Process
## Juan Benavides 3/28/2022

from cProfile import label
import os
import subprocess as sp
import re
import matplotlib.pyplot as plt
import numpy as np



'''
Specs to check:

Does tank ever go above...:
LTLSPEC G (time <= 170 -> tank <= 550); -- 0
LTLSPEC G (time <= 170 -> tank <= 600); -- 1
LTLSPEC G (time <= 170 -> tank <= 650); -- 2

Does tank ever go below ...:
LTLSPEC G (time <= 170 -> tank >= 300); -- 3
LTLSPEC G (time <= 170 -> tank >= 200); -- 4
LTLSPEC G (time <= 170 -> tank >= 100); -- 5
LTLSPEC G (time <= 170 -> tank >= 25); -- 6
LTLSPEC G (time <= 170 -> tank >= 10); -- 7

'''

# get to the right directory
os.chdir('..')
os.chdir('NuXmv Models')

# launch nuxmv and save counterexample trace down
print("Launching NuXmv - This may take a minute")
nuxmv = sp.Popen('nuxmv -n 7  CyberFalseFinite.smv ',stdout=sp.PIPE,universal_newlines=True)
output = nuxmv.stdout.read()

# get a list of states
states = re.split("State:",output)

# parse to get an array of tank and tank sensor states
tanks = np.ones(len(states)) * 700
sensors = np.ones(len(states)) * 700
for time,state in enumerate(states):
    if time == 0: continue
    tank = re.findall("tank = [0-9]+",state)
    sensor = re.findall("tankSensor = [0-9]+",state)
    if len(tank) == 0:
        tanks[time] = tanks[time-1]
    else:
        tank = re.findall("[0-9]+",tank[0])
        tanks[time] = int(tank[0])
    if len(sensor) == 0:
        sensors[time] = sensors[time-1]
    else:
        sensor = re.findall("[0-9]+",sensor[0])
        sensors[time] = int(sensor[0])
tanks = tanks[1:-1]
sensors = sensors[1:-1]


#print(tanks)
#print(sensors)
   
# Plot or print that no counterexample was found
if len(tanks) != 0:
    # cut off at states we don't care about
    if len(tanks) > 170:
        tanks = tanks[0:170]
        sensors = sensors[0:170]
    time = np.arange(len(tanks))

    fig, ax = plt.subplots()
    ax.plot(time, tanks,label = "tank")
    ax.plot(time,sensors,label='tank sensor')

    ax.set(xlabel='time (s)', ylabel='tank height (cm)',
        title='nuXmv Trace')
    ax.grid()
    ax.legend()

    #fig.savefig("test.png")
    plt.show()
else:
    print("No Counterexample Found") 

# todo: add some way to choose or monitor current state 
#  ask user when they want to run the model check with nuxmv 
# encapsulate stuff into functions/ clean this up
