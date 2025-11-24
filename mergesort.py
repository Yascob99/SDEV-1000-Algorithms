def merge(left, right):
    leftlength = len(left)
    rightlength = len(right)
    i = 0
    j = 0
    mergedlist = []
    while i < leftlength and j < rightlength:
        if left[i] < right[j]:
            mergedlist.append(left[i])
            i+= 1
        else:
            mergedlist.append(right[j])
            j += 1
    while i < leftlength:
        mergedlist.append(left[i])
        i+= 1
    while j < rightlength:
        mergedlist.append(right[j])
        j += 1
    return mergedlist

def mergeSort(list):
    length = len(list)
    if length <= 1:
        return list
    leftsize = length//2
    rightsize = length - leftsize
    leftlist = []
    rightlist = []
    for i in range(length):
        if i < leftsize:
            leftlist.append(list[i])
        else:
            rightlist.append(list[i])
    leftlist = mergeSort(leftlist)
    rightlist = mergeSort(rightlist)
    return merge(leftlist, rightlist)
print(mergeSort([10, 1, 7, 6, 3, 9]))