# CHESS LAN VIEWING PROGRAM

This is a simple project for visualizing chess games written in LAN (Long Algebraic Notation) format.  
The project includes both a **GUI version** and a **terminal version** of the viewer.

---

## What is Long Algebraic Notation (LAN)?

**LAN** stands for **Long Algebraic Notation** — a chess notation where each move is written as: <from_column><from_row><to_column><to_row>

For example:
- `e2e4` – pawn moves from e2 to e4
- `g1f3` – knight moves from g1 to f3

Some example games in this format are included in the repository.

---

## Running the Program

The project was made to run on both **Linux** and **Windows**.  

### Terminal version:

```bash
cd terminal_version
python main.py <path_to_input_file>
```

### GUI version:

```bash
cd gui_version
python main.py <path_to_input_file>
```
You can also run it without providing a file, and enter the notation manually as a string.

