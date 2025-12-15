import data
import re
import time
from dataclasses import dataclass


# immutable, all other structures reference these
# not immutable cause gotta change attempts and accuracy etc
@dataclass
class AtomicChunk:
    id: int
    latin: str
    english: str
    avgAccuracy: float = 0.0
    attempts: int = 0 
    # avgTime: float = 0.0 
    # cant use time as complex to tell time for individual chunks when testing merged chunks
    # future feature: validate as typing to detect when chunk starts and ends and time individually

@dataclass
class MergedChunk:
    chunk_ids: list[int]


@dataclass
class Deck:
    chunks: list[MergedChunk]


class ChunkStore:
    def __init__(self, atomic_chunks: list[AtomicChunk]):
        self._atomic = atomic_chunks

    def get(self, chunk_id: int) -> AtomicChunk:
        return self._atomic[chunk_id]

    def atoms(self, merged: MergedChunk) -> list[AtomicChunk]:
        return [self._atomic[i] for i in merged.chunk_ids]

    def latin(self, merged: MergedChunk) -> str:
        return ". ".join([self._atomic[i].latin for i in merged.chunk_ids])
    
    def english(self, merged: MergedChunk) -> str:
        return ". ".join([self._atomic[i].english for i in merged.chunk_ids])

    def recordAttempt(self, merged: MergedChunk, accuracyList: list[float]):
        atoms = self.atoms(merged)
        for i, accuracy in enumerate(accuracyList):
            atoms[i].avgAccuracy = ((atoms[i].avgAccuracy * atoms[i].attempts) + accuracy) / (atoms[i].attempts + 1)
            atoms[i].attempts += 1


def initialiseChunks(passage):
    # re.split produces empty string if input ends in delimter, so get rid of this
    latin = [s.strip() for s in re.split(r'[?.!]', passage['latin']) if s.strip()]
    english = [s.strip() for s in re.split(r'[?.!]', passage['english']) if s.strip()]

    if len(english) != len(latin):
        print("number of sentences do not match, check input data")
        return -1
    
    atomic_chunks = [
        AtomicChunk(
            id=i,
            latin=lat,
            english=eng
        )
        for i, (lat, eng) in enumerate(zip(latin, english))
    ]

    merged_chunks = [
        MergedChunk (
            chunk_ids=[atomic_chunk.id] # square brackets as must be list as defined in class (containing one element)
        )
        for atomic_chunk in atomic_chunks 
    ]
    
    return (atomic_chunks, merged_chunks)


atomic_chunks, merged_chunks = initialiseChunks(data.text)
chunkStore = ChunkStore(atomic_chunks)

def check_accuracy(given: str, expected: str) -> float:
    # need a method so that doing one wrong thing at the start doesnt result in it all being wrong (as currently, letters would all shift out of order)
    # currently (GIVEN: "th quick brown fox") and (EXPECTED: "the quick brown fox") would give very low accuracy
    errors = 0
    if len(given) <= len(expected):
        print("given is shorter than expected")
        for i, letter in enumerate(given):
            if letter != expected[i]:
                errors += 1

        print(errors)
        difference = len(expected) - len(given) # should always be pos as under condition that given <= expected
        accuracy = ((len(expected) - errors - difference) / len(expected)) * 100 # subtracting difference means thatt all missed letters are treated as errors 
        return accuracy
    else:
        print("given is longer than expected")
        for i, letter in enumerate(expected):
            if letter != given[i]:
                errors += 1

        print(errors)
        accuracy = ((len(given) - errors) / len(given)) * 100
        return accuracy



def test(merged_chunk):
    latin = chunkStore.latin(merged_chunk)
    # consider stripping and lowering in chunkstore or jsut find somehwere more general to normalise data
    english = chunkStore.english(merged_chunk).strip().lower()
    print("--- Please remember to put a . in between chunks, as lines up with the latin, so that individual chunks can be properly stored ---")
    # display latin
    print(latin)

    # for debugging
    print(english)


    userInput = input("> ").strip().lower()

    # validate: accuracy etc
    if userInput == english.strip().lower():
        # fully correct so can skip complex validation
        chunkStore.recordAttempt(merged_chunk, [100.0 for x in merged_chunk.chunk_ids]) # create list of 100 accuracy same size as number of chunks
        print("recorded")
        print(chunkStore.atoms(merged_chunk))
    else: 
        accuracyList = []
        for i, clause in enumerate(userInput.split(".")):
            accuracyList.append(check_accuracy(clause, english.split(".")[i]))
        
        chunkStore.recordAttempt(merged_chunk, accuracyList)
        print(chunkStore.atoms(merged_chunk))

practice_chunk = MergedChunk([1, 2])
test(practice_chunk)
