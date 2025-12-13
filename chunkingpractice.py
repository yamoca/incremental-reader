# chunk together mastered clauses

testlist = ["mastered", "mastered", "lkjsad", "mastered", "lkljdsaf", "mastered", "mastered", "mastered"]

# expected output
chunklist = [[0, 1], [2], [3], [4], [5, 6, 7]]

def chunkClauses(arr):
    length = len(arr)
    chunklist = []
    currentChunk = []

    for i in range(length):
        print("iteration: ", i)
        print("currentChunk: ", currentChunk)
        print("chunklist: ", chunklist)
        print()
        if arr[i] == "mastered":
            currentChunk.append(i)
        else:
            chunklist.append(currentChunk)
            currentChunk = []
            chunklist.append(i)



chunkClauses(testlist)
print(chunklist)
