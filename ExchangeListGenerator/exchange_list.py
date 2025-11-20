import random
from collections import deque
from typing import Iterable, Deque

from ExchangeListGenerator import Participant


class ExchangeList:
    def __init__(self, participants: Iterable[Participant]) -> None:
        self.participants = set(participants)

    def add_participant(self, new_participant: Participant) -> None:
        self.participants.add(new_participant)

    def add_participants(self, new_participants: Iterable[Participant]) -> None:
        self.participants.union(new_participants)

    def generate_pairs(self) -> None:
        if len(self.participants) < 2:
            raise RuntimeError('Not enough participants')

        participants = deque(self.participants.copy())
        random.shuffle(participants)

        total_participants = len(self.participants)

        no_shift = 0

        participants_pool: Deque[Participant] = deque()

        while no_shift < total_participants:
            participant = participants.pop()
            matched = participants[0]

            no_shift += 1

            while matched in participant.excluded_participants:
                no_shift = 0
                participants_pool.append(participant)
                participant = participants.pop()

            while participants_pool:
                participants.append(participants_pool.pop())

            participants.appendleft(participant)

        participant = participants.popleft()
        while not participant.matched_participant:
            participant.matched_participant = participants[0]
            participants.append(participant)
            participant = participants.popleft()
