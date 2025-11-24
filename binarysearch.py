# finds item in list, more quickly but requires a sorted list. returns the index or none if not found.     
def binarySearch(list, value):
    start = 0
    end = len(list)
    while start != end:
        half = (end-start)//2 + start # finds the approximate halfway point between the two.
        if list[half] == value:
            return half
        elif list[half] > value:
            start = half
        else:
            end = half
    return None
print(binarySearch([1, 3, 6, 7, 9, 10], 7))