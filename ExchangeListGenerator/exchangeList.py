from .participant import Participant
import random

class ExchangeList:
    def __init__(self):
        self.participantList = []

    
    def addParticipant(self,newParticipant):
        self.participantList.append(newParticipant)

    def addParticipants(self,newParticipants):
        self.participantList.extend(newParticipants)

    def removeParticipant(self,participantId):
        self.participantList = [p for p in self.participantList if p.id != participantId]

    def generatePairs(self):
        
        if len(self.participantList) < 2:
            print("Se necesitan al menos dos participantes")
            return False
        
        participantCopy = self.participantList[:]
        random.shuffle(participantCopy)

        seed = participantCopy[0]
        other = participantCopy[1:]

        solution = self.SearchCandidates([seed],other)
        
        if(solution):
            self._assignLastCandidates(solution)
            return True
        else:
            return False
        
    def SearchCandidates(self, candidatesActual, otherCandidates):
        
        if not otherCandidates:
            first = candidatesActual[0]
            last = candidatesActual[-1]

            if first.id not in last.excludedParticipants:
                return candidatesActual
            else:
                return None
            
        lastAssigned = candidatesActual[-1]

        random.shuffle(otherCandidates)

        for candidate in otherCandidates:

            if candidate.id in lastAssigned.excludedParticipants:
                continue
            
            newCandidates = [p for p in otherCandidates if p != candidate]

            result = self.SearchCandidates(candidatesActual + [candidate], newCandidates)

            if result is not None:
                return result
            
        return None
    
    def _assignLastCandidates(self, sortCandidates):

        n = len(sortCandidates)
        for i in range(n):
            person = sortCandidates[i]
            receptor = sortCandidates[(i+1)%n]
            person.pairingElement  = receptor