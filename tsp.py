#!/usr/bin/env python
# coding: utf-8

# Imports
from logging import NullHandler
from os import stat
from pyomo.environ import *
from pyomo.opt import *
from pyomo.core import * 

class TSP:

    def __init__(self):
        self.model = None
        self.subset_constraints = []

    # Objective rule: Minimize total distance
    def objective_rule(self, model):
        
        return sum(model.SELECT[i, j] * model.distance[i, j] for i in model.i for j in model.i)

    def one_successor_rule(self, model, i):
        
        # Must have an exact one successor
        return sum(model.SELECT[i, j] for j in model.i if j != i) == 1

    def one_predecessor_rule(self, model, j):
        
        # Must have an exact one predecessor
        return sum(model.SELECT[i, j] for i in model.i if i != j) == 1

    def subset_rule(self, model, subset_index):
        subset = self.subset_constraints[subset_index]
        return sum(model.SELECT[i, j] for i in subset for j in subset if i != j) <= (len(subset) - 1)

    def pyomo_create_model(self, distance, n):

        # Create concrete model
        self.model = ConcreteModel()

        # Define set of index
        self.model.i = Set(initialize=[i for i in range(1, n+1)], ordered = True)
        self.model.subset_index = Set(ordered = True)

        # Define decision variable (n x n)
        self.model.SELECT = Var((self.model.i * self.model.i), domain=Binary, initialize = 0)

        # Define parameters
        self.model.distance = Param((self.model.i * self.model.i), initialize = distance)

        # Objective function
        self.model.objective = Objective(rule = self.objective_rule, sense = minimize)

        # Constraints
        self.model.successorConstraint = Constraint(self.model.i, rule=self.one_successor_rule)
        self.model.predecessorConstraint = Constraint(self.model.i, rule=self.one_predecessor_rule)
        self.model.subsetConstraint = Constraint(self.model.subset_index, rule=self.subset_rule)
        
        return self.model

    def run_model(self, distance, n, verbose):
        # Create model
        model = self.pyomo_create_model(distance, n)

        # Initialize solver
        opt = SolverFactory("glpk")

        # Solve the model
        iteration = 1
        if verbose:
            print(f"Solving model at iteration {iteration}...", end="\r")
        results = opt.solve(model)

        # Get the cycle that includes 1
        cycle = self.get_list_cycle(model, n)

        # Subtour elimination if necessary
        while len(cycle) != 1:
            
            # Increment the iteration number
            iteration += 1
            
            # Add the subset to the constraints and redefine constraint
            self.subset_constraints += cycle
            for i in cycle:
                if model.subset_index.ordered_data().count(0) == 0:
                    model.subset_index.add(0)
                else:
                    model.subset_index.add(model.subset_index.ordered_data()[-1] + 1)
            model.subsetConstraint.clear()
            model.subsetConstraint._constructed = False
            model.subsetConstraint.construct()
            
            # Re solve the model
            if verbose:
                print(f"Solving model at iteration {iteration}...", end="\r")
            results = opt.solve(model)
                
            # Re evaluate cycle
            cycle = self.get_list_cycle(model, n)
        
        return model

    @staticmethod
    def get_list_cycle(model, n):
        '''
        Function to get all cycles in our model
        '''
        # Initialize necessary variables
        visited = []
        cycle_list = []
        
        while len(visited) < n:
            
            # find which city that hasn't been visited
            idx = [i for i in model.i.ordered_data() if i not in visited][0]
            
            cycle = TSP.get_cycle_starting_from_idx(model, idx) # function defined below
            
            # add the subset to cycle_list
            cycle_list.append(cycle)
            
            # add each visited cities to visited array
            visited += cycle
            
        return cycle_list

    @staticmethod
    def get_cycle_starting_from_idx(model, idx):
        
        '''
        Function to get cycle from a given city
        '''
        subset = set()
        
        # starting city
        subset.add(idx)
        i = idx
        
        # find where i goes to
        for j in model.i.ordered_data():
            if model.SELECT[i, j].value == 1:
                subset.add(j)
                break

        # While we're not back to the starting city
        while j != idx:
            
            # Go to the next city and add it to the cycle
            i = j
            for j in model.i.ordered_data():
                if model.SELECT[i, j].value == 1:
                    subset.add(j)
                    break
        return list(subset)  # list of visited cities
