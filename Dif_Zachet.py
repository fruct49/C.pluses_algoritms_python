def binarka(arr, x):
    l, r = 0, len(arr) - 1
    while l <= r:
        mid = (l + r) // 2
        if arr[mid] == x:
            while mid > 0 and arr[mid-1] == x:
                mid -= 1
            return mid
        elif arr[mid] < x:
            if mid + 2 <= r and arr[mid + 2] <= x:
                l = mid + 2
            else:
                l = mid + 1
        else:
            if mid - 2 >= l and arr[mid - 2] >= x:
                r = mid - 2
            else:
                r = mid - 1
    return l

def f():
    n = int(input())
    a = list(map(int, input().split()))
    b = int(input())
    c = list(map(int, input().split()))
    a_sorted = sorted(a)

    r = []
    for x in c:
        count = binarka(a_sorted, x)
        r.append(str(count))
    print(' '.join(r))

if __name__ == "__main__":
    f()

















