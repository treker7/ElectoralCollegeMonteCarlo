import random
import sys
import statistics

from ElectoralCollege2024 import *

class ElectoralCollegeResult():
    def __init__(self, redElectoralPoints, blueElectoralPoints):
        self.redElectoralPoints = redElectoralPoints
        self.blueElectoralPoints = blueElectoralPoints

    def isRedWin(self):
        return self.redElectoralPoints >= 270
    
    def isBlueWin(self):
        return self.blueElectoralPoints >= 270
    
    def isTie(self):
        return (self.blueElectoralPoints < 270) and (self.redElectoralPoints < 270)

class ElectoralCollegeMonteCarloSimulator():
    def __init__(self, electoralCollegeStates, consensusPointsRed = 0, consensusPointsBlue = 0):
        self.electoralCollegeStates = electoralCollegeStates
        self.consensusPointsRed = consensusPointsRed
        self.consensusPointsBlue = consensusPointsBlue
    
    def getExpectedPointsRed(self):
        return self.consensusPointsRed + sum((s.probabilityRed * s.electoralPoints) for s in self.electoralCollegeStates)
    
    def getExpectedPointsBlue(self):
        return self.consensusPointsBlue + sum(((1 - s.probabilityRed) * s.electoralPoints) for s in self.electoralCollegeStates)
    
    def sampleElectoralCollege(self):
        redElectoralPoints = self.consensusPointsRed
        blueElectoralPoints = self.consensusPointsBlue
        for state in self.electoralCollegeStates:
            if random.random() < state.probabilityRed:
                redElectoralPoints += state.electoralPoints
            else:
                blueElectoralPoints += state.electoralPoints
        
        return ElectoralCollegeResult(redElectoralPoints, blueElectoralPoints)
        
    def runMonteCarloSimulations(self, numIterations = 100000):
        monteCarloSimulations = []
        for i in range(numIterations):
            monteCarloSimulations.append(self.sampleElectoralCollege())

        return monteCarloSimulations

def main():
    if (len(sys.argv) < 2) or (len(sys.argv) > 3):
        print(f"Usage: {sys.argv[0]} <num_iterations> [-a]")
        return -1

    numIterations = int(sys.argv[1])
    simulateAllStates = (len(sys.argv) == 3) and (sys.argv[2] == "-a")

    if simulateAllStates:
        simulator = ElectoralCollegeMonteCarloSimulator(ALL_ELECTORAL_COLLEGE_STATES)
    else:
        simulator = ElectoralCollegeMonteCarloSimulator(BATTLEGROUND_ELECTORAL_COLLEGE_STATES, CONSENSUS_ELECTORAL_POINTS_RED, CONSENSUS_ELECTORAL_POINTS_BLUE)

    print("<<< Electoral College Monte Carlo Simulations >>>\n")
    simulations = simulator.runMonteCarloSimulations(numIterations)

    simulationsRedWin = list(filter(lambda s: s.isRedWin(), simulations))
    simulationsBlueWin = list(filter(lambda s: s.isBlueWin(), simulations))
    simulationsTie = list(filter(lambda s: s.isTie(), simulations))

    probabilityRedWin = len(simulationsRedWin) / len(simulations)
    probabilityBlueWin = len(simulationsBlueWin) / len(simulations)
    probabilityTie = len(simulationsTie) / len(simulations)

    medianElectoralPointsRedWin = statistics.median([s.redElectoralPoints for s in simulationsRedWin])
    medianElectoralPointsBlueWin = statistics.median([s.blueElectoralPoints for s in simulationsBlueWin])

    print(f"Probability of red win = {100 * probabilityRedWin:.2f}%")
    print(f"Probability of blue win = {100 * probabilityBlueWin:.2f}%")
    print(f"Probability of tie = {100 * probabilityTie:.2f}%")
    print()

    print(f"Median electoral college vote for red wins = {medianElectoralPointsRedWin}")
    print(f"Median electoral college vote for blue wins = {medianElectoralPointsBlueWin}")

    return 0


main()