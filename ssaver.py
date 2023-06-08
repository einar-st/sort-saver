import curses
import random
import sort_algs
import time
import sys


def populate(maxy, maxx):

    # populate to width
    nums = []
    for i in range(1, maxx):
        nums.append(random.choice(range(1, maxy)))
    return nums

    # only unique numbers
    # return random.sample(list(range(1, maxy)), maxy-1)


def visualize(nums, vars, stdscr, maxy, maxx, cols):

    # draw columns representing numbers
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


def main(stdscr):

    curses.curs_set(0)  # hide the cursor
    curses.use_default_colors()  # fix icky background issue
    stdscr.nodelay(1)  # non-blocking input
    rate = 30
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

    nums = populate(maxy, maxx)

    try:
        algs = [int(i) for i in sys.argv[1]]
    except IndexError:
        algs = [1, 2, 3, 4]

    alg = 0

    alg_funcs = {
        1: (sort_algs.sel_sort, 'Selection sort'),
        2: (sort_algs.bubble_sort, 'Bubble sort'),
        3: (sort_algs.insert_sort, 'Insert sort'),
        4: (sort_algs.quick_sort, 'Quick sort')
    }

    nums_gen = alg_funcs[algs[alg]][0](nums)

    change_rate = {
        259: 10,
        258: -10
    }

    # Main loop
    while True:

        # user input
        key = stdscr.getch()

        if key == ord('q'):
            break  # exit with 'q'
        elif key in change_rate.keys():
            rate += change_rate[key]
            stdscr.timeout(rate)  # refresh rate in milliseconds
        elif key == ord('n'):
            try:
                nums = populate(maxy, maxx)
                nums_gen = alg_funcs[algs[alg + 1]][0](nums)
                alg += 1
            except IndexError:
                nums = populate(maxy, maxx)
                nums_gen = alg_funcs[algs[0]][0](nums)
                alg = 0
        elif key == ord('r'):
            nums = populate(maxy, maxx)
            nums_gen = alg_funcs[algs[0]][0](nums)

        # Update creen
        stdscr.erase()
        try:
            nums, vars = next(nums_gen)
        except StopIteration:
            time.sleep(2)
            nums = populate(maxy, maxx)
            try:
                nums_gen = alg_funcs[algs[alg + 1]][0](nums)
                alg += 1
            except IndexError:
                nums_gen = alg_funcs[algs[0]][0](nums)
                alg = 0
        visualize(nums, vars, stdscr, maxy, maxx, cols)
        stdscr.addstr(0, 0, alg_funcs[algs[alg]][1])
        stdscr.addstr(1, 0, str(rate))

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
