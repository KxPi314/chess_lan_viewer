import tkinter as tk
from PIL import ImageTk
from ui import GameWindow
from board import Board
import re
import sys

def main():
    lan = ""
    if len(sys.argv) == 1:
        lan = input("input LAN notation: ")
    elif len(sys.argv) == 2:
        with open(sys.argv[1]) as moves:
            lan = moves.read()      
    else:
        raise ValueError("Invalid number of arguments. Usage: script.py <input_file>")
    
    verifi_lan = re.compile("([a-h][1-8][a-h][1-8] ?)+")
    if verifi_lan.fullmatch(lan) == None:
        raise ValueError(f"Invalid move format in input.txt at position {verifi_lan.match(lan).end()}")
    
    try:
        board = Board("ChessPiecesArray.png", lan)
    except FileNotFoundError:
        return
    root = tk.Tk()
    board.board_img_array = [ImageTk.PhotoImage(img, master=root) for img in board.board_img_array]
    GameWindow(root, board)
    root.mainloop()  

if __name__ == "__main__":
    main()
