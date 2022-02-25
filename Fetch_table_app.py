from helper_funcs import parse_table

import tkinter as tk


class TkApp:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.title("Excel Generator")
        self.frame.geometry('400x200')
        self.match_link = tk.StringVar(self.frame)

    def get_link(self):
        mlink = self.match_link.get()
        # https://www.vlr.gg/73218/100-thieves-vs-tsm-knights-monthly-gauntlet-2022-february-gf
        print("The link is : " + mlink)
        parse_table(mlink)

    def create_window(self):
        match_label = tk.Label(self.frame, text='Match Link', font=('calibre', 10, 'bold'))
        match_label.pack()

        link = tk.Entry(self.frame, textvariable=self.match_link, font=('calibre', 10, 'normal'))
        btn = tk.Button(self.frame, text='Submit', command=self.get_link)
        link.pack()
        btn.pack()
        self.frame.mainloop()


if __name__ == '__main__':
    TkApp().create_window()
