from ethereum_utils import *
import time
import curses

def display_balance_voting_booths(stdscr, voting_booths=voting_booths):
    curses.curs_set(0)  # Hide the cursor
    while True:
        stdscr.clear()
        for booth in voting_booths:
            balance_str = "The balance of the voting booth {} is: {}".format(booth, mu_get_balance(booth))
            stdscr.addstr(balance_str + "\n")
        
        stdscr.refresh()
        time.sleep(1)  # Adjust the sleep duration as needed

if __name__ == "__main__":
    curses.wrapper(display_balance_voting_booths, voting_booths)

