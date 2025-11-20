from ExchangeListGenerator import ExchangeList
from ExchangeListGenerator import Participant

exchangeList = ExchangeList()
p1 = Participant(1, "Ana")
p2 = Participant(2, "Beto")
p3 = Participant(3, "Carlos")
p4 = Participant(4, "Diana")
p5 = Participant(5, "Elena")


p1.addExcludedParticipant(2)
p3.addExcludedParticipant(4)
p5.addExcludedParticipants([1, 2])


exchangeList.addParticipants([p1, p2, p3, p4, p5])


if(exchangeList.generatePairs()):
    for participant in exchangeList.participantList:
        print(participant.name + " comparte a " + participant.getPairingElement().name)
else:
    print("No existe asignacion exitosa")
