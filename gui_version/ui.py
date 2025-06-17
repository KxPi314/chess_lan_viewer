import tkinter as tk

class GameWindow:
    def __init__(self, root, board):
        self.image_pointer = 0
        self.board = board
        self.playing = False
        left_frame = tk.Frame(root)
        right_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill= 'y')
        right_frame.pack(side=tk.LEFT, fill= 'y')
        
        self.list_of_moves = tk.Listbox(right_frame,)
        self.list_of_moves.pack(side=tk.LEFT, fill= 'y')
        scrollbar = tk.Scrollbar(right_frame, orient="vertical",command=self.list_of_moves.yview)
        scrollbar.pack(side=tk.LEFT, fill= 'y')
        self.list_of_moves.configure(yscrollcommand=scrollbar.set)

        for index, move in enumerate(board.moves_names):
            self.list_of_moves.insert('end',f"{index+1}: {move}")
        self.list_of_moves.update()
        self.list_of_moves.bind("<<ListboxSelect>>", self.on_listbox_click)

        self.board_img = tk.Label(left_frame, image=board.board_img_array[self.image_pointer])
        self.board_img.pack(pady=10)
        controls = tk.Frame(left_frame)
        controls.pack(anchor=tk.CENTER)

        button_previous = tk.Button(controls, text="<", command=self.previous_img)
        self.button_play = tk.Button(controls, text="▶", command=self.play_stop)
        button_next = tk.Button(controls, text=">", command=self.next_img)

        button_previous.pack(side=tk.LEFT) 
        self.button_play.pack(side=tk.LEFT)
        button_next.pack()
        self.update_img()

    def previous_img(self):
        self.image_pointer = (self.image_pointer-1)%len(self.board.board_img_array)
        self.update_img()

    def play_stop(self):
        self.playing = not self.playing
        if self.playing:
            self.button_play.config(text="⏸")
            self.autoplay()
        else:
            self.button_play.config(text="▶")
            
    def autoplay(self):
        if self.playing:
            self.next_img()
            self.board_img.after(1000, self.autoplay)
        
    def next_img(self):
        self.image_pointer = (self.image_pointer+1)%len(self.board.board_img_array)
        self.update_img()

    def update_img(self):
        self.board_img.config(image=self.board.board_img_array[self.image_pointer])
        self.board_img.update()
        self.list_of_moves.select_clear(0,len(self.board.moves_names))
        self.list_of_moves.select_set(self.image_pointer,self.image_pointer)        

    def on_listbox_click(self, event):
        selected_move = self.list_of_moves.curselection()
        if selected_move:
            self.image_pointer = int(selected_move[0])
            self.update_img()
