import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror
from datetime import datetime


colors = {
    1: 'blue',
    2: '#11660a',
    3: 'red',
    4: '#a442f5',
    5: '#f542ef',
    6: '#42f5da',
    7: '#428769',
    8: '#4d7b96'
}


class Mybutton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(Mybutton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_mines = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton {self.x}{self.y} {self.number} {self.is_mine}'


class MineSwepper:
    window = tk.Tk()
    ROW = 7
    COLUMNS = 7
    MINES = 10
    COUNT_FLAGS = MINES
    TEMP = 0
    TIME_STEP = ''
    SELF_ID = ''
    IS_WIN = False
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        for i in range(MineSwepper.ROW + 2):
            temp = []
            for j in range(MineSwepper.COLUMNS + 2):
                btn = Mybutton(MineSwepper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button), bg='#3fb837')
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)
        self.update_time()

    def right_click(self, event):
        if MineSwepper.IS_GAME_OVER:
            return
        if MineSwepper.IS_WIN:
            return
        # count_flags = MineSwepper.MINES
        cur_btn = event.widget
        if cur_btn['state'] == 'normal' and MineSwepper.COUNT_FLAGS:
            cur_btn['state'] = "disabled"
            cur_btn['text'] = "☻"
            cur_btn['disabledforeground'] = "red"
            MineSwepper.COUNT_FLAGS -= 1
            self.inform_field()
        elif cur_btn['text'] == "☻":
            cur_btn['text'] = " "
            cur_btn['state'] = "normal"
            MineSwepper.COUNT_FLAGS += 1
            self.inform_field()

        if self.chek_for_victory():
            MineSwepper.IS_WIN = True
            self.window.after_cancel(MineSwepper.SELF_ID)
            showinfo('WINNER', f'ПОБЕДА! Вы нашли все мины за {MineSwepper.TIME_STEP}')

    def click(self, clicked_button: Mybutton):
        if MineSwepper.IS_GAME_OVER:
            return

        if MineSwepper.IS_WIN:
            return

        if MineSwepper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_btn()
            MineSwepper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSwepper.IS_GAME_OVER = True
            showinfo('Game Over', 'Вы проиграли ')
            for i in range(1, MineSwepper.ROW + 1):
                for j in range(1, MineSwepper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_mines, 'black')
            if clicked_button.count_mines:
                clicked_button.config(text=clicked_button.count_mines, disabledforeground=color, bg='#d2ffcf')
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state="disabled")
        clicked_button.config(relief=tk.SUNKEN)

        if self.chek_for_victory():
            MineSwepper.IS_WIN = True
            self.window.after_cancel(MineSwepper.SELF_ID)
            showinfo('WINNER', f'ПОБЕДА! Вы нашли все мины за {MineSwepper.TIME_STEP}')

    def chek_for_victory(self):
        count = 0
        for i in range(1, MineSwepper.ROW + 1):
            for j in range(1, MineSwepper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_open:
                    count += 1
        if (MineSwepper.ROW*MineSwepper.COLUMNS - count) == MineSwepper.MINES and MineSwepper.COUNT_FLAGS == 0:
            return True

    def breadth_first_search(self, btn: Mybutton):
        queue = [btn]

        while queue:

            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_mines, 'black')
            if cur_btn.count_mines:
                cur_btn.config(text=cur_btn.count_mines, disabledforeground=color, bg='#d2ffcf')
            else:
                cur_btn.config(text='', disabledforeground=color, bg='#d2ffcf')

            cur_btn.is_open = True
            cur_btn.config(state="disabled")
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_mines == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #     continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSwepper.ROW and \
                                1 <= next_btn.y <= MineSwepper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def inform_field(self):
        tk.Label(self.window, text=f"Количество мин : {MineSwepper.COUNT_FLAGS}        Таймер : {MineSwepper.TIME_STEP} ").grid(row=MineSwepper.ROW + 2, column=0, columnspan=MineSwepper.COLUMNS + 2, padx=20, pady=20)

    def update_time(self):
        MineSwepper.SELF_ID = self.window.after(1000, self.update_time)
        MineSwepper.TIME_STEP = datetime.fromtimestamp(MineSwepper.TEMP).strftime("%M:%S")
        MineSwepper.TEMP += 1
        self.inform_field()

    def reload(self):
        self.window
        [child.destroy() for child in self.window.winfo_children()]
        self.window.after_cancel(MineSwepper.SELF_ID)
        MineSwepper.TEMP = 0
        self.__init__()
        self.create_widgets()
        MineSwepper.COUNT_FLAGS = MineSwepper.MINES
        self.inform_field()
        MineSwepper.IS_WIN = False
        MineSwepper.IS_FIRST_CLICK = True
        MineSwepper.IS_GAME_OVER = False

    def settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSwepper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество столбцов').grid(row=1, column=0)
        columns_entry = tk.Entry(win_settings)
        columns_entry.insert(0, MineSwepper.COLUMNS)
        columns_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSwepper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text="Применить",
                             command=lambda: self.change_settings(row_entry, columns_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка ввода', 'Вы ввели неправельное значение')
        MineSwepper.ROW = int(row.get())
        MineSwepper.COLUMNS = int(column.get())
        MineSwepper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        setting_menu = tk.Menu(menubar, tearoff=0)
        setting_menu.add_command(label='Новая игра', command=self.reload)
        setting_menu.add_command(label='Настройка', command=self.settings_window)
        setting_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=setting_menu)

        count = 1
        for i in range(1, MineSwepper.ROW + 1):
            for j in range(1, MineSwepper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick="nswe")
                count += 1

        self.inform_field()

        for i in range(1, MineSwepper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, MineSwepper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        for i in range(MineSwepper.ROW + 2):
            for j in range(MineSwepper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background='red', disabledforeground='black')
                # elif btn.count_mines == 1:
                #     btn.config(text=btn.count_mines, fg='blue')
                elif btn.count_mines in colors:
                    color = colors.get(btn.count_mines, 'black')
                    btn.config(text=btn.count_mines, fg=color)

    def count_mines_in_buttons(self):
        for i in range(1, MineSwepper.ROW + 1):
            for j in range(1, MineSwepper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_mines = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_mines += 1
                btn.count_mines = count_mines

    def print_btn(self):
        print(self.buttons)
        for i in range(1, MineSwepper.ROW + 1):
            for j in range(1, MineSwepper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print(' M ', end='')
                else:
                    print(f" {btn.count_mines} ", end='')
            print()

    @staticmethod
    def get_mines_places(exclude_number: int):
        index = list(range(1, MineSwepper.COLUMNS * MineSwepper.ROW))
        index.remove(exclude_number)
        shuffle(index)
        return index[:MineSwepper.MINES]

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for i in range(1, MineSwepper.ROW + 1):
            for j in range(1, MineSwepper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def start(self):
        self.create_widgets()
        #        self.open_all_buttons()
        MineSwepper.window.mainloop()


game = MineSwepper()
game.start()
