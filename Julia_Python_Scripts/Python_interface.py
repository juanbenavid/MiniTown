## Testing a possible Python Interface for NuXmv
## Ongoing Process
## Juan Benavides 3/28/2022

import os
import subprocess as sp
import re
import matplotlib.pyplot as plt
import numpy as np

print("Launching NuXmv")
nuxmv = sp.Popen('nuxmv -n 3 Cyber.smv ',stdout=sp.PIPE,universal_newlines=True)
output = nuxmv.stdout.read()

print("Tank States:")
tank = re.findall("tank = [0-9]+",output)

for ind,state in enumerate(tank):
    tank[ind] = int(re.findall("[0-9]+",state)[0])
print(tank)

if len(tank) != 0:
    # cut off at states we don't care about
    if len(tank) > 170:
        tank = tank[0:170]
    time = np.arange(len(tank))

    fig, ax = plt.subplots()
    ax.plot(time, tank)

    ax.set(xlabel='time (s)', ylabel='tank height (cm)',
        title='nuXmv Trace')
    ax.grid()

    #fig.savefig("test.png")
    plt.show()
else:
    print("No Counterexample Found")

