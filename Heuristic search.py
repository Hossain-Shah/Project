from constraint import *
problem = Problem()
problem.addVariable('a', range(10))
problem.addVariable('b', range(10))
problem.addConstraint(lambda a, b: a * 2 == b)
solutions = problem.getSolutions()
print(solutions)
