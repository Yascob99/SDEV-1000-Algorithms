def merge(left, right):
    
    # initialize the pointers and length variables
    leftlength = len(left)
    rightlength = len(right)
    i = 0
    j = 0
    
    # create a new list
    mergedlist = []
    
    # go put the smallest item from each list into the new list until all the items from one input list has been added.
    while i < leftlength and j < rightlength:
        if left[i] < right[j]:
            mergedlist.append(left[i])
            i+= 1
        else:
            mergedlist.append(right[j])
            j += 1
            
    # add the remaining items from each list.
    while i < leftlength:
        mergedlist.append(left[i])
        i+= 1
    while j < rightlength:
        mergedlist.append(right[j])
        j += 1
    return mergedlist

def mergeSort(list):
    # if length of list is 1 or less return the list.
    length = len(list)
    if length <= 1:
        return list
    
    # divide the lists into equal parts
    leftsize = length//2
    leftlist = []
    rightlist = []
    for i in range(length):
        if i < leftsize:
            leftlist.append(list[i])
        else:
            rightlist.append(list[i])
    
    # use recursion to divide the lists until they are 1 item or shorter.
    leftlist = mergeSort(leftlist)
    rightlist = mergeSort(rightlist)
    
    # merge and sort the lists and return the result
    return merge(leftlist, rightlist)
print(mergeSort([10, 1, 7, 6, 3, 9]))