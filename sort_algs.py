def sel_sort(nums):

    for i in range(len(nums) - 1):
        low = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[low]:
                low = j
            vars = {low: 'green', i: 'red', j: 'blue'}
            yield (nums, vars)
        nums[i], nums[low] = nums[low], nums[i]
        vars = {i: 'red', j: 'blue'}
        yield (nums, vars)

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
            vars = {y: 'red'}
            yield nums, vars

    vars = {}
    yield nums, vars


def insert_sort(nums):

    yield nums, {}

    for x in range(1, len(nums)):
        for i in range(x, - 1, - 1):
            vars = {i: 'red', x: 'blue'}
            yield nums, vars
            if i == 0 or nums[i] > nums[i - 1]:
                break
            else:
                nums[i], nums[i - 1] = nums[i - 1], nums[i]

    yield nums, {}


if __name__ == '__main__':

    import random

    all_nums = [i for i in range(1, 11)]

    nums = []
    for i in range(len(all_nums)):
        num = random.choice(all_nums)
        nums.append(num)
        all_nums.remove(num)

    print(nums)
    for i in sel_sort(nums):
        print(i)
