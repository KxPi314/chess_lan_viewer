import copy

def letter_to_number(letter):
    return ord(letter.upper()) - ord('A')

class Board:
    def __init__ (self, game_moves: str): 
        self.board_state_array = []
        start_setup = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        first_state = [[" " for _ in range(8)] for _ in range(8)]
        for index, figure in enumerate(start_setup):
            first_state[0][index] = figure.lower()
            first_state[1][index] = 'p'
            first_state[6][index] = 'P'
            first_state[7][index] = figure
        self.board_state_array.append(first_state)
        self.game_moves_str_to_array(game_moves)
        self.fill_board_state_array()
        self.current_state = 0
    
    def next_state(self):
        self.current_state = (self.current_state+1)%len(self.board_state_array)

    def previous_state(self):
        self.current_state = (self.current_state-1)%len(self.board_state_array)

    def game_finished(self):
        return self.current_state == len(self.board_state_array)-1

    def game_moves_str_to_array(self, moves: str):
        self.moves_array = []
        moves = moves.strip()
        self.moves_names = moves.split(" ")
        for move in self.moves_names:
            x0 = letter_to_number(move[0])
            y0 = 8-int(move[1])
            x1 = letter_to_number(move[2])
            y1 = 8-int(move[3])
            prom = None
            if len(move) == 5: prom = move[4].upper()
            self.moves_array.append((x0, y0, x1, y1, prom))

    def check_short_castle(self, piece, dst, board_state):
        x0, y0 = piece
        x1, _ = dst
        if board_state[y0][x0] == "" or board_state[y0][x0].upper() != "K":
            return False
        if x0 - x1 == -2:
            return True # short castle
        return False

    def check_long_castle(self, piece, dst, board_state):
        x0, y0 = piece
        x1, _ = dst
        if board_state[y0][x0] == "" or board_state[y0][x0].upper() != "K":
            return False
        if x0 - x1 == 2:
            return True # long castle
        return False

    def fill_board_state_array(self): 
        previous_board_state = copy.deepcopy(self.board_state_array[0])
        for i, move in enumerate(self.moves_array):
            previous_board_state = self.board_state_array[i]
            current_board_state = copy.deepcopy(previous_board_state)
            x0, y0, x1, y1, promotion = move
            if promotion:
                current_board_state[y1][x1] = previous_board_state[y0][x0][0] + promotion 
            elif self.check_long_castle((x0, y0), (x1, y1), previous_board_state):
                current_board_state[y1][x1] = previous_board_state[y0][x0]
                current_board_state[y1][x1+1] = previous_board_state[y0][0]
                current_board_state[y0][0] = " "
            elif self.check_short_castle((x0, y0), (x1, y1), previous_board_state):
                current_board_state[y1][x1] = previous_board_state[y0][x0]
                current_board_state[y1][x1-1] = previous_board_state[y0][7]
                current_board_state[y0][7] = " "
            else:
                current_board_state[y1][x1] = previous_board_state[y0][x0]
            current_board_state[y0][x0] = " "
            self.board_state_array.append(current_board_state)
    
    def board_state_as_unicode_string(self):
        output = ""
        for y, row in enumerate(self.board_state_array[self.current_state]):
            output += "\n  "+"+---"*8+f"+\n{y+1} |"
            for fig in row:
                output += f" {fig} |"
        output += f"\n  "+"+---"*8+f"+\n    a   b   c   d   e   f   g   h\n"
        return output

