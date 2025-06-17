from board import Board
import time
import curses
from curses import wrapper


class GameUI:
    def __init__(self, board: Board):
        self.board = board
        self.playing = False
        self.run = True
        wrapper(self.main_loop)

    def main_loop(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.clear()

        self.draw_board_state(stdscr)
        while self.run:
            key = stdscr.getch()

            if key != -1:
                self.handle_key(key, stdscr)

            if self.playing and not self.board.game_finished():
                self.board.next_state()
                self.draw_board_state(stdscr)
                time.sleep(1)
                

    def handle_key(self, key, stdscr):
        if key == ord(' '):
            self.toggle_play()
        elif key == curses.KEY_RIGHT:
            self.playing = False
            self.board.next_state()
            self.draw_board_state(stdscr)
        elif key == curses.KEY_LEFT:
            self.playing = False
            self.board.previous_state()
            self.draw_board_state(stdscr)
        elif key == ord('q'):
            self.run = False 

    def draw_board_state(self, stdscr):
        stdscr.clear()
        board_str = self.board.board_state_as_unicode_string()
        stdscr.addstr(0, 0, board_str)
        stdscr.refresh()


    def toggle_play(self):
        self.playing = not self.playing

