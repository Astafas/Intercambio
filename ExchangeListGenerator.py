from ExchangeListGenerator import ExchangeList
from ExchangeListGenerator import Participant

p1 = Participant(1, 'Ana')
p2 = Participant(2, 'Beto')
p3 = Participant(3, 'Carlos')
p4 = Participant(4, 'Diana')
p5 = Participant(5, 'Elena')

exchange_list = ExchangeList([p1, p2, p3, p4, p5])

p1.add_excluded_participant(p2)
p3.add_excluded_participant(p2)
p5.add_excluded_participants([p1, p2])

exchange_list.generate_pairs()

for participant in exchange_list.participants:
    print(f'{participant.name} comparte a {participant.matched_participant}')
