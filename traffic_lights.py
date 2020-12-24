# traffic light simulation
import simpy
import numpy as np

def traffic_lights_process(env):
    
    while True:
        print("Light turned green at t=" + str(env.now))
        green_light_duration = 60
        yield env.timeout(green_light_duration)
        
        print("Light turned yellow at t=" + str(env.now))
        yellow_light_duration = 10
        yield env.timeout(yellow_light_duration)
        
        print("Light turned red at t=" + str(env.now))
        red_light_duration = 40
        yield env.timeout(red_light_duration)

#set a seed to reproduce the results
np.random.seed(0)

#create a simpy environment
env = simpy.Environment()

#instantiate a simpy process
env.process(traffic_lights_process(env))

print("Traffic light simulation begins")

#run the process for 1000 seconds
env.run(until=1000)

print("Traffic light simulation completes")
