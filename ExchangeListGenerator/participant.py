import logging
from typing import Optional, Any, Iterable, Set

logger = logging.getLogger(__name__)


class Participant:
    def __init__(self, _id: int, name: str, email: str) -> None:
        self.id = _id
        self.name = name
        self.email = email
        self.matched_participant: Optional[Participant] = None
        self.excluded_participants: Set[Participant] = {self}

        logger.debug(f'Created participant {self}')

    @classmethod
    def _validate_participant(cls, participant: Participant | int) -> Participant:
        if isinstance(participant, int):
            return Participant(participant, f'Participant {participant}', 'email@example.com')
        return participant

    def should_give_to(self, participant: Participant | int) -> None:
        participant = self._validate_participant(participant)

        if self == participant:
            raise ValueError(f'A participant cannot give to themselves: {self}')

        if participant in self.excluded_participants:
            raise ValueError(f'A participant cannot give to an excluded participant: {participant}')

        self.matched_participant = participant
        logger.debug(f'{self} will give to {participant}')

    def add_excluded_participant(self, participant: Participant | int) -> None:
        participant = self._validate_participant(participant)

        if self == participant:
            raise ValueError(f'A participant cannot exclude themself: {self}')

        if participant == self.matched_participant:
            raise ValueError(f'A participant cannot exclude their matched participant: {participant}')

        self.excluded_participants.add(participant)
        logger.debug(f'{self} will exclude {participant}')

    def add_excluded_participants(self, participants: Iterable[Participant | int]) -> None:
        participants = [self._validate_participant(p) for p in participants]

        if self in participants:
            raise ValueError(f'A participant cannot exclude themself: {self}')

        if self.matched_participant in participants:
            raise ValueError(f'A participant cannot exclude their matched participant: {self.matched_participant}')

        self.excluded_participants.update(participants)
        logger.debug(f'{self} will exclude {participants}')

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f'Participant(id={self.id}, name={self.name}, email={self.email})'

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Participant):
            return self.id == other.id

        if isinstance(other, int):
            return self.id == other

        return False
