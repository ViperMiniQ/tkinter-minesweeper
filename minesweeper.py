import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.font as tkFont
import random
import os
import sys
from PIL import Image, ImageTk
import time


LOCATION: str = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else \
    os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    

class MinesweeperSettings(tk.Toplevel):
    def __init__(self, minesweeper, font: tkFont.Font, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.minesweeper: Minesweeper = minesweeper
        
        self.font: tkFont.Font = font
        
        self.rows = tk.StringVar()
        self.cols = tk.StringVar()
        self.no_of_mines = tk.StringVar()
        self.font_size = tk.StringVar()
        
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill="both")
        
        self.lbl_col_size = tk.Label(
            self.frame,
            text="Columns:"
        )
        
        self.lbl_row_size = tk.Label(
            self.frame,
            text="Rows:"
        )
        
        self.lbl_no_of_mines = tk.Label(
            self.frame,
            text="Mines:"
        )
        
        self.spin_col_size = tk.Spinbox(
            self.frame,
            textvariable=self.cols,
            from_=3,
            to=1000
        )
        
        self.spin_row_size = tk.Spinbox(
            self.frame,
            textvariable=self.rows,
            to=1000,
            from_=3
        )
        
        self.spin_no_of_mines = tk.Spinbox(
            self.frame,
            textvariable=self.no_of_mines,
            to=200,
            from_=3
        )
        
        self.btn_apply = tk.Button(
            self,
            text="Apply",
            command=lambda: self.apply_minesweeper_settings()
        )
        
        self.lbl_font_size = tk.Label(
            self,
            text="Font size:"
        )
        
        self.spin_font_size = tk.Spinbox(
            self,
            to=72,
            from_=14
        )
        
        self.lbl_col_size.place(relx=0.1, rely=0.1)
        self.spin_col_size.place(relx=0.3, rely=0.1)
        
        self.lbl_row_size.place(relx=0.1, rely=0.3)
        self.spin_row_size.place(relx=0.3, rely=0.3)
        
        self.lbl_no_of_mines.place(relx=0.1, rely=0.5)
        self.spin_no_of_mines.place(relx=0.3, rely=0.5)
        
        self.lbl_font_size.place(relx=0.1, rely=0.7)
        self.spin_font_size.place(relx=0.3, rely=0.7)
        
        self.btn_apply.place(relx=0.7, rely=0.9)
        
        self.set_minesweeper_settings()
        
    def set_font_size(self):
        self.font.configure(size=int(self.spin_font_size.get()))
    
    def set_minesweeper_settings(self):
        self.no_of_mines.set(self.minesweeper.no_of_mines)
        self.rows.set(self.minesweeper.rows)
        self.cols.set(self.minesweeper.cols)
        self.font_size.set(self.font["size"])
        
    def apply_minesweeper_settings(self):
        self.minesweeper.create_field(
            columns=int(self.spin_col_size.get()), 
            rows=int(self.spin_row_size.get()),
            no_of_mines=int(self.spin_no_of_mines.get())
        )
        self.set_font_size()


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Minesweeper")
        
        self.minesweeper = Minesweeper()
        
        self.font = tkFont.Font(size=14)
        
        self.minesweeper.create_field(
            columns=5,
            rows=5,
            no_of_mines=5
        )
        self.minedrawer = MineDrawer(minesweeper=self.minesweeper, font=self.font)
        
        self.minedrawer.pack(expand=True, fill="both")
        
        self.minedrawer.set_board()
        
        self.menu = tk.Menu(self, tearoff=0)
        self.config(menu=self.menu)
        
        self.menu_settings = tk.Menu(self.menu, tearoff=0)
        self.menu_settings.add_command(label="Reset", command=self.minedrawer.set_board)
        self.menu_settings.add_command(label="New game", command=self.new_game)
        self.menu_settings.add_command(label="Settings", command=self.change_settings)
        self.menu.add_cascade(label="File", menu=self.menu_settings)
        
    def new_game(self):
        self.minesweeper.recreate_field()
        self.minedrawer.set_board()
        
    def change_settings(self):
        settings_window = MinesweeperSettings(self.minesweeper, self.font)
        settings_window.geometry("300x300")
        settings_window.wait_window()
        self.new_game()


class MineDrawer(tk.Frame):
    FG_COLORS = {
        "": "black",
        "0": "black",
        "1": "deep sky blue",
        "2": "green",
        "3": "red",
        "4": "purple",
        "5": "blue",
        "6": "pink",
        "7": "orange",
        "8": "lime",
        "!": "black"
    }
    def __init__(self, minesweeper, font: tkFont.Font, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.minesweeper: Minesweeper = minesweeper

        self.font: tkFont.Font = font
        self.buttons = None
        self.frame_board = None
        
        self.image_bomb = Image.open(f"{LOCATION}/images/bomb.png") 
        self.image_bomb_crossed = Image.open(f"{LOCATION}/images/bomb_crossed.png")
        self.image_flag = Image.open(f"{LOCATION}/images/flag.png")
        
        self.image_bomb_btn = None
        self.image_bomb_crossed_btn = None
        self.image_flag_btn = None
        
    def resize_images(self, width: int, height: int):
        if self.image_bomb:
            self.image_bomb_btn = ImageTk.PhotoImage(self.image_bomb.resize((width, height), Image.Resampling.LANCZOS))
        if self.image_bomb_crossed:
            self.image_bomb_crossed_btn = ImageTk.PhotoImage(self.image_bomb_crossed.resize((width, height), Image.Resampling.LANCZOS))
        if self.image_flag:
            self.image_flag_btn = ImageTk.PhotoImage(self.image_flag.resize((width, height), Image.Resampling.LANCZOS))
        
    def set_board(self):
        if self.frame_board is not None:
            self.frame_board.destroy()
        self.minesweeper.hide_all()
        self.frame_board = tk.Frame(self)
        self.frame_board.pack(expand=True, fill="both")
        self.set_uniform_grid()
        self.create_buttons()
        self.update()
        self.resize_images(self.buttons[0].winfo_width() - 7, self.buttons[0].winfo_height() - 7)     
        
    def create_buttons(self):
        start = time.time()
        self.buttons = []
        for row in range(self.minesweeper.rows):
            for col in range(self.minesweeper.cols):
                self.buttons.append(
                    tk.Button(
                        self.frame_board,
                        font=self.font,
                        command=lambda x=col, y=row: self.left_button_pressed(x, y)
                    )
                )
                self.buttons[-1].grid(column=col, row=row, sticky="nsew")
                self.buttons[-1].bind("<Button-3>", lambda event=None, x=col, y=row: self.right_button_pressed(event, x, y))
        print(time.time() - start)
        
    def set_button_bomb_crossed(self, index: int):
        self.buttons[index].configure(image=self.image_bomb_crossed_btn)
                
    def set_button_bomb(self, index: int):
        self.buttons[index].configure(image=self.image_bomb_btn)
                
    def set_button_text(self, index: int, text: int | str):
        self.buttons[index].configure(text=text, fg=MineDrawer.FG_COLORS[str(text)], relief="sunken")
                
    def reveal_bombs(self):
        for i, button in enumerate(self.buttons):
            y = i // self.minesweeper.cols
            x = i % self.minesweeper.cols
            value = self.minesweeper.get_value(x, y)
            if value == 0:
                self.set_button_bomb(i)
                continue
            
    def set_button_flag(self, index: int):
        if not self.buttons[index].cget("image") and not self.buttons[index].cget("text"):
            self.buttons[index].configure(image=self.image_flag_btn)
            return
        self.buttons[index].configure(image='')
        self.update()
            
    def right_button_pressed(self, event, x: int, y: int):
        button_index = y * self.minesweeper.cols + x
        self.set_button_flag(button_index)
                
    def left_button_pressed(self, x: int, y: int):
        value = self.minesweeper.press_field(x, y)
        button_index = y * self.minesweeper.cols + x
        
        if value == 0:
            self.reveal_bombs()
            self.set_button_bomb_crossed(button_index)
            messagebox.showinfo(title="Loser", message="YOU LOSE!")
            return
        if value == -1:
            self.refresh_buttons_text()
            return
        self.set_button_text(index=button_index, text=value)

    def set_uniform_grid(self):
        for col in range(self.minesweeper.cols):
            self.frame_board.columnconfigure(col, weight=1, uniform="cols")
        for row in range(self.minesweeper.rows):
            self.frame_board.rowconfigure(row, weight=1, uniform="rows")
            
    def refresh_buttons_text(self):
        for row in range(self.minesweeper.rows):
            for col in range(self.minesweeper.cols):
                if self.minesweeper.get_flag(col, row) == 1:
                    self.set_button_text(
                        index=row * self.minesweeper.cols + col, 
                        text=self.minesweeper.get_value(col, row) if self.minesweeper.get_value(col, row) != -1 else "0"
                    )


class Minesweeper(object):
    def __init__(self) -> None:
        self.cols = None
        self.rows = None
        self.no_of_mines = None
        
        self.mines = None
    
    def hide_all(self):
        for properties in self.mines.values():
            properties["flag"] = 0
    
    def get_value(self, x: int, y: int):
        return self.mines[(x, y)]["value"]
    
    def reveal_all_empty_fields(self, x: int, y: int):
        if not self.is_valid_range(x, y):
            return
        
        if self.mines[(x, y)]["flag"] == 1:
            return
        
        self.mines[(x, y)]["flag"] = 1
        
        if self.mines[(x, y)]["value"] == -1:
        
            if x < self.cols:
                self.reveal_all_empty_fields(x + 1, y)
                if y < self.rows:
                    self.reveal_all_empty_fields(x + 1, y + 1)
                if y > 0:
                    self.reveal_all_empty_fields(x + 1, y - 1)
            if y < self.rows:
                self.reveal_all_empty_fields(x, y + 1)
                if x < self.cols:
                    self.reveal_all_empty_fields(x + 1, y + 1)
                if x > 0:
                    self.reveal_all_empty_fields(x -1 , y + 1)
            if x > 0:
                self.reveal_all_empty_fields(x - 1, y)
                if y < self.rows:
                    self.reveal_all_empty_fields(x - 1, y + 1)
                if y > 0:
                    self.reveal_all_empty_fields(x - 1, y - 1)
            if y > 0:
                self.reveal_all_empty_fields(x, y - 1)
                if x < self.cols:
                    self.reveal_all_empty_fields(x + 1, y - 1)
                if x > 0:
                    self.reveal_all_empty_fields(x - 1, y - 1)
            
            
    def press_field(self, x: int, y: int) -> int:
        """Get value at position

        Args:
            x (int): column
            y (int): row

        Returns:
            int: -1 if empty, 0 if bomb, else number of neighbouring mines
        """
        
        if self.mines[(x, y)]["value"] == -1:
            self.reveal_all_empty_fields(x, y)
            
        self.mines[(x, y)]["flag"] = 1
         
        return self.mines[(x, y)]["value"]
        
    def check_win(self) -> bool:
        no_of_revealed = 0
        for properties in self.mines.values():
            if properties["flag"] == 1:
                no_of_revealed += 1
        return no_of_revealed == self.no_of_mines
        
    def neighbour_mines(self, x: int, y: int):
        neighbour_check = [-1, 0, 1]
        no_of_neighbour_mines = 0
        
        coords_to_check = [(x + offset_x, y + offset_y) for offset_x in neighbour_check for offset_y in neighbour_check]
        coords_to_check = self.filter_invalid_ranges(coords_to_check)
        
        for coord in coords_to_check:
            if not self.mines[coord]["value"]:
                no_of_neighbour_mines += 1
                
        return no_of_neighbour_mines
        
    def filter_invalid_ranges(self, coords: list[tuple]):
        for i in range(len(coords) - 1, -1, -1):
            if not self.is_valid_range(coords[i][0], coords[i][1]):
                coords.pop(i)
        return coords

    def recreate_field(self):
        self.create_field(self.cols, self.rows, self.no_of_mines)
    
    def create_field(self, columns: int, rows: int, no_of_mines: int):
        """restraints:
            3 <= columns <= 100
            3 <= rows <= 100 
            no_of_mines must not exceed 20%
        """
        if rows < 3 or rows > 100:
            raise ValueError("rows value must be within 3 and 100 (inclusive)")
        if columns < 3 or columns > 100:
            raise ValueError("columns value must be within 3 and 100 (inclusive)")
        if columns * rows / 5 < no_of_mines:
            raise ValueError("number of mines must not be more than 20%")
        
        self.cols = columns
        self.rows = rows
        self.no_of_mines = no_of_mines
        
        mines_1d = random.sample(range(0, self.cols * self.rows), self.no_of_mines)
        
        if self.mines is not None:
            self.mines.clear()
            
        self.mines = {}
        
        for y in range(self.rows):
            for x in range(self.cols):
                self.mines[(x, y)] = {
                    "value": 0 if y * self.cols + x in mines_1d else -1,
                    "flag": 0
                }
        
        self._set_neighbour_mines_values()
                
    def _set_neighbour_mines_values(self):
        for coord, properties in self.mines.items():
            if properties["value"]:
                neighbour_mines = self.neighbour_mines(coord[0], coord[1])
                if neighbour_mines:
                    properties["value"] = neighbour_mines
    
    def is_valid_range(self, x: int, y: int) -> bool:
        if x > self.cols - 1 or x < 0 or y > self.rows -1 or y < 0:
            return False
        return True
    
    def _raise_not_valid_range(self):
        raise ValueError(f"coordinates must be within defined grid {self.cols} x {self.rows}")
                
    def is_mine(self, x: int, y: int):
        if not self.is_valid_range(x, y):
            self._raise_not_valid_range()
        return not self.mines[(x, y)]["value"]
        
    def set_flag(self, x: int, y: int, flag: int):
        if not self.is_valid_range(x, y):
            self._raise_not_valid_range()
        self.mines[(x, y)]["flag"] = flag    
        
    def get_flag(self, x: int, y: int):
        if not self.is_valid_range(x, y):
            self._raise_not_valid_range()
        return self.mines[(x, y)]["flag"]
    
    def get_mines(self):
        return self.mines


if __name__ == "__main__":
    program = GUI()
    program.geometry(f"{400}x{400}")
    program.mainloop()
    