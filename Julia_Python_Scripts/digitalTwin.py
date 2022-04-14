from cProfile import label
import os
import subprocess as sp
import re
from tkinter import BASELINE
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time as timewait

from writesmv import *

'''
Specs to check:

Does tank ever go above...:
LTLSPEC G (time <= 5 -> tank <= x); -- 0

Does tank ever go below ...:
LTLSPEC G (time <= 5 -> tank >= x); -- 3

'''
while True:
    print(" \n ")
    print("*********nuXmV Minitown Reachability Checking *********")
    print(" ")
    print("----- Regular Operations------")
    print(" ")

    tankState = input("Tank Height:")
    pump1 = input ("Pump1:")
    pump2 = input("Pump2:")
    heightCheck = int(input("reachability bound:"))
    writeState(tankState,pump1,pump2)
    writeStateHack(tankState,pump1,pump2)
    tankState = int(tankState)

    if heightCheck > tankState:

        check = str("msat_check_ltlspec_bmc -p \" G (time <5 -> tank <=" + str(heightCheck) + ")\"")

        with open("cmds.txt", "w") as file1:
            # Writing data to a file
            file1.write("read_model -i quickRun.smv ; set msat_dump_frac_as_float 1; go_msat ;"+str(check)+";quit")
        
        print("Launching NuXmv - This may take a minute")
        nuxmv = sp.Popen('nuxmv -source cmds.txt',stdout=sp.PIPE,universal_newlines=True)
        output = nuxmv.stdout.read()
        print(output)

    elif heightCheck < tankState:
        check = str("msat_check_ltlspec_bmc -p \" G (time <5 -> tank >=" + str(heightCheck) + ")\"")
        with open("cmds.txt", "w") as file1:
            # Writing data to a file
            file1.write("read_model -i quickRun.smv ; set msat_dump_frac_as_float 1; go_msat ;"+str(check)+";quit")

        print("Launching NuXmv - This may take a minute")
        nuxmv = sp.Popen('nuxmv -source cmds.txt',stdout=sp.PIPE,universal_newlines=True)
        output = nuxmv.stdout.read()

        print(output)
    else:
        print("try asking something that makes sense")
        continue

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
    tanks = tanks[1:]
    sensors = sensors[1:]


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
        #ax.plot(time,sensors,label='tank sensor')
        ax.plot(time,np.ones(len(time))*heightCheck, label = "check")

        ax.set(xlabel='time (hrs)', ylabel='tank height (cm)',
            title='nuXmv Trace Infinite Precision')
        ax.grid()
        ax.legend()

        plt.show()
    else:
        print("No Counterexample Found - System is SAFE (up to 5 hours)") 

    timewait.sleep(4)

    print(" ")
    print("----- With Possible Cyber Attacks------")
    print(" ")

    if heightCheck > tankState:

        check = str("msat_check_ltlspec_bmc -p \" G (time <5 -> tank <=" + str(heightCheck) + ")\"")

        with open("cmds.txt", "w") as file1:
            # Writing data to a file
            file1.write("read_model -i quickRunHacker.smv ; set msat_dump_frac_as_float 1; go_msat ;"+str(check)+";quit")
        
        print("Launching NuXmv - This may take a minute")
        nuxmv = sp.Popen('nuxmv -source cmds.txt',stdout=sp.PIPE,universal_newlines=True)
        output = nuxmv.stdout.read()
        print(output)

    elif heightCheck < tankState:
        check = str("msat_check_ltlspec_bmc -p \" G (time <5 -> tank >=" + str(heightCheck) + ")\"")
        with open("cmds.txt", "w") as file1:
            # Writing data to a file
            file1.write("read_model -i quickRunHacker.smv ; set msat_dump_frac_as_float 1; go_msat ;"+str(check)+";quit")

        print("Launching NuXmv - This may take a minute")
        nuxmv = sp.Popen('nuxmv -source cmds.txt',stdout=sp.PIPE,universal_newlines=True)
        output = nuxmv.stdout.read()

        print(output)
    else:
        print("try asking something that makes sense")
        continue

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
    tanks = tanks[1:]
    sensors = sensors[1:]


    #print(tanks)
    #print(sensors)
    
    # Plot or print that no counterexample was found
    if len(tanks) != 0:
        time = np.arange(len(tanks))

        fig, ax = plt.subplots()
        ax.plot(time, tanks,label = "tank")
        ax.plot(time,sensors,label='tank sensor')
        ax.plot(time,np.ones(len(time))*heightCheck, label = "check")

        ax.set(xlabel='time (hrs)', ylabel='tank height (cm)',
            title='nuXmv Trace Infinite Precision')
        ax.grid()
        ax.legend()

        plt.show()
    else:
        print("No Counterexample Found - System is SAFE (up to 5 hours)") 


