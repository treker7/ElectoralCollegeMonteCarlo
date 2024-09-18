from dataclasses import dataclass
from enum import StrEnum


class StateAbbreviation(StrEnum):
    ALABAMA = "AL"
    ALASKA = "AK"
    ARIZONA = "AZ"
    ARKANSAS = "AR"
    CALIFORNIA = "CA"
    COLORADO = "CO"
    CONNECTICUT = "CT"
    DELAWARE = "DE"
    FLORIDA = "FL"
    GEORGIA = "GA"
    HAWAII = "HI"
    IDAHO = "ID"
    ILLINOIS = "IL"
    INDIANA = "IN"
    IOWA = "IA"
    KANSAS = "KS"
    KENTUCKY = "KY"
    LOUISIANA = "LA"
    MAINE = "ME"
    MARYLAND = "MD"
    MASSACHUSETTS = "MA"
    MICHIGAN = "MI"
    MINNESOTA = "MN"
    MISSISSIPPI = "MS"
    MISSOURI = "MO"
    MONTANA = "MT"
    NEBRASKA = "NE"
    NEVADA = "NV"
    NEW_HAMPSHIRE = "NH"
    NEW_JERSEY = "NJ"
    NEW_MEXICO = "NM"
    NEW_YORK = "NY"
    NORTH_CAROLINA = "NC"
    NORTH_DAKOTA = "ND"
    OHIO = "OH"
    OKLAHOMA = "OK"
    OREGON = "OR"
    PENNSYLVANIA = "PA"
    RHODE_ISLAND = "RI"
    SOUTH_CAROLINA = "SC"
    SOUTH_DAKOTA = "SD"
    TENNESSEE = "TN"
    TEXAS = "TX"
    UTAH = "UT"
    VERMONT = "VT"
    VIRGINIA = "VA"
    WASHINGTON = "WA"
    WASHINGTON_DC = "DC"
    WEST_VIRGINIA = "WV"
    WISCONSIN = "WI"
    WYOMING = "WY"
    NE_1 = "NE_1"
    NE_2 = "NE_2"
    ME_1 = "ME_1"
    ME_2 = "ME_2"


@dataclass
class State:
    abbreviation: StateAbbreviation
    electoral_points: int
    probability_red: float

    def __post_init__(self) -> None:
        # Convert string abbreviations to the enum
        if not isinstance(self.abbreviation, StateAbbreviation):
            self.abbreviation = StateAbbreviation(self.abbreviation)


@dataclass
class Year:
    states: list[State]
    battleground_state_abbreviations: set[StateAbbreviation]
    red_consensus_points: int
    blue_consensus_points: int

    @property
    def battleground_states(self) -> list[State]:
        return [
            state
            for state in self.states
            if state.abbreviation in self.battleground_state_abbreviations
        ]
