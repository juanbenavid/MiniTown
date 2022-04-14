# Test to see how we can write an smv file

def writeState (tank,p1,p2):

    assignblock = "init(tank) :=" + str(tank) + "; \n" + "init(pump1) :=" + str(p1) + "; \n" + "init(pump2) :=" + str(p2) + "; \n"

    template = str(
    '''
MODULE main

DEFINE

pumpFlow0 := 0;
pumpFlow1 := 113.699 + 6.735*demand - 1.35* (tank/100);
pumpFlow2 := 181.44 + 18.356*demand - 2.1*(tank/100);

tankFlow0 := demand * 246 - pumpFlow0;
tankFlow1 := demand * 246 - pumpFlow1;
tankFlow2 := demand * 246 - pumpFlow2;

dT0 := tankFlow0 * 0.004678 *100;
dT1 := tankFlow1 * 0.004678 *100;
dT2 := tankFlow2 * 0.004678 *100;


VAR
pump1  : {on,off};
pump2  : {on,off};
demand : real;
tank   : real;
time   : integer;

ASSIGN
init(time) := 1;

    ''' ) + '\n' + assignblock + str(
    
    '''

next(pump1) := case

    next(tank) <= 400 : on;
    next(tank) >= 630: off;
    TRUE : pump1;
esac;

next(pump2) := case

    next(tank) <= 100 : on;
    next(tank) >= 450: off;
    TRUE : pump2;
esac;

next(time) := time + 1;
    
INVAR demand <= 1;
INVAR demand >= 0;

TRANS pump1 = off & pump2 = off -> next(tank) = tank - dT0;
TRANS pump1 = on & pump2 = off -> next(tank) = tank - dT1;
TRANS pump1 = on & pump2 = on -> next(tank) = tank - dT2;
TRANS pump1 = off & pump2 = on -> next(tank) = tank - dT1;

LTLSPEC G (time <= 5 -> tank <= 400); -- 0
LTLSPEC G (time <= 5 -> tank <= 550); -- 1
LTLSPEC G (time <= 5 -> tank <= 600); -- 2
LTLSPEC G (time <= 5 -> tank <= 650); -- 3

LTLSPEC G (time <= 5 -> tank >= 300); -- 4
LTLSPEC G (time <= 5 -> tank >= 200); -- 5
LTLSPEC G (time <= 5 -> tank >= 100); -- 6
LTLSPEC G (time <= 5 -> tank >= 25); -- 7
LTLSPEC G (time <= 5 -> tank >= 10); -- 8
    ''')

    with open("quickRun.smv", "w") as file1:
        # Writing data to a file
        file1.write(template)


def writeStateHack (tank,p1,p2):

    assignblock = "init(tank) :=" + str(tank) + "; \n" + "init(pump1) :=" + str(p1) + "; \n" + "init(pump2) :=" + str(p2) + "; \n"
    assignblock += "init(tankSensor) :=" + str(tank) + "; \n" + "init(actuator1) :=" + str(p1) + "; \n" + "init(actuator2) :=" + str(p2) + "; \n"

    template = str(
    '''
MODULE main

DEFINE

pumpFlow0 := 0;
pumpFlow1 := 113.699 + 6.735*demand - 1.35* (tank/100);
pumpFlow2 := 181.44 + 18.356*demand - 2.1*(tank/100);

tankFlow0 := demand * 246 - pumpFlow0;
tankFlow1 := demand * 246 - pumpFlow1;
tankFlow2 := demand * 246 - pumpFlow2;

dT0 := tankFlow0 * 0.004678 *100;
dT1 := tankFlow1 * 0.004678 *100;
dT2 := tankFlow2 * 0.004678 *100;


VAR
  pump1  : {on,off};
  pump2  : {on,off};
  demand : real;
  tank   : real;
  time   : integer;

  actuator1: {on,off};
  actuator2: {on,off};
  tankSensor: real;
  falseRead: {active,waiting};
  attackTime: 1..3;
  reading:{640,460,300,50};


ASSIGN

init(falseRead) := waiting;
init(time) := 0;

    ''' ) + '\n' + assignblock + str(
    
    '''

next(pump1) := next(actuator1);
next(pump2) := next(actuator2);

next(attackTime) := attackTime;
next(reading) := reading;

next(actuator1) := case

	next(tankSensor) <= 400 : on;
	next(tankSensor) >= 630 : off;
	TRUE : actuator1;
esac;

next(actuator2) := case

	next(tankSensor) <= 100 : on;
	next(tankSensor) >= 450 : off;
	TRUE : actuator2;
esac;

next(tankSensor) := case
	
	falseRead = active: reading;
	TRUE: next(tank);
esac;

next(falseRead) := case

	time >= attackTime -1 & time <= attackTime +1: active;
	TRUE: waiting; 

esac;

next(time) := time + 1;
	
INVAR demand <= 1;
INVAR demand >= 0;

TRANS pump1 = off & pump2 = off -> next(tank) = tank - dT0;
TRANS pump1 = on & pump2 = off -> next(tank) = tank - dT1;
TRANS pump1 = on & pump2 = on -> next(tank) = tank - dT2;
TRANS pump1 = off & pump2 = on -> next(tank) = tank - dT1;

LTLSPEC G (time <= 5 -> tank <= 400); -- 0
LTLSPEC G (time <= 5 -> tank <= 550); -- 1
LTLSPEC G (time <= 5 -> tank <= 600); -- 2
LTLSPEC G (time <= 5 -> tank <= 650); -- 3

LTLSPEC G (time <= 5 -> tank >= 300); -- 4
LTLSPEC G (time <= 5 -> tank >= 200); -- 5
LTLSPEC G (time <= 5 -> tank >= 100); -- 6
LTLSPEC G (time <= 5 -> tank >= 25); -- 7
LTLSPEC G (time <= 5 -> tank >= 10); -- 8
    ''')

    with open("quickRunHacker.smv", "w") as file1:
        # Writing data to a file
        file1.write(template)

writeStateHack(300,'on','off')

