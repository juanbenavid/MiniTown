# Script to run WINTR simulations and compare to NuXmv 
# NuXmv is not modelled directly but a NuXmv "simulator" is made

import wntr
import wntr.network.controls as controls
import numpy as np
import matplotlib.pyplot as plt

minitown = wntr.network.WaterNetworkModel('minitown_juan75.inp')
minitown.options.time.duration = 604800
tank = minitown.get_node('TANK')
tank.init_level = 5.0
sim = wntr.sim.EpanetSimulator(minitown)
results = sim.run_sim()

tank = minitown.get_node('TANK')
tank_height = results.node['pressure'].loc[:,'TANK']
#flow_p1 = results.link['flowrate'].loc[:, 'PUMP1']*1000     #get flowrate through PUMP1 for all times, convert from m^3/s -> LPS
#flow_p2 = results.link['flowrate'].loc[:, 'PUMP2']*1000     #get flowrate through PUMP1 for all times, convert from m^3/s -> LPS
#print(tank_height)

def nuxmv(time,demand,tanki,step):
    tank = tanki
    times  = np.array([0])
    tanks = np.array([tanki])
    pumps1 = []
    pumps2 = []
    pump1 = True
    pump2 = False
    for i in range(1,time*step):
        pumpFlow0 = 0
        pumpFlow1 = 113.699 + 6.735*demand - 1.35* (tank/100)
        pumpFlow2 = 181.44 + 18.356*demand - 2.16*(tank/100)

        tankFlow0 = demand * 208 - pumpFlow0
        tankFlow1 = demand * 208 - pumpFlow1
        tankFlow2 = demand * 208 - pumpFlow2

        #dT0 = np.floor(tankFlow0 * (0.004679/step) *100)
        #dT1 = np.floor(tankFlow1 * (0.004679/step) *100)
        #dT2 = np.floor(tankFlow2 * (0.004679/step) *100)
        
        #dT0 = round(tankFlow0 * (0.004679/step) *100)
        #dT1 = round(tankFlow1 * (0.004679/step) *100)
        #dT2 = round(tankFlow2 * (0.004679/step) *100)
        
        dT0 = tankFlow0 * (0.004679/step) *100
        dT1 = tankFlow1 * (0.004679/step) *100
        dT2 = tankFlow2 * (0.004679/step) *100
        
        if (not pump1) and (not pump2):
            tank -= dT0
        elif (not pump1) and pump2:
            tank -= dT1
        elif pump1 and (not pump2):
            tank -= dT1
        elif pump1 and pump2:
            tank -= dT2
            
        if tank <= 400:
            pump1 = True
        elif tank >= 630:
            pump1 = False
            
        if tank <= 100:
            pump2 = True
        elif tank >= 450:
            pump2 = False

        
        times = np.append(times,i)
        tanks = np.append(tanks,tank)
        pumps1.append(pump1)
        pumps2.append(pump2)
        
    return times/step,tanks/100,pumps1,pumps2


time,tank,p1,p2 = nuxmv(175,0.75,500.0,1)


# Plot against WINTR
plt.plot(np.arange(0,169),tank_height,label="WINTR")
plt.plot(time,tank, label = "nuXmv python")
plt.legend()

# To get a NuXmv style trace:
print("Time----Pump1-----Pump2-----Tank")
for i in range(0,100):
    print(time[i],"----",p1[i],"----",p2[i],"----",tank[i])

