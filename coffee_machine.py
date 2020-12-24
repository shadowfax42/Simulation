
# a basic example: simulating a coffee machine usage where customer's interarrival time is 3 mins
import numpy as np
import simpy

def coffee_machine(env):
    customer_count = 0
    while True:
        yield env.timeout(np.random.exponential(3))
        customer_count += 1
        print(f"At {env.now:0.3f} minutes, customer {customer_count} used the coffee machine")
        
# create a simpy environment
env = simpy.Environment()

# initialize a simpy process
env.process(coffee_machine(env))

print("coffee machine simulation output:\n")

# Run the process
env.run(until=100)
