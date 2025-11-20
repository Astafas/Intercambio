import random
from typing import Optional, Any, Self, Iterable, Set


class Participant:
    def __init__(self, _id: int, name: str) -> None:
        self.id = _id
        self.name = name
        self.matched_participant: Optional[Participant] = None
        self.excluded_participants: Set[Participant] = {self}

    def add_excluded_participant(self, participant: Self) -> None:
        self.excluded_participants.add(participant)

    def add_excluded_participants(self, participants: Iterable[Self]) -> None:
        self.excluded_participants.update(participants)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Participant(id={self.id}, name={self.name})'

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Participant):
            return False
        return self.id == other.id
