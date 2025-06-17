from PIL import Image, ImageDraw
import copy

def letter_to_number(letter):
    return ord(letter.upper()) - ord('A')

class Board:
    def __init__ (self, figure_img_path: str, game_moves: str): 
        self.p_x, self.p_y = 60, 60
        self.fig_img_dict = self.prepare_piece_img(figure_img_path)
        self.board_bg_img = self.create_board_bg_img()
        self.board_state_array = []
        self.board_img_array = []
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
        self.fill_board_img_array()
        self.current_state = 0


    def prepare_piece_img(self, figure_img_path: str):
        try:
            im = Image.open(figure_img_path)
            im = im.resize((self.p_x*6, self.p_y*2))
            im = im.convert("RGBA")

            fig_img_pos = {
                'q': (0, 0),
                'k': (1, 0),
                'r': (2, 0),
                'n': (3, 0),
                'b': (4, 0),
                'p': (5, 0),
                'Q': (0, 1),
                'K': (1, 1),
                'R': (2, 1),
                'N': (3, 1),
                'B': (4, 1),
                'P': (5, 1),
            }
       
            fig_img_dict = {}
            # croping figures from png
            for key, value in fig_img_pos.items():
                x, y = int(value[0]*self.p_x), int(value[1]*self.p_y)
                fig_img_dict[key] = im.crop((x, y, x+ self.p_x, y + self.p_y))
            return fig_img_dict
        
        except FileNotFoundError:
            print(f"Missing file: {figure_img_path}")
            raise FileNotFoundError

    def create_board_bg_img(self)->Image :
        board_base_img = Image.new("RGBA", (int(self.p_x*8),int(self.p_y*8)), "#7c9c5c")
        draw_board = ImageDraw.Draw(board_base_img)
        for i in range(8):
            for j in range(8):
                if (i+j)%2 == 0:
                    draw_board.rectangle((j*self.p_x, i*self.p_y, (j+1)*self.p_x, (i+1)*self.p_y), fill = "#e4eccc")
        return board_base_img

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

    def draw_board_state_img(self, board_state):
        img: Image = self.board_bg_img.copy()
        for y, row in enumerate(board_state):
            for x, fig in enumerate(row):
                if fig == " ": continue
                img.paste(self.fig_img_dict[fig], (x*self.p_x, y*self.p_y), self.fig_img_dict[fig])            
        return img
    
    def fill_board_img_array(self):
        for state in self.board_state_array:
            img = self.draw_board_state_img(state)
            self.board_img_array.append(img)
        self.board_img_array = [img.convert('RGB') for img in self.board_img_array]
    
    def print_state_as_unicode(self, state):
        output = ""
        for y, row in enumerate(state):
            output += "\n  "+"+---"*8+f"+\n{y+1} |"
            for fig in row:
                output += f" {fig} |"
        output += f"\n  "+"+---"*8+f"+\n    a   b   c   d   e   f   g   h\n"
        print(output)

