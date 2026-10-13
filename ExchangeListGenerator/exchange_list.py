import logging
import random
from collections import deque
from typing import Iterable, Deque

from ExchangeListGenerator import Participant

logger = logging.getLogger(__name__)


class ExchangeList:
    def __init__(self, participants: Iterable[Participant]) -> None:
        self.participants = set[Participant](participants)
        self.matched_participants: tuple[Participant] = tuple()
        logger.debug(f'Created exchange list with participants {self.participants}')

    @classmethod
    def from_file(cls, filename: str) -> 'ExchangeList':
        """
        Load participants from a file with one participant per line:

            name|email|excluded_ids|forced_receiver

        IDs are assigned by line order, starting at 0 (blank lines are skipped).
        excluded_ids is a comma-separated list of IDs, and both it and forced_receiver may be empty.
        """
        rows: list[tuple[int, list[str]]] = []

        with open(filename, encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                fields = [field.strip() for field in line.split('|')]
                if len(fields) != 4:
                    raise ValueError(f'{filename}:{line_number} - Expected 4 fields '
                                     f'(name|email|excluded_ids|forced_receiver), got {len(fields)}')
                rows.append((line_number, fields))

        participants = [Participant(_id, name, email) for _id, (_, (name, email, _, _)) in enumerate(rows)]
        logger.debug(f'Loaded {len(participants)} participants from {filename}')

        def get_participant(raw_id: str, line_number: int) -> Participant:
            try:
                _id = int(raw_id)
            except ValueError:
                raise ValueError(f'{filename}:{line_number} - Invalid ID: {raw_id!r}') from None

            if not 0 <= _id < len(participants):
                raise ValueError(f'{filename}:{line_number} - Unknown participant ID: {_id}')

            return participants[_id]

        for participant, (line_number, (_, _, excluded_ids, forced_receiver)) in zip(participants, rows):
            if excluded_ids:
                participant.add_excluded_participants(
                    get_participant(raw_id, line_number) for raw_id in excluded_ids.split(',') if raw_id.strip()
                )

            if forced_receiver:
                participant.should_give_to(get_participant(forced_receiver, line_number))

        return cls(participants)

    def add_participant(self, new_participant: Participant) -> None:
        self.participants.add(new_participant)
        logger.debug(f'{new_participant} added to exchange list')

    def add_participants(self, new_participants: Iterable[Participant]) -> None:
        self.participants.union(new_participants)
        logger.info(f'{new_participants} added to exchange list')

    def generate_pairs(self) -> None:
        if self.matched_participants:
            logger.debug(f'Exchange list already has matched participants: {self.matched_participants}')
            return

        self._validate_forced_participants()

        if len(self.participants) < 2:
            raise RuntimeError(f'Not enough participants: {self.participants}')

        participants: Deque[Participant] = deque[Participant](self.participants.copy())
        random.shuffle(participants)
        logger.debug(f'Participants shuffled: {participants}')

        total_participants = len(self.participants)
        logger.debug(f'Total participants: {total_participants}')

        shifts = 0

        participants_pool: Deque[Participant] = deque()
        logger.debug(f'Participants pool created: {participants_pool}')

        while shifts < total_participants:
            participant = participants.pop()
            logger.debug(f'Participant popped: {participant}')

            if participant.matched_participant:
                participants.insert(participants.index(participant.matched_participant), participant)
                logger.debug(f'Participant inserted back (has forced receiver): {participant}')
                continue

            matched = participants[0]

            shifts += 1

            while matched in participant.excluded_participants:
                logger.debug(f'Shifting participant due to exclusion: {matched}')

                shifts = 0
                participants_pool.append(participant)
                participant = participants.pop()

                logger.debug(f'Pooled participants: {participants_pool} || Participant popped: {participant}')

            while participants_pool:
                participants.append(participants_pool.pop())

            participants.appendleft(participant)
            logger.debug(f'Current participants: {participants}')

        matched_participants: list[Participant] = []
        while participants:
            matched_participants.append(participants.popleft())
            matched_participants[-1].matched_participant = participants[0] if participants else matched_participants[0]

        self.matched_participants = tuple(matched_participants)
        self._validate_matched_participants()
        logger.debug(f'Matched participants: {matched_participants}')

    def _validate_forced_participants(self) -> None:
        participants_seen: set[Participant] = set()

        for participant in self.participants:
            logger.debug(f'Validating Participant forced receiver: {participant}')

            if participant.matched_participant is not None:
                if participant.matched_participant in participants_seen:
                    raise RuntimeError(f'Forced participants configuration is invalid - '
                                       f'Repeated forced participant: {participant.matched_participant}')
                participants_seen.add(participant.matched_participant)
                logger.debug(f'Added forced to forced participants pool: {participant.matched_participant}')

        logger.debug(f'Forced participants configuration is valid')

    def _validate_matched_participants(self) -> None:
        logger.debug(f'Validating matched participants')

        for participant in self.matched_participants:
            logger.debug(f'Validating Participant: {participant}')

            if participant.matched_participant in participant.excluded_participants:
                raise RuntimeError('Matched participants configuration is invalid - '
                                   f'{participant} cannot be matched with {participant.matched_participant} '
                                   f'because the latter is in the excluded participants list of the former - '
                                   f'Exclustion list: {participant.excluded_participants}')
