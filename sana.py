
def SubArray(arr, k):
    l2 = {}    
    for i in range(0, len(arr)-(k-1)):
        l2[str(arr[i:i+(k)])] = sum(arr[i:i+(k)])
        
    min_val = min(l2.values())

    for i, j in l2.items():
        if j == min_val:
            i = i.replace('[', '')
            i = i.replace(']', '')
            i = i.replace(',', '')
            return i
        
print(SubArray([10, 2, 13, -6, 9], 2))