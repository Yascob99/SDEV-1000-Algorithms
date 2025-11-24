def bubbleSort(list):
    length = len(list)
    for i in range(length):
        j = 0
        # while j is not out of index and is not at the currently sorted values.
        while j < length - i -1:
            # if the current value is larger than the next number swap
            if list[j] > list[j+1]:
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp  
            j += 1
    return list
print(bubbleSort([10, 1, 7, 6, 3, 9]))            
        