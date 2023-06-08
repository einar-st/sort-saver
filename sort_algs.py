def sel_sort(nums):

    for i in range(len(nums) - 1):
        low = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[low]:
                low = j
            vars = {low: 'blue', i: 'red', j: 'green'}
            yield (nums, vars)
        nums[i], nums[low] = nums[low], nums[i]

    vars = {}
    yield nums, vars


def bubble_sort(nums):

    vars = {}
    yield nums, vars

    for i in range(len(nums) - 1):
        for x in range(len(nums) - i - 1):
            y = x + 1
            if nums[x] > nums[y]:
                nums[x], nums[y] = nums[y], nums[x]
            vars = {y: 'blue'}
            yield nums, vars

    vars = {}
    yield nums, vars


def insert_sort(nums):

    yield nums, {}

    for x in range(1, len(nums)):
        for i in range(x, - 1, - 1):
            vars = {i: 'blue', x: 'green'}
            yield nums, vars
            if i == 0 or nums[i] > nums[i - 1]:
                break
            else:
                nums[i], nums[i - 1] = nums[i - 1], nums[i]

    yield nums, {}


def quick_sort(nums, top=True, *args):

    try:
        lo, hi = args[0]
    except IndexError:
        lo = 0
        hi = len(nums) - 1

    if lo >= hi:
        return

    j = lo - 1
    p = hi

    # median of three
    mots = [nums[lo], nums[int(len(nums) / 2)], nums[hi]]
    mots.remove(min(mots))
    mots.remove(max(mots))
    mot = mots[0]

    for i in [lo, int(len(nums) / 2)]:
        if nums[i] == mot:
            nums[i], nums[p] = nums[p], nums[i]
            break

    for i in range(lo, hi):  # iterate all except p
        if nums[i] < nums[p]:  # if less than p, swap with previous hi
            j += 1
            nums[i], nums[j] = nums[j], nums[i]
        yield nums, {j: 'blue', lo - 1: 'white', i: 'blue', lo: 'red', p: 'green'}

    # move pivot to correct spot
    nums[p], nums[j + 1] = nums[j + 1], nums[p]

    # sort left and right 'in-place'
    for part in quick_sort(nums, False, (lo, j)):
        yield part
    for part in quick_sort(nums, False, (j + 2, hi)):
        yield part

    if top:
        yield nums, {}
