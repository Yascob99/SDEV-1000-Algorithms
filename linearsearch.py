# searches for a value in a list and returns the index, returns none if not found.
def linearSearch(list, value):
    i = 0
    for item in list:
        if item == value:
            return i
        i += 1
    return None
print(linearSearch([1, 3, 6, 7, 9, 10], 7))