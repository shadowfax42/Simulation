# (s,S) inventory simulation
import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
sns.set()

h = 2.0
r = 100
L = 2.0

def warehouse_run(env, order_cutoff, order_target):
    global inventory, balance, num_ordered
    
    inventory = order_target
    balance = 0.0
    num_ordered = 0
    
    while True:
        interarrival = generate_interarrival()
        yield env.timeout(interarrival)
        balance -= inventory * h * interarrival
        demand = generate_demand()
        if demand < inventory:
            # sell equal to demand, increase balance and decrease inventory
            balance += r*demand
            inventory -= demand
            print(f"{env.now:.2f} Sold {demand}")
        else:
            # sell what we can, reduce inventory to 0
            balance += r*inventory
            inventory = 0
            print(f"{env.now:.2f} Sold {inventory}, now out of stock")
        
        if inventory < order_cutoff and num_ordered==0:
            # if inventory is below safety level and we haven't ordered
            # new inventory yet, then we want to place a new order
            env.process(handle_order(env, order_target))

def handle_order(env, order_target):
    global inventory, balance, num_ordered
    
    num_ordered = order_target - inventory # calculate # of inventory to order
    print(f"{env.now:.2f} We placed an order for {num_ordered} units")
    cost = 50 * num_ordered # calculate cost of order
    balance -= cost # subtact cost of order from profit balance
    yield env.timeout(L) # wait for delay period
    inventory += num_ordered # reset inventory to previous inventory + new inventory
    num_ordered = 0 # reset number of inventory to order back to 0
    print(f"{env.now:.2f} received order of {num_ordered} units")
    
def generate_interarrival():
    return np.random.exponential(1./5) # lambda = 5

def generate_demand():
    return np.random.randint(1,5)

obs_time = []
inventory_level = []

def observe(env):
    global inventory
    
    while True:
        obs_time.append(env.now)
        inventory_level.append(inventory)
        yield env.timeout(0.1) # record observations 10 times a day
    

np.random.seed(77)
env = simpy.Environment()

s = 10
S = 30
env.process(warehouse_run(env, s, S))
env.process(observe(env))
env.run(until=5.0)
