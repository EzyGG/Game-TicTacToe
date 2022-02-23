import sys

import ezyapi.game_manager as manager
from ezyapi.mysql_connection import DatabaseConnexionError
from ezyapi.sessions import UserNotFoundException
from ezyapi.UUID import UUID
from ezyapi.contants import COLOR_EXP, COLOR_GP, COLOR_SPECIAL
from threading import Thread
from time import sleep
from tkinter import *
from random import randint, choice, shuffle


GAME_UUID = UUID.parseUUID("14b34484-0b34-d080-71ee-13b3a8bd18c2")
GAME_VERSION = manager.GameVersion("v1.1")


class TicTacToe:
    def __init__(self):
        self.table = None
        self.win_app = None

        self.app_name = "Tic Tac Toe"
        self.app_ico = "tic_tac_toe.ico"
        self.app_size = 300
        self.app_bg = 'black'
        self.app_fg = 'white'
        self.app_circle_color = 'blue'
        self.app_cross_color = 'red'
        self.win_title = "Fin de la partie !"
        self.win_geometry = "275x125"

        self.wins = 0
        self.looses = 0

        self.IA_win_possibilities = [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 1), (2, 2)],
                                     [(0, 2), (1, 1), (2, 0)], [(2, 2), (2, 1), (2, 0)], [(2, 2), (1, 2), (0, 2)],
                                     [(1, 0), (1, 1), (1, 2)], [(0, 1), (1, 1), (2, 1)]]

        self.tk = Tk()
        self.tk.title(self.app_name)
        self.tk.resizable(False, False)
        self.tk.geometry(str(self.app_size) + "x" + str(self.app_size))
        self.tk.configure(background=self.app_bg)
        try:
            self.tk.iconbitmap(self.app_ico)
        except Exception:
            pass

        self.canvas = Canvas(self.tk, width=self.app_size, height=self.app_size,
                             background=self.app_bg, highlightthickness=0)
        self.canvas.pack()
        self.reset()
        self.canvas.bind("<Button-1>", lambda event: self.played(event))

        self.tk.protocol("WM_DELETE_WINDOW", self.quit)

    def IA(self):
        if self.is_playable():
            played = False
            for i in [2, 1]:
                if not played:
                    for p in self.IA_win_possibilities:
                        cur = [self.table[p[0][0]][p[0][1]], self.table[p[1][0]][p[1][1]], self.table[p[2][0]][p[2][1]]]
                        if cur[0] == i and cur[1] == i and cur[2] == 0:
                            self.table[p[2][0]][p[2][1]] = 2
                            played = True
                            break
                        elif cur[0] == i and cur[1] == 0 and cur[2] == i:
                            self.table[p[1][0]][p[1][1]] = 2
                            played = True
                            break
                        elif cur[0] == 0 and cur[1] == i and cur[2] == i:
                            self.table[p[0][0]][p[0][1]] = 2
                            played = True
                            break
            if not played:
                while not played:
                    x = randint(0, 3) - 1
                    y = randint(0, 3) - 1
                    if self.table[x][y] == 0:
                        self.table[x][y] = 2
                        played = True
            if self.get_win() != 0:
                self.refresh()
                self.win(self.get_win())
        else:
            self.reset()
            self.IA()
        self.refresh()

    def played(self, event):
        if self.win_app is None:
            if self.is_playable():
                x = None
                y = None
                if 0 <= event.x <= self.app_size / 3:
                    x = 0
                elif self.app_size / 3 <= event.x <= self.app_size / 3 * 2:
                    x = 1
                elif self.app_size / 3 * 2 <= event.x <= self.app_size:
                    x = 2
                if 0 <= event.y <= self.app_size / 3:
                    y = 0
                elif self.app_size / 3 <= event.y <= self.app_size / 3 * 2:
                    y = 1
                elif self.app_size / 3 * 2 <= event.y <= self.app_size:
                    y = 2
                if x is not None and y is not None and self.table[x][y] == 0:
                    self.table[x][y] = 1
                    if self.get_win() != 0:
                        self.refresh()
                        self.win(self.get_win())
                    self.IA()
            else:
                self.reset()
                self.played(event)

    def is_playable(self):
        for t in self.table:
            if 0 in t:
                return True
        return False

    def get_win(self):
        for p in self.IA_win_possibilities:
            cur = [self.table[p[0][0]][p[0][1]], self.table[p[1][0]][p[1][1]], self.table[p[2][0]][p[2][1]]]
            if cur[0] != 0 and cur[0] == cur[1] == cur[2]:
                return cur[0]
        return 0

    def win(self, team=0):
        if team == 1:
            self.wins += 1
        if team == 2:
            self.looses += 1
        self.win_app = Tk()
        self.win_app.resizable(False, False)
        self.win_app.geometry(self.win_geometry)
        self.win_app.title(self.win_title)
        self.win_app.configure(background=self.app_bg)
        try:
            self.win_app.iconbitmap(self.app_ico)
        except Exception:
            pass
        label = Label(self.win_app, bg=self.app_bg, fg=self.app_circle_color if team == 1 else self.app_cross_color if
                      team == 2 else self.app_fg, font=("", 16, "bold"), text="L'équipe des Ronds\na gagné !" if
                      team == 1 else "L'équipe des Croix\na gagné !" if team == 2 else "Personne n'a\ngagné...")
        label.pack(expand=YES, side=TOP)
        points = Frame(self.win_app, bg=self.app_bg)
        side = RIGHT if team == 2 else LEFT
        Label(points, bg=self.app_bg, font=("", 16, "bold"), fg=self.app_circle_color, text=str(self.wins)).pack(side=side, padx=5)
        Label(points, bg=self.app_bg, font=("", 16, "bold"), fg=self.app_fg, text=" | ").pack(side=side, padx=5)
        Label(points, bg=self.app_bg, font=("", 16, "bold"), fg=self.app_cross_color, text=str(self.looses)).pack(side=side, padx=5)
        points.pack(expand=YES, side=TOP, pady=5)
        frame = Frame(self.win_app, bg=self.app_bg)
        restart_button = Button(frame, text="Rejouer !", command=self.start)
        restart_button.grid(row=0, column=0, padx=5)
        quit_button = Button(frame, text="Quitter.", command=self.quit)
        quit_button.grid(row=0, column=1, padx=5)
        frame.pack(side=BOTTOM)
        self.win_app.protocol("WM_DELETE_WINDOW", self.quit)
        self.win_app.mainloop()

    def quit(self):
        self.tk.destroy()
        if self.win_app is not None:
            self.win_app.destroy()
        self.commit_scores()
        sys.exit(1)

    def commit_scores(self):
        scores = Scores(self.wins, self.looses, "+10 Karma")
        if manager.linked() and (self.wins + self.looses):
            try:
                manager.start_new_game()
                manager.commit_new_set(GAME_UUID, self.wins >= self.looses, scores.v_total_exp, scores.v_total_gp)
            except manager.AlreadyCommitted as e:
                Error("AlreadyCommitted", str(e) + "\nYou can close now :).")
            except DatabaseConnexionError as e:
                Error("DatabaseConnexionError", str(e) + "\nThe SQL Serveur is potentially down for maintenance...\nWait and Rety Later." + CONTINUE)
            except Exception as e:
                Error(type(e)[1:-1], str(e))
        scores.start()

    def start(self):
        if self.win_app is not None:
            self.win_app.destroy()
            self.win_app = None
        self.reset()
        self.tk.mainloop()

    def reset(self):
        self.table = [[0 for j in range(0, 3)] for i in range(0, 3)]
        self.refresh()

    def reset_canvas(self):
        self.tk.update()
        self.canvas.delete("all")
        self.draw_init_pattern()

    def refresh(self):
        self.reset_canvas()
        for x in range(0, len(self.table)):
            for y in range(0, len(self.table[x])):
                if self.table[x][y] == 1:
                    self.draw_circle(x, y)
                elif self.table[x][y] == 2:
                    self.draw_cross(x, y)

    def draw_round_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
        return self.canvas.create_polygon(points, fill=self.app_fg, **kwargs, smooth=True)

    def draw_init_pattern(self):
        self.draw_round_rectangle(self.app_size / 3 - 3, self.app_size / 24, self.app_size / 3 + 3, self.app_size / 24 * 23)
        self.draw_round_rectangle(self.app_size / 3 * 2 - 3, self.app_size / 24, self.app_size / 3 * 2 + 3, self.app_size / 24 * 23)
        self.draw_round_rectangle(self.app_size / 24, self.app_size / 3 - 3, self.app_size / 24 * 23, self.app_size / 3 + 3)
        self.draw_round_rectangle(self.app_size / 24, self.app_size / 3 * 2 - 3, self.app_size / 24 * 23, self.app_size / 3 * 2 + 3)

    def draw_circle(self, x, y):
        if x is None:
            x = randint(0, 2)
        if y is None:
            y = randint(0, 2)
        self.canvas.create_oval(self.app_size / 24 + self.app_size / 24 * 8 * x, self.app_size / 24 + self.app_size / 24 * 8 * y, self.app_size / 24 * 7 + self.app_size / 24 * 8 * x, self.app_size / 24 * 7 + self.app_size / 24 * 8 * y, width=10, outline=self.app_circle_color)
        # canvas.create_oval(app_size_height / 12 + app_size_height / 12 * 4 * x, app_size_width / 12 + app_size_width / 12 * 4 * y, app_size_height / 12 * 3 + app_size_height / 12 * 4 * x, app_size_width / 12 * 3 + app_size_width / 12 * 4 * y, width=6, outline=app_circle_color)

    def draw_cross(self, x, y):
        self.canvas.create_line(self.app_size / 24 + self.app_size / 24 * 8 * x, self.app_size / 24 + self.app_size / 24 * 8 * y, self.app_size / 24 * 7 + self.app_size / 24 * 8 * x, self.app_size / 24 * 7 + self.app_size / 24 * 8 * y, width=10, fill=self.app_cross_color)
        self.canvas.create_line(self.app_size / 24 * 7 + self.app_size / 24 * 8 * x, self.app_size / 24 + self.app_size / 24 * 8 * y, self.app_size / 24 + self.app_size / 24 * 8 * x, self.app_size / 24 * 7 + self.app_size / 24 * 8 * y, width=10, fill=self.app_cross_color)


class Error(Tk):
    def __init__(self, name: str, desc: str):
        super().__init__("err")
        self.app_bg = 'black'
        self.app_fg = 'white'
        self.app_circle_color = 'blue'
        self.app_cross_color = 'red'

        self.title("Erreur")
        # self.resizable(False, False)
        self.geometry("300x300")
        self.configure(background=self.app_bg)
        try:
            self.iconbitmap("tic_tac_toe.ico")
        except Exception:
            pass

        self.name, self.desc = name, desc

        self.name_label = Label(self, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), wraplengt=300, text=name)
        self.name_label.pack(side=TOP, pady=10)

        self.desc_label = Label(self, bg=self.app_bg, fg=self.app_fg, wraplengt=300, text=desc)
        self.desc_label.pack(side=TOP, pady=10)

        self.opt_frame = Frame(self, bg=self.app_bg)
        self.cont_frame = Frame(self.opt_frame, bg=self.app_circle_color)
        self.cont_btn = Button(self.cont_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_circle_color, fg=self.app_circle_color,
                               highlightcolor=self.app_circle_color, font=("", 12, "bold"), text="Continuer !",
                               command=self.destroy)
        self.cont_btn.pack(padx=1, pady=1)
        self.cont_frame.pack(side=LEFT, padx=5)
        self.quit_frame = Frame(self.opt_frame, bg=self.app_cross_color)
        self.quit_btn = Button(self.quit_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_cross_color, fg=self.app_cross_color,
                               highlightcolor=self.app_cross_color, font=("", 12, "bold"), text="Quitter.",
                               command=lambda: sys.exit(1))
        self.quit_btn.pack(padx=1, pady=1)
        self.quit_frame.pack(side=RIGHT, padx=5)
        self.opt_frame.pack(side=BOTTOM, pady=5)

        self.bind("<Configure>", self.event_handler)
        self.quit_btn.focus_set()

        self.mainloop()

    def event_handler(self, event=None):
        new_wrap = int(self.winfo_geometry().split("x")[0]) - 5
        self.name_label.config(wraplengt=new_wrap)
        self.desc_label.config(wraplengt=new_wrap)


class Update(Thread):
    def __init__(self, from_version: manager.GameVersion = manager.GameVersion(),
                 to_version: manager.GameVersion = manager.GameVersion()):
        super().__init__()
        self.running = True

        self.from_version, self.to_version = from_version, to_version
        self.tk: Tk = None

    def stop(self):
        self.running = False
        if self.tk:
            self.tk.destroy()
        raise Exception("Thread Ending.")

    def run(self):
        self.tk = Tk("update")
        self.app_bg = 'black'
        self.app_fg = 'white'

        self.tk.title("Mise-à-Jour")
        self.tk.geometry("375x320")
        self.tk.configure(background=self.app_bg)
        try:
            self.tk.iconbitmap("tic_tac_toe.ico")
        except Exception:
            pass

        self.magic_frame = Frame(self.tk)
        self.internal_frame = Frame(self.magic_frame, bg=self.app_bg)

        self.magic_frame.pack_propagate(0)
        self.internal_frame.pack_propagate(0)

        self.title_frame = Frame(self.internal_frame, bg=self.app_bg)
        self.name_label = Label(self.title_frame, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), text="Mise-à-Jour")
        self.name_label.pack(side=TOP)

        self.version_label = Label(self.title_frame, bg=self.app_bg, fg=self.app_fg, font=("", 12, "bold"), text=f"{self.from_version}  →  {self.to_version}")
        self.version_label.pack(side=TOP)
        self.title_frame.pack(side=TOP, fill=X, expand=True, pady=20, padx=20)

        self.desc_label = Label(self.internal_frame, bg=self.app_bg, fg=self.app_fg, text="Nous remettons à jour votre jeu pour vous assurer une experience sans égale. Actuellement, nous transferont et compilons les nouveaux fichiers depuis la base de donnée. Si le jeu est important ou que votre connexion est mauvaise, l'action peut durer plusieurs minutes... Revenez un peu plus tard. (Temps éstimé: 5sec)")
        self.desc_label.pack(side=BOTTOM, pady=20, padx=20)

        self.internal_frame.pack(fill=BOTH, expand=True, padx=7, pady=7)
        self.magic_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        self.tk.protocol("WM_DELETE_WINDOW", self.quit)
        self.tk.bind("<Configure>", self.on_configure)

        while self.running:
            self.loop()
            self.tk.mainloop()

    def quit(self):
        if not self.running:
            self.stop()

    def on_configure(self, e=None):
        wrap = int(self.tk.winfo_geometry().split("x")[0]) - 114  # 114 -> padx: 2*30 + 2*7 + 2*20
        self.name_label.config(wraplengt=wrap)
        self.desc_label.config(wraplengt=wrap)

    def loop(self, infinite=True, random=True):
        path = ["000", "100", "110", "010", "011", "001", "101", "111"]
        color = [0, 0, 0]
        while self.running:
            temp_path = path[:]
            if random:
                shuffle(temp_path)
            for p in temp_path:
                run = True
                while run and self.running:
                    run = False
                    for i in range(len(color)):
                        if p[i] == "0" and color[i] != 0:
                            color[i] -= 2 if color[i] - 2 > 0 else 1
                            run = True
                        elif p[i] == "1" and color[i] != 255:
                            color[i] += 2 if color[i] + 2 < 256 else 1
                            run = True
                    str_color = "#{color[0]:0>2X}{color[1]:0>2X}{color[2]:0>2X}".format(color=color)
                    self.magic_frame.configure(bg=str_color)
                    self.tk.update()
                    sleep(0.0001)
            if not infinite:
                break


class Scores(Tk):
    def __init__(self, wins: int, looses: int, special: str = None):
        super().__init__("err")
        self.app_bg = 'black'
        self.app_fg = 'white'
        self.app_circle_color = 'blue'
        self.app_cross_color = 'red'
        self.app_green = '#00FF00'
        self.app_special = '#FF00FF'

        self.title("Scores")
        self.geometry("400x350")
        self.configure(background=self.app_bg)
        try:
            self.iconbitmap("tic_tac_toe.ico")
        except Exception:
            pass

        self.wins, self.looses, self.special = wins, looses, special

        self.name_label = Label(self, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), text="Scores")
        self.name_label.pack(side=TOP, pady=10)

        self.desc_label = Label(self, bg=self.app_bg, fg=self.app_fg, text=f"Calcul des scores pour {self.wins + self.looses} parties ({self.wins} victoires et {self.looses} défaites).")
        self.desc_label.pack(side=TOP)

        self.grid_frame = Frame(self, bg=self.app_bg)

        self.exp_title = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="EXP", width=7)
        self.gp_title = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="GP", width=7)
        self.wins_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Bonus de Victoire :")
        self.looses_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Malus de Défaites :")
        self.mul_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Multiplicateur d'EXP :")
        self.red_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Réducteur aléatoire de GP :")
        self.total_label = Label(self.grid_frame, bg=self.app_bg, fg=self.app_fg, text="Total des Récompenses :")

        self.v_wins_exp = wins ** 1.06 * 10
        self.v_wins_gp = wins ** 1.04 * 1.5
        self.v_looses_exp = -(looses ** 0.95 * 8)
        self.v_looses_gp = -(looses ** 0.85 * 2)
        self.v_mul = (1 + (wins - looses) / (2 * (wins + looses))) if wins + looses else 1
        self.v_red = float(choice("012345") + "." + choice("0123456789"))
        self.v_total_exp = (self.v_wins_exp + self.v_looses_exp) * self.v_mul
        self.v_total_gp = (self.v_wins_gp + self.v_looses_gp) * (1 - self.v_red / 100)
        self.v_total_exp = int(self.v_total_exp) if self.v_total_exp > 0 else 0
        self.v_total_gp = int(self.v_total_gp) if self.v_total_gp > 0 else 0

        self.wins_exp = Label(self.grid_frame, **self.nargs(self.v_wins_exp, suffix=" EXP"))
        self.wins_gp = Label(self.grid_frame, **self.nargs(self.v_wins_gp, suffix=" GP"))

        self.looses_exp = Label(self.grid_frame, **self.nargs(self.v_looses_exp, suffix=" EXP"))
        self.looses_gp = Label(self.grid_frame, **self.nargs(self.v_looses_gp, suffix=" GP"))

        self.mul_exp = Label(self.grid_frame, **self.sargs("* {:+.2f} EXP".format(self.v_mul), self.app_green if self.v_mul >= 0 else self.app_cross_color))
        self.red_gp = Label(self.grid_frame, **self.sargs(f"{-self.v_red}% GP", self.app_cross_color))

        self.total_exp = Label(self.grid_frame, **self.nargs(self.v_total_exp, suffix=" EXP", color=COLOR_EXP))
        self.total_gp = Label(self.grid_frame, **self.nargs(self.v_total_gp, suffix=" GP", color=COLOR_GP))
        if special:
            self.total_special = Label(self.grid_frame, **self.sargs(special))

        self.exp_title.grid(**self.gargs(0, 1, sticky=W, pady=10))
        self.gp_title.grid(**self.gargs(0, 2, sticky=W, pady=10))
        self.wins_label.grid(**self.gargs(1, 0, sticky=W))
        self.looses_label.grid(**self.gargs(2, 0, sticky=W))
        self.mul_label.grid(**self.gargs(3, 0, sticky=W))
        self.red_label.grid(**self.gargs(4, 0, sticky=W))
        Frame(self.grid_frame, height=3, bg=self.app_fg).grid(**self.gargs(5, 0, 1, 3, pady=10))
        self.total_label.grid(**self.gargs(6, 0, sticky=W))

        self.wins_exp.grid(**self.gargs(1, 1))
        self.wins_gp.grid(**self.gargs(1, 2))
        self.looses_exp.grid(**self.gargs(2, 1))
        self.looses_gp.grid(**self.gargs(2, 2))
        self.mul_exp.grid(**self.gargs(3, 1))
        self.red_gp.grid(**self.gargs(4, 2))
        self.total_exp.grid(**self.gargs(6, 1))
        self.total_gp.grid(**self.gargs(6, 2))
        if special:
            self.total_special.grid(**self.gargs(7, 1, 1, 2, sticky="e"))

        self.grid_frame.pack(side=TOP, pady=10)

        self.cont_frame = Frame(self, bg=self.app_green)
        self.cont_btn = Button(self.cont_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_green, fg=self.app_green,
                               highlightcolor=self.app_green, font=("", 12, "bold"), text="Quitter",
                               command=self.destroy)
        self.cont_btn.pack(padx=1, pady=1)
        self.cont_frame.pack(side=BOTTOM, pady=5)

        self.bind("<Return>", lambda x: self.destroy())
        self.cont_btn.focus_set()

    def start(self):
        self.mainloop()

    def nargs(self, exp: int | float, prefix: str = None, suffix: str = None, color: str = None):  # n args
        return {"bg": self.app_bg, "fg": color if color else (self.app_green if exp >= 0 else self.app_cross_color),
                "text": (f"{prefix}" if prefix else "") + "{:+}".format(int(exp)) + (f"{suffix}" if suffix else "")}

    def sargs(self, special: str, color: str = None):  # special args
        return {"bg": self.app_bg, "fg": color if color else COLOR_SPECIAL, "text": str(special)}

    def gargs(self, row, column, rowspan=1, columnspan=1, sticky=NE+SW, padx=15, pady=1):  # grid args
        return {"row": row, "column": column, "rowspan": rowspan, "columnspan": columnspan, "padx": padx, "pady": pady,
                "ipadx": 5, "sticky": sticky}


CONTINUE = "\n\nIf you Continue, you will not be able to get rewards and update the ranking."
try:
    manager.setup(GAME_UUID, GAME_VERSION, up_to_date=False)
except manager.UserParameterExpected as e:
    Error("UserParameterExpected", str(e) + "\nYou must run the game from the Launcher to avoid this error." + CONTINUE)
except DatabaseConnexionError as e:
    Error("DatabaseConnexionError", str(e) + "\nThe SQL Serveur is potentially down for maintenance...\nWait and Retry Later." + CONTINUE)
except UserNotFoundException as e:
    Error("UserNotFoundException", str(e) + "\nThe user information given does not match with any user." + CONTINUE)

if not manager.updated():
    u = Update(manager.__current_version, manager.__game_info.version)
    u.start()
    manager.update()
    try:
        u.stop()
    except Exception:
        pass

TicTacToe().start()
