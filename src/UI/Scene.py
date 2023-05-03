# standard library imports
from __future__ import annotations
import tkinter as tk
from tkinter import filedialog
from abc import abstractmethod
from enum import Enum, auto
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.Controller import Controller

from src.Data.SheetType import SheetType


class SceneType(Enum):
    """Enumeration for the 2 types of sheets

    SELECT for the workbook selection screen
    TYPE for the typing screen
    """

    SELECT = auto()
    TYPE = auto()


class Scene(object):
    """base Class representing how the UI is build

    Attributes
    ----------
    window
        the tkinter instance the app is running on
    frame
        the active frame rendered in tkinter
    sheet_types
        the sheet_types in the active File
    controller
        the controller controlling the UI

    Methods
    -------
    switch(self, scene: Scene)
        method for switching between scenes

    render(self)
        abstract method stub for rendering a scene

    button(frame, text, command, row, col)
        helper method for more clearly building a button

    get_masterframe(cls):
        returns the main tkinter instance running the UI
    """

    def __new__(cls, type: SceneType, *kwargs):
        if type is SceneType.SELECT:
            return super(Scene, SelectScene).__new__(SelectScene)
        if type is SceneType.TYPE:
            return super(Scene, TypeScene).__new__(TypeScene)

    def __init__(self, _, controller: Controller):
        self.window = self.get_masterframe()
        self.frame = None
        self.sheet_types = list(str(st) for st in SheetType)
        self.controller = controller

    def switch(self, scene: Scene):
        if self.frame:
            self.frame.destroy()
        scene.render()

    @abstractmethod
    def render(self):
        pass

    @staticmethod
    def button(frame, text, command, row, col):
        button = tk.Button(master=frame, text=text, width=20, height=1, command=command)
        button.grid(row=row, column=col)
        return button

    @staticmethod
    def get_masterframe():
        if not hasattr(Scene, "masterframe"):
            Scene.masterframe = tk.Tk()
        return Scene.masterframe


class TypeScene(Scene):
    """Class representing the typescene

    Methods
    -------
    render(self)
        implemented method for showing the type screen
    """

    def __init__(self, _, controller: Controller):
        self.sheet_names = controller.file.sheet_names
        self.controller = controller
        super().__init__(None, controller)

    def render(self):
        # create main UI frame
        frame = tk.Frame(master=self.get_masterframe())
        frame.rowconfigure(0, minsize=10, weight=1)
        frame.columnconfigure([0], minsize=50, weight=1)
        # create select_sheet menu
        options = tk.StringVar(frame)
        options.set(self.sheet_names[0])
        data_label = tk.Label(master=frame, text="Geselecteerde sheet")
        data_label.grid(row=1, column=0)
        data = tk.OptionMenu(
            frame, options, *self.sheet_names, command=self.controller.set_active
        )
        data.grid(row=2, column=0)

        # create write_baten button
        self.button(
            frame, "Baten uitschrijven", self.controller.start_write_baten, 3, 0
        )

        # create write_lasten button
        self.button(
            frame, "Lasten uitschrijven", self.controller.start_write_lasten, 3, 1
        )

        # create return to selection screen button
        self.button(frame, "Back", lambda: self.controller.transition_to_select(), 1, 0)

        self.frame = frame
        frame.pack()


class SelectScene(Scene):
    """Class representing the SelectScene

    Methods
    -------
    render(self)
        implemented method for showing the SelectScene
    select_file(self, entry: tk.Entry)
        Subroutine for selecting a file using explorer interface
    show_open_error(self)
        Subroutine for showing an error when something is wrong with object path

    """

    def __init__(self, _, controller: Controller):
        super().__init__(_, controller)

    def render(self):
        # create main UI frame
        frame = tk.Frame(master=self.get_masterframe())
        frame.rowconfigure(0, minsize=10, weight=1)
        frame.columnconfigure([0, 1, 2], minsize=50, weight=1)
        # Create Sheet locatie label
        label = tk.Label(master=frame, text="Sheet locatie")
        label.grid(row=0, column=0)
        # create entry field for manual copy pasting
        entry = tk.Entry(master=frame, width=60)
        entry.grid(row=1, column=0)
        entry.insert(0, self.controller.get_path())
        # create sheet_type field

        options = tk.StringVar(frame)
        options.set(str(self.controller.get_type()))
        data_label = tk.Label(master=frame, text="Sheet type")
        data_label.grid(row=0, column=2)
        data = tk.OptionMenu(
            frame,
            options,
            *[str(type) for type in SheetType],
            command=self.controller.set_type,
        )
        data.grid(row=1, column=2)

        # Create search button
        file_button = tk.Button(
            master=frame,
            text="Zoeken",
            width=5,
            height=1,
            command=lambda: self.select_file(entry),
        )
        file_button.grid(row=1, column=1)

        # Create continue button
        continue_button = tk.Button(
            master=frame,
            text="Openen",
            width=5,
            height=1,
            padx=10,
            pady=5,
            command=lambda: self.controller.transition_to_type(),
        )
        continue_button.grid(row=2, column=0)
        # pack frame and run
        frame.pack()
        self.frame = frame
        self.window.mainloop()

    def select_file(self, entry: tk.Entry):
        self.window.withdraw()
        self.controller.set_path(filedialog.askopenfilename())
        self.window.deiconify()
        entry.delete(0, "end")
        entry.insert(0, self.controller.get_path())

    def show_open_error(self):
        error_label = tk.Label(
            master=self.frame, text="Deze file bestaat niet", fg="red"
        )
        error_label.grid(row=3, column=0)
