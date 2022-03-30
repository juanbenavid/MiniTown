# Script to print transition values for finite NuXmv model

import numpy as np
import matplotlib.pyplot as plt
import math

# Equations we got through
# hardy cross and EPAnet regressions:

'''
pumpFlow0 := 0;
pumpFlow1 := 113.699 + 6.735*demand - 1.35* (tank/100);
pumpFlow2 := 181.44 + 18.356*demand - 2.1*(tank/100);

tankFlow0 := demand * 246 - pumpFlow0;
tankFlow1 := demand * 246 - pumpFlow1;
tankFlow2 := demand * 246 - pumpFlow2;

dT0 := tankFlow0 * 0.004678 *100;
dT1 := tankFlow1 * 0.004678 *100;
dT2 := tankFlow2 * 0.004678 *100;

'''

def PumpFlow(tankLevel,demand,pumps):
    if pumps == 1.0:
        return (113.699 + 6.735*demand) - 1.35*tankLevel
    elif pumps == 2.0:
        return (181.44 + 18.356*demand) - 2.16*tankLevel
    else:
        return 0

# Change in water tank height from flow:

def DWL(q,r):
    v = q * 3600      # /4 = 15 mins
    return v/math.pi/(r**2)/1000

tank_dia = 31.3
tank_rad = tank_dia/2
Qmax = 208

# Dictionary of discrete values for change in tank height:

def disc_rels():
    rels_dic = {}
    rels_dic[1.0] = {}   # create subdictioncaries for 1 pump, 2 pumps , 0 pumps
    rels_dic[2.0] = {}
    rels_dic[0.0] = {}
    for i in [0,0.25,0.5,0.75,1.0]:  # create subdictionaries for each demand level
        rels_dic[1.0][i] = {}        
        rels_dic[2.0][i] = {}
        rels_dic[0.0][i] = {}
        for j in np.arange(0,660)/100:
                for p in [0.0,1.0,2.0]: # create subdicitonaries for each tank level (arbitrary increments)
                    tq = i * 246 - PumpFlow(j,i,p)
                    dh = round(DWL(tq,tank_rad),2)
                    if j - dh < 0:
                        dh = j
                    elif j - dh > 6.5:
                        dh = -1*(6.5-j)
                    rels_dic[p][i][j] = dh
    return rels_dic


Delta_tank= disc_rels()
DistinctFlows = [[],[],[]]

prev = Delta_tank[1.0][0][0.0]
prevT = 0.0
curr = Delta_tank[1.0][0][0.0]
currT = 0.0        

for p in Delta_tank:
    for d in Delta_tank[p]:
        prev = Delta_tank[p][d][0.0]
        prevT = 0.0
        curr = Delta_tank[p][d][0.0]
        currT = 0.0
        for t in Delta_tank[p][d]:
            #print("pump:",p," demand:",d," tank:",t, " Flow:", curr)
            if curr != prev:
                if p == 0.0:
                    print("TRANS pump1 = off & pump2 = off & demand =",int(d*100),"& tank >=",int(prevT*100), "& tank <",int(currT*100),"-> next(tank) = tank -", int(round(prev*100,1)),";")
                elif p == 1.0:
                    print("TRANS pump1 = off & pump2 = on & demand = ",int(d*100), "& tank >=",int(prevT*100), "& tank <",int(currT*100),"-> next(tank) = tank -", int(round(prev*100,1)),";")
                    print("TRANS pump1 = on & pump2 = off & demand = ",int(d*100), " & tank >=",int(prevT*100), "& tank <",int(currT*100),"-> next(tank) = tank -", int(round(prev*100,1)),";") 
                elif p == 2.0:
                    print("TRANS pump1 = on & pump2 = on & demand =",int(d*100), " & tank >=",int(prevT*100), "& tank <",int(currT*100),"-> next(tank) = tank -", int(round(prev*100,1)),";")
                prev = curr
                prevT = currT
            if t == 6.59:
                if p == 0.0:
                    print("TRANS pump1 = off & pump2 = off & demand =",int(d*100),"& tank >=",int(prevT*100), "& tank <",660,"-> next(tank) = tank -", int(round(prev*100,1)),";")
                elif p == 1.0:
                    print("TRANS pump1 = off & pump2 = on & demand = ",int(d*100), "& tank >=",int(prevT*100), "& tank <",660,"-> next(tank) = tank -", int(round(prev*100,1)),";")
                    print("TRANS pump1 = on & pump2 = off & demand = ",int(d*100), " & tank >=",int(prevT*100), "& tank <",660,"-> next(tank) = tank -", int(round(prev*100,1)),";") 
                elif p == 2.0:
                    print("TRANS pump1 = on & pump2 = on & demand =",int(d*100), " & tank >=",int(prevT*100), "& tank <",660,"-> next(tank) = tank -", int(round(prev*100,1)),";")
            curr = Delta_tank[p][d][t]
            currT = t
            
            

        