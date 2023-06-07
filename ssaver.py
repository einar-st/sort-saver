import curses
from curses import wrapper
import random
import sort_algs
import time
import sys


def main(stdscr):

    def populate(maxy, maxx, unique=False):
        lst_length = maxx - 1
        nums = []
        if unique:
            maxx = maxy
            nums = random.sample(list(range(1, maxx)), maxx-1)
        else:
            for i in range(1, lst_length + 1):
                nums.append(random.choice(range(1, maxy)))
        return nums

    def visualize(nums, vars):

        for line in range(maxy - 1, -1, -1):
            for i in range(len(nums)):
                if nums[i] >= line + 1:
                    try:
                        stdscr.addch(
                            maxy - 1 - line,
                            i + int((maxx - len(nums) - 1)/2),
                            '\u2588', cols[vars[i]]
                        )
                    except KeyError:
                        stdscr.addch(
                            maxy - 1 - line,
                            i + int((maxx - len(nums) - 1)/2),
                            '\u2588'
                        )

    # Setup
    curses.curs_set(0)  # hide the cursor
    curses.use_default_colors()  # fix icky background issue
    stdscr.nodelay(1)  # non-blocking input
    rate = 20
    stdscr.timeout(rate)  # refresh rate in milliseconds
    maxy, maxx = stdscr.getmaxyx()

    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_BLUE, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)

    cols = {
        'red': curses.color_pair(1),
        'blue': curses.color_pair(2),
        'green': curses.color_pair(3)
    }

    # create list
    nums = populate(maxy, maxx)
    algs = [
        sort_algs.sel_sort,
        sort_algs.bubble_sort,
        sort_algs.insert_sort,
        sort_algs.quick_sort
    ]
    alg_names = [
        'Selection sort',
        'Bubble sort',
        'Insert sort',
        'Quick sort'
    ]
    try:
        alg = int(sys.argv[1])
    except IndexError:
        alg = 0

    nums_obj = algs[alg](nums)

    change_rate = {
        259: 10,
        258: -10
    }

    # Main loop
    while True:

        # Get user input
        key = stdscr.getch()

        # Process user input
        if key == ord('q'):
            break  # Exit the loop if 'q' is pressed
        elif key in change_rate.keys():
            rate += change_rate[key]
            stdscr.timeout(rate)  # refresh rate in milliseconds
        elif key == ord('n'):
            try:
                nums_obj = algs[alg + 1](nums)
                alg += 1
            except IndexError:
                nums_obj = algs[0](nums)
                alg = 0
        elif key == ord('r'):
            nums = populate(maxy, maxx, True)

        # Update creen
        stdscr.erase()
        try:
            nums, vars = next(nums_obj)
        except StopIteration:
            time.sleep(2)
            nums = populate(maxy, maxx)
            try:
                nums_obj = algs[alg + 1](nums)
                alg += 1
            except IndexError:
                nums_obj = algs[0](nums)
                alg = 0
        visualize(nums, vars)
        stdscr.addstr(0, 0, alg_names[alg])
        stdscr.addstr(1, 0, str(rate))

        stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
