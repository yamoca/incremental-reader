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


# implement true composite pattern by creating base "chunk" class. mergedchunk and atomicchunk then inherit from this
# probably also move latin, english etc methods to be implemented at the chunk level, not chunkstore.
@dataclass
class MergedChunk:
    chunk_ids: list[int]


@dataclass
class Deck:
    chunks: list[MergedChunk]
    # prolly should have a chunkstore too


class ChunkStore:
    def __init__(self, atomic_chunks: list[AtomicChunk]):
        self._atomic = atomic_chunks

    # need tighter integrtion between chunkstore and mergedchunk
    # maybe a get func that takes in a list of chunk ids and returns a list of chunks

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

    def validate(self, merged: MergedChunk):
        ids = merged.chunk_ids
        if ids != list(range(ids[0], ids[-1] + 1)):
            raise ValueError("MergedChunk not continguous")

    def merge(self, chunks_to_be_merged: list[MergedChunk]) -> MergedChunk:
        # validate before is more optimised, but validate after is easier 
        new_chunk_ids = [] 
        for chunk in chunks_to_be_merged:
            for id in chunk.chunk_ids:
                new_chunk_ids.append(id)

        new_chunk = MergedChunk(new_chunk_ids)
        self.validate(new_chunk)
        return new_chunk


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


def check_accuracy(given: str, expected: str) -> float:
    # need a method so that doing one wrong thing at the start doesnt result in it all being wrong (as currently, letters would all shift out of order)
    # currently (GIVEN: "th quick brown fox") and (EXPECTED: "the quick brown fox") would give very low accuracy
    errors = 0
    if len(given) <= len(expected):
        for i, letter in enumerate(given):
            if letter != expected[i]:
                errors += 1

        print(errors)
        difference = len(expected) - len(given) # should always be pos as under condition that given <= expected
        accuracy = ((len(expected) - errors - difference) / len(expected)) * 100 # subtracting difference means thatt all missed letters are treated as errors 
        return accuracy
    else:
        for i, letter in enumerate(expected):
            if letter != given[i]:
                errors += 1

        print(errors)
        accuracy = ((len(given) - errors) / len(given)) * 100
        return accuracy



def test(merged_chunk: MergedChunk):
    latin = chunkStore.latin(merged_chunk)
    # consider stripping and lowering in chunkstore or jsut find somehwere more general to normalise data
    english = chunkStore.english(merged_chunk).strip().lower()

    print("--- Please remember to put a . in between chunks, as lines up with the latin, so that individual chunks can be properly stored ---")
    print(latin)

    # for debugging
    print(english)

    userInput = input("> ").strip().lower()

    # validate: accuracy etc
    accuracyList = []
    for i, clause in enumerate(userInput.split(".")):
        accuracyList.append(check_accuracy(clause, english.split(".")[i]))
        
    chunkStore.recordAttempt(merged_chunk, accuracyList)
    print(chunkStore.atoms(merged_chunk))

def study(deck: Deck):
    # move from chunk to chunk
    # user / "game" loop stuff 
    while True: # keep going until user quits
        for chunk in deck.chunks:
            test(chunk)
        
        # check_for_chunks_to_merge
        chunks_to_merge = []

        for chunk in deck.chunks:
            for id in chunk.chunk_ids:
                if chunkStore.get(id).avgAccuracy > 90:
                    chunks_to_merge.append(id)

        print(chunks_to_merge)

        twodimensionlist = []
        newchunks = 1
        for i, id in enumerate(chunks_to_merge):
            if i == 0: 
                twodimensionlist.append([id])
                last_id = id 
            else:
                if id == last_id + 1:
                    twodimensionlist[newchunks-1].append(id)
                else:
                    twodimensionlist.append([id])
                    newchunks += 1

        print(twodimensionlist)

        # mergechunks()
        # update deck: careful, is this allowed: changing current scope variable within function that its operating with?

        # [1, 2, 3, 5] currently returns [[1, 2], [3], [5]]
        # should return [[1, 2, 3,], [5]]
        # think about using linked lists


# need a "ChunkManager" or something official to actually decide which chunks need merging and when
# once every "game loop" -> in study func ?



atomic_chunks, merged_chunks = initialiseChunks(data.text)
print(atomic_chunks)
chunkStore = ChunkStore(atomic_chunks)
aeneid_page_1 = Deck(merged_chunks)

study(aeneid_page_1)

# getting an empty one at the end of data e.g problem with splitting of initial data
# empty atomic chunk somewhere