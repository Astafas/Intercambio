class Participant:
    def __init__(self, id,name):
        self.name = name
        self.id = id
        self.pairingElement = None
        self.excludedParticipants = [self.id]

    def __eq__(self, other):
        if not isinstance(other, Participant):
            return NotImplemented
        return self.id == other.id
    
    def getPairingElement(self):
        return self.pairingElement

    def pairElement(self,newElement):
        self.pairingElement = newElement

    def addExcludedParticipant(self,participant):
        self.excludedParticipants.append(participant)

    def addExcludedParticipants(self,participants):
        self.excludedParticipants.extend(participants)

    def getExcludedParticipants(self):
        return self.excludeParticipants
