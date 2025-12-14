import data
import re
from dataclasses import dataclass


# immutable, all other structures reference these
@dataclass
class AtomicChunk:
    id: int
    latin: str
    english: str
    avgAccuracy: float = 0.0
    attempts: int = 0 
    avgTime: float = 0.0

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
        return " ".join([self._atomic[i].latin for i in merged.chunk_ids])
    
    def english(self, merged: MergedChunk) -> str:
        return " ".join([self._atomic[i].english for i in merged.chunk_ids])



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