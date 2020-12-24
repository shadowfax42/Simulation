# clothing store simulation
import simpy

class Store(object):
    def __init__(self, env, num_items, holding_time):
        self.env =  env
        self.items = simpy.Resource(env, num_items)
        self.holding_time =  holding_time
        
    def send_order(self, customer):
        print(f"sending item for {customer}")
        yield self.env.timeout(self.holding_time)
        print(f"item from {customer} returns to the store")
        
def order(env, customer, store):
    print(f"{customer} is requesting an item")
    
    with store.items.request() as request:
        yield request
        yield env.process(store.send_order(customer))
        
        
def setup(env, num_items, holding_time, order_period):
    store = Store(env, num_items, holding_time)
    num_customers = 10
    for i in range(1,num_customers):
        env.process(order(env, 'Customer %d' % i, store))
        
    while True:
        yield env.timeout(order_period)
        i += 1
        env.process(order(env, 'Customer %d' % i, store))
        
NUM_ITEMS = 100    # number of items in the store
HOLDING_TIME = 2  # how long the customer is keeping the item in days
ORDER_PERIOD = 3  # time period between each order    

env = simpy.Environment()
env.process(setup(env, NUM_ITEMS, HOLDING_TIME, ORDER_PERIOD))

# run the simulation for 7 days
env.run(until=7)
