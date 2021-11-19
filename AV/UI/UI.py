import tkinter as tk
from configparser import ConfigParser
from os import path
from AV.Controller import Controller
from AV.ControllerData import ControllerData

from tkinter import filedialog

config = ConfigParser()
config.read(path.join(path.dirname(__file__), "../__conf__.ini"))


class UI(object):

    def __init__(self, data: ControllerData):
        self.data = data
        self.window = tk.Tk()
        self.frame = None
        self.controller = Controller(data)

    def transition(self, screen, data=None):
        def callback():
            self.data.current_screen = screen
            if self.data.current_screen == screen:
                if self.data.current_screen == 'select':
                    self.open_screen()
                elif self.data.current_screen == 'type':
                    self.transfer_to_type_screen(*data)
        return callback

    def select_file(self, entry: tk.Entry):
        def select():
            self.window.withdraw()
            self.data.file_path = filedialog.askopenfilename()
            self.window.deiconify()
            entry.delete(0, 'end')
            entry.insert(0, self.data.file_path)

        return select

    def open_screen(self):
        if self.frame is not None:
            self.frame.destroy()
        # create main UI frame
        frame = tk.Frame()
        frame.rowconfigure(0, minsize=10, weight=1)
        frame.columnconfigure([0, 1, 2], minsize=50, weight=1)
        # Create Sheet locatie label
        label = tk.Label(master=frame,
                         text="Sheet locatie")
        label.grid(row=0, column=0)
        # create entry field for manual copy pasting
        entry = tk.Entry(master=frame, width=60)
        entry.grid(row=1, column=0)
        entry.insert(0, self.data.file_path)
        # create sheet_type field

        options = tk.StringVar(frame)
        options.set(str(self.data.sheet_type))
        data_label = tk.Label(master=frame,
                              text="Sheet type")
        data_label.grid(row=0, column=2)
        data = tk.OptionMenu(frame, options, *self.data.sheet_types, command=self.controller.set_sheet_type)
        data.grid(row=1, column=2)

        # Create search button
        file_button = tk.Button(master=frame,
                                text="Zoeken",
                                width=5,
                                height=1,
                                command=self.select_file(entry))
        file_button.grid(row=1, column=1)

        # Create continue button
        continue_button = tk.Button(master=frame,
                                    text="Openen",
                                    width=5,
                                    height=1,
                                    padx=10,
                                    pady=5,
                                    command=self.transition('type', data=[entry]))
        continue_button.grid(row=2, column=0)
        # pack frame and run
        frame.pack()
        self.frame = frame
        self.window.mainloop()

    def show_open_error(self):
        error_label = tk.Label(master=self.frame,
                               text="Deze file bestaat niet",
                               fg='red')
        error_label.grid(row=3, column=0)

    def transfer_to_type_screen(self, entry: tk.Entry):
        try:
            self.data.file_path = entry
            self.controller.set_workbook()
            self.type_screen()
        except FileNotFoundError:
            self.show_open_error()

    def type_screen(self):
        if self.frame is not None:
            self.frame.destroy()
        # create main UI frame
        frame = tk.Frame()
        frame.rowconfigure(0, minsize=10, weight=1)
        frame.columnconfigure([0], minsize=50, weight=1)
        # create select_sheet menu
        options = tk.StringVar(frame)
        options.set(self.data.sheet_name)
        data_label = tk.Label(master=frame,
                              text="Geselecteerde sheet")
        data_label.grid(row=1, column=0)
        data = tk.OptionMenu(frame, options,
                             *self.data.sheet_names,
                             command=self.controller.set_sheet_name)
        data.grid(row=2, column=0)
        # create write_baten button
        self.button(frame, "Baten uitschrijven", self.controller.start_write_baten, 3, 0)

        # create write_lasten button
        self.button(frame, "Lasten uitschrijven", self.controller.start_write_lasten, 3, 1)

        # create return to selection screen button
        self.button(frame, "Back", self.transition('select'), 1, 0)

        self.frame = frame
        frame.pack()

    def button(self, frame, text, command, row, col):
        button = tk.Button(master=frame,
                           text=text,
                           width=20,
                           height=1,
                           command=command)
        button.grid(row=row, column=col)
        return button


if __name__ == '__main__':
    ui = UI(ControllerData())
    ui.open_screen()
