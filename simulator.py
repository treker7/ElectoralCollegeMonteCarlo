import argparse
import random
import statistics
from dataclasses import dataclass
from typing import Generator

from electoral_college_2024 import (
    ALL_ELECTORAL_COLLEGE_STATES,
    BATTLEGROUND_ELECTORAL_COLLEGE_STATES,
    CONSENSUS_ELECTORAL_POINTS_BLUE,
    CONSENSUS_ELECTORAL_POINTS_RED,
    ElectoralCollegeState,
)


@dataclass
class ElectoralCollegeResult:
    red_points: int
    blue_points: int

    @property
    def is_red_win(self) -> bool:
        return self.red_points >= 270

    @property
    def is_blue_win(self) -> bool:
        return self.blue_points >= 270

    @property
    def is_tie(self) -> bool:
        return not self.is_blue_win and not self.is_red_win


class Simulator:
    def __init__(
        self,
        states: list[ElectoralCollegeState],
        consensus_points_red: int = 0,
        consensus_points_blue: int = 0,
    ):
        self.electoral_college_states = states
        self.consensus_points_red = consensus_points_red
        self.consensus_points_blue = consensus_points_blue

    @property
    def red_expected_points(self) -> float:
        return self.consensus_points_red + sum(
            (state.probability_red * state.electoral_points)
            for state in self.electoral_college_states
        )

    @property
    def blue_expected_points(self) -> float:
        return self.consensus_points_blue + sum(
            ((1 - state.probability_red) * state.electoral_points)
            for state in self.electoral_college_states
        )

    def sample_electoral_college(self) -> ElectoralCollegeResult:
        red_electoral_points = self.consensus_points_red
        blue_electoral_points = self.consensus_points_blue
        for state in self.electoral_college_states:
            if random.random() < state.probability_red:
                red_electoral_points += state.electoral_points
            else:
                blue_electoral_points += state.electoral_points

        return ElectoralCollegeResult(red_electoral_points, blue_electoral_points)

    def generate_simulations(
        self, num_iterations: int = 100_000
    ) -> Generator[ElectoralCollegeResult, None, None]:
        return (self.sample_electoral_college() for _ in range(num_iterations))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("num_iterations", type=int)
    parser.add_argument("-a", "--allstates", action="store_true")

    args = parser.parse_args()

    if args.allstates:
        simulator = Simulator(ALL_ELECTORAL_COLLEGE_STATES)
    else:
        simulator = Simulator(
            BATTLEGROUND_ELECTORAL_COLLEGE_STATES,
            CONSENSUS_ELECTORAL_POINTS_RED,
            CONSENSUS_ELECTORAL_POINTS_BLUE,
        )

    print("<<< Electoral College Monte Carlo Simulations >>>\n")
    simulations = list(simulator.generate_simulations(args.num_iterations))

    red_win_simulations = [
        simulation for simulation in simulations if simulation.is_red_win
    ]
    blue_win_simulations = [
        simulation for simulation in simulations if simulation.is_blue_win
    ]
    tie_simulations = [simulation for simulation in simulations if simulation.is_tie]

    red_win_probability = len(red_win_simulations) / len(simulations)
    blue_win_probability = len(blue_win_simulations) / len(simulations)
    tie_probability = len(tie_simulations) / len(simulations)

    median_red_win_electoral_points = (
        statistics.median([simulation.red_points for simulation in red_win_simulations])
        if red_win_simulations
        else 0
    )
    median_blue_win_electoral_points = (
        statistics.median(
            [simulation.blue_points for simulation in blue_win_simulations]
        )
        if blue_win_simulations
        else 0
    )

    print(f"Probability of red win = {100 * red_win_probability:.2f}%")
    print(f"Probability of blue win = {100 * blue_win_probability:.2f}%")
    print(f"Probability of tie = {100 * tie_probability:.2f}%")
    print()

    print(
        f"Median electoral college vote for red wins = {median_red_win_electoral_points}"
    )
    print(
        f"Median electoral college vote for blue wins = {median_blue_win_electoral_points}"
    )


if __name__ == "__main__":
    main()
