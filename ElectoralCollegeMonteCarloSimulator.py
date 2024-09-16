import random
import sys

from ElectoralCollege2024 import *

class ElectoralCollegeResult():
    def __init__(self, redElectoralPoints, blueElectoralPoints):
        self.redElectoralPoints = redElectoralPoints
        self.blueElectoralPoints = blueElectoralPoints

    def isRedWin(self):
        return self.redElectoralPoints >= 270

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
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <num_iterations>")
        return -1

    numIterations = int(sys.argv[1])

    print("<<< Electoral College Monte Carlo Simulations >>>\n")
    simulator = ElectoralCollegeMonteCarloSimulator(BATTLEGROUND_ELECTORAL_COLLEGE_STATES,
                                                    CONSENSUS_ELECTORAL_POINTS_RED, CONSENSUS_ELECTORAL_POINTS_BLUE)
    
    simulations = simulator.runMonteCarloSimulations(numIterations)
    probabilityRedWin = len(list(filter(lambda s: s.isRedWin(), simulations))) / len(simulations)
    probabilityBlueWin = 1 - probabilityRedWin

    print(f"Expected value of red points = {simulator.getExpectedPointsRed()}.")
    print(f"Expected value of blue points = {simulator.getExpectedPointsBlue()}.")

    print(f"Probablility red win = {100 * probabilityRedWin}%.")
    print(f"Probablility blue win = {100 * probabilityBlueWin}%.")

    return 0


main()