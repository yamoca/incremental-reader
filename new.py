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


def test(merged_chunk):
    latin = chunkStore.latin(merged_chunk)
    english = chunkStore.english(merged_chunk)
    # display latin
    print(latin)

    # for debugging
    print(english)


    # get answer and answer time
    startTime = time.time()
    userInput = input("> ").strip().lower()
    endTime = time.time()
    answerTime = endTime - startTime

    # validate: accuracy etc
    if userInput == english.strip().lower():
        # fully correct so can skip complex validation
        chunkStore.recordAttempt(merged_chunk, [100.0 for x in merged_chunk.chunk_ids]) # create list of 100 accuracy same size as number of chunks
        print("recorded")
        print(chunkStore.atoms(merged_chunk))
    else: 
        print(english)

practice_chunk = MergedChunk([1, 2])
test(practice_chunk)