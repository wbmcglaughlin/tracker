import json
from tkinter import *
import platform
import logging

if platform.system() == "Darwin":
    from tkmacosx import Button

from Scripts.Tracker import Tracker


class Gui:
    def __init__(self, canvas_width, canvas_height):
        self.root = Tk()

        with open("./Information/config.json", "r") as config_file:
            config = json.load(config_file)

        saves_file_path = config["saves"]

        self.tracker = Tracker(saves_file_path)
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.logger = logging.getLogger("gui")
        self.logger.setLevel(logging.INFO)

        self.canvas = Canvas(self.root,
                             width=canvas_width,
                             height=canvas_height,
                             background=rgb_hack((255, 255, 255)),
                             borderwidth=0,
                             highlightthickness=0,
                             border=0,
                             relief='ridge')

        self.root.resizable(False, False)

        options_list = self.tracker.get_current_worlds()
        self.value_inside = StringVar(self.root)
        self.value_inside.set("World Selection")

        self.option_menu = OptionMenu(self.canvas, self.value_inside, *options_list)

        self.start_button = Button(self.canvas,
                                   bd=0,
                                   text="Start Tracker",
                                   command=self.start
                                   )

    def show(self):
        self.canvas.pack()
        self.canvas.create_window(self.canvas_width / 2, 10, anchor="n", window=self.option_menu)
        self.canvas.create_window(self.canvas_width / 2, 100, anchor="n", window=self.start_button)

        for c in sorted(self.canvas.children):
            self.canvas.children[c].pack()

        self.root.mainloop()

    def start(self):
        self.logger.info("Starting Tracker")
        self.tracker.world_name = str(self.value_inside.get())
        self.tracker.setup()
        self.root.after(60 * 1000, self.run_loop)

    def run_loop(self):
        self.tracker.run_loop()
        self.root.after(5000, self.run_loop)


def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb
