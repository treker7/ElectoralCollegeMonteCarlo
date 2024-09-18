from dataclasses import dataclass


@dataclass
class State:
    abbreviation: str
    electoral_points: int
    probability_red: float


@dataclass
class Year:
    states: list[State]
    battleground_state_abbreviations: set[str]
    red_consensus_points: int
    blue_consensus_points: int

    @property
    def battleground_states(self) -> list[State]:
        return [
            state
            for state in self.states
            if state.abbreviation in self.battleground_state_abbreviations
        ]
