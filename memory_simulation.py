#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random


MEMORY_SIZE = 256 
UNIT_SIZE = 2  
NUM_UNITS = MEMORY_SIZE // UNIT_SIZE

class Memory:
    def __init__(self):
        self.memory = [0] * NUM_UNITS
        self.processes = {}

    def allocate_mem_first_fit(self, process_id, num_units):
        for i in range(NUM_UNITS - num_units + 1):
            if all(self.memory[i+j] == 0 for j in range(num_units)):
                for j in range(num_units):
                    self.memory[i+j] = process_id
                self.processes[process_id] = (i, num_units)
                return i
        return -1

    def allocate_mem_next_fit(self, process_id, num_units, last_allocation):
        for i in range(last_allocation, NUM_UNITS):
            if i + num_units <= NUM_UNITS and all(self.memory[i+j] == 0 for j in range(num_units)):
                for j in range(num_units):
                    self.memory[i+j] = process_id
                self.processes[process_id] = (i, num_units)
                return i
        for i in range(last_allocation):
            if i + num_units <= last_allocation and all(self.memory[i+j] == 0 for j in range(num_units)):
                for j in range(num_units):
                    self.memory[i+j] = process_id
                self.processes[process_id] = (i, num_units)
                return i
        return -1

    def allocate_mem_best_fit(self, process_id, num_units):
        best_fit_index = -1
        best_fit_size = float('inf')
        for i in range(NUM_UNITS - num_units + 1):
            if all(self.memory[i+j] == 0 for j in range(num_units)):
                free_space_size = sum(1 for j in range(NUM_UNITS) if self.memory[j] == 0 and j >= i and j < i + num_units)
                if free_space_size < best_fit_size:
                    best_fit_index = i
                    best_fit_size = free_space_size
        if best_fit_index != -1:
            for j in range(num_units):
                self.memory[best_fit_index+j] = process_id
            self.processes[process_id] = (best_fit_index, num_units)
            return best_fit_index
        return -1

    def allocate_mem_worst_fit(self, process_id, num_units):
        worst_fit_index = -1
        worst_fit_size = -1
        for i in range(NUM_UNITS - num_units + 1):
            if all(self.memory[i+j] == 0 for j in range(num_units)):
                free_space_size = sum(1 for j in range(NUM_UNITS) if self.memory[j] == 0 and j >= i and j < i + num_units)
                if free_space_size > worst_fit_size:
                    worst_fit_index = i
                    worst_fit_size = free_space_size
        if worst_fit_index != -1:
            for j in range(num_units):
                self.memory[worst_fit_index+j] = process_id
            self.processes[process_id] = (worst_fit_index, num_units)
            return worst_fit_index
        return -1

    def deallocate_mem(self, process_id):
        if process_id in self.processes:
            start, num_units = self.processes[process_id]
            for i in range(num_units):
                self.memory[start + i] = 0
            del self.processes[process_id]
            return 1
        return -1

    def fragment_count(self):
        count = 0
        i = 0
        while i < NUM_UNITS:
            if self.memory[i] == 0:
                count += 1
                i += 1
            elif self.memory[i] in self.processes:
                i += self.processes[self.memory[i]][1]
            else:
                i += 1
        return count

    
class RequestGenerator:
    def __init__(self):
        self.process_id = 1

    def generate_request(self):
        action = random.choice(['allocate', 'deallocate'])
        if action == 'allocate':
            num_units = random.randint(3, 10)
            return action, self.process_id, num_units
        else:
            return action, self.process_id

        self.process_id += 1

        
def report_statistics(memory, technique):
    fragment_avg = memory.fragment_count() / NUM_UNITS
    total_allocations = len(memory.processes)
    total_nodes_traversed = sum(memory.processes[pid][0] for pid in memory.processes)
    allocation_avg = total_nodes_traversed / total_allocations if total_allocations > 0 else 0
    denied_percentage = (1 - total_allocations / NUM_UNITS) * 100

    print(f"Technique: {technique}")
    print(f"Average number of external fragments: {fragment_avg}")
    print(f"Average allocation time: {allocation_avg}")
    print(f"Percentage of denied allocation requests: {denied_percentage}%")
    print()


def simulate(technique):
    memory = Memory()
    request_generator = RequestGenerator()
    last_allocation = 0

    for _ in range(10000):
        action, *params = request_generator.generate_request()
        if action == 'allocate':
            if technique == "First Fit":
                memory.allocate_mem_first_fit(*params)
            elif technique == "Next Fit":
                last_allocation = memory.allocate_mem_next_fit(*params, last_allocation)
            elif technique == "Best Fit":
                memory.allocate_mem_best_fit(*params)
            elif technique == "Worst Fit":
                memory.allocate_mem_worst_fit(*params)
        elif action == 'deallocate':
            memory.deallocate_mem(*params)

    report_statistics(memory, technique)


simulate("First Fit")
simulate("Next Fit")
simulate("Best Fit")
simulate("Worst Fit")


# In[ ]:




