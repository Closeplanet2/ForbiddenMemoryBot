from tkinter import Tk, Label, Button
from PythonCores.ThreadController import ThreadController
from PIL import ImageTk, Image
from enum import Enum
import time

class DestructionStage(Enum):
    DESTROY = 0
    DELAYED_DESTROY = 1
    DONT_DESTROY = 2

class TkinterController:
    def __init__(self, debug_info=True):
        self.callback_functions = []
        self.current_window = None
        self.debug_info = debug_info

    # Window Height, Window Width, Window Title, Scale Width, Scale Height, Background Color
    def create_window(self, function_thread_callback, wh=900, ww=400, wt="Title", sw=False, sh=False, bg="#000000", update_gui_per_second=1):
        self.current_window = TkinterClass(wh, ww, wt, sw, sh, bg, self.widget_thread_callback, function_thread_callback, update_gui_per_second)
        if self.debug_info: print(f"Window Created: {wt}")

    def destroy_widgets(self, current_window):
        if not current_window is None:
            current_window.destroy_widgets()

    def add_callback_function(self, callback_function):
        self.callback_functions.append(callback_function)
        if self.debug_info: print("Callback Function Added!")

    def start_window(self):
        if self.current_window is None:
            if self.debug_info: print("Current Window Is Null!")
        else:
            if self.debug_info: print("Starting Window....")
            self.current_window.mainloop()

    # Text, Background Color, Foreground Color, Width, Height, x_pos, y_pos, Font Size, Font Family, allow destroy
    def add_label(self, text="Text Here", bg="#000000", fg="#ffffff", w=10, h=10, x_pos=0, y_pos=0, fs=14, ff="Helvetica", destroy_status=None):
        if not self.current_window is None:
            self.current_window.add_label(text, bg, fg, w, h, x_pos, y_pos, fs, ff, destroy_status)

    def add_button(self, text="Text Here", function_callback=None, bg="#000000", fg="#FFFFFF", w=10, h=10, x_pos=10, y_pos=10, fs=14, ff="Helvetica", destroy_status=None):
        if not self.current_window is None:
            self.current_window.add_button(text, function_callback, bg, fg, w, h, x_pos, y_pos, fs, ff, destroy_status)

    def add_image_as_grid(self, card_image, w=5, h=5, pos_x=5, pos_y=5, offset_x=88, offest_y=129, numx=3, numy=2, index=0, destroy_status=None):
        if not self.current_window is None:
            self.current_window.add_image_as_grid(card_image, w, h, pos_x, pos_y, offset_x, offest_y, numx, numy, index, destroy_status)

    def widget_thread_callback(self):
        if not self.current_window is None:
            for callback_function in self.callback_functions:
                callback_function(self.current_window)

class TkinterClass(Tk):
    # Window Height, Window Width, Window Title, Scale Width, Scale Height, Background Color
    def __init__(self, wh, ww, wt, sw, sh, bg, widget_thread_callback, function_thread_callback, update_gui_per_second):
        super().__init__()
        self.ignore_destruction = {}
        self.main_loop_running = True
        self.update_gui_per_second = update_gui_per_second
        self.widget_thread_callback = widget_thread_callback
        self.function_thread_callback = function_thread_callback
        self.ThreadController = ThreadController(max_threads=1)
        self.ThreadController.load_threads(self.callback_widget_thread_callback, True)
        self.ThreadController.load_threads(self.callback_function_thread_callback, True)
        self.ThreadController.start_all_threads()
        self.set_values(wh, ww, wt, sw, sh, bg)

    def callback_widget_thread_callback(self, thread_index, args):
        while self.main_loop_running:
            self.widget_thread_callback()
            time.sleep(1 / self.update_gui_per_second)

    def callback_function_thread_callback(self, thread_index, args):
        while self.main_loop_running:
            self.function_thread_callback()
            time.sleep(1 / self.update_gui_per_second)

    # Window Height, Window Width, Window Title, Scale Width, Scale Height, Background Color
    def set_values(self, wh, ww, wt, sw, sh, bg):
        self.title(wt)
        self.geometry(f"{ww}x{wh}+0+0")
        self.resizable(width=sw, height=sh)
        self.configure(bg=bg)

    def destroy_widgets(self):
        for widget in self.winfo_children():
            if self.ignore_destruction[widget] is DestructionStage.DONT_DESTROY: continue
            elif self.ignore_destruction[widget] is DestructionStage.DELAYED_DESTROY: self.ignore_destruction[widget] = DestructionStage.DESTROY
            elif self.ignore_destruction[widget] is DestructionStage.DESTROY:
                self.ignore_destruction.pop(widget)
                widget.destroy()

    # Text, Background Color, Foreground Color, Width, Height, x_pos, y_pos, Font Size, Font Family, allow destroy
    def add_label(self, text="Text Here", bg="#000000", fg="#ffffff", w=10, h=10, x_pos=0, y_pos=0, fs=14, ff="Helvetica", destroy_status=None):
        label = Label(self, text=text, font=(ff, fs), fg=fg, bg=bg)
        label.place(x=x_pos, y=y_pos)
        label.config(width=w, height=h)
        if destroy_status is None: destroy_status = DestructionStage.DONT_DESTROY
        self.ignore_destruction[label] = destroy_status

    def add_button(self, text="Text Here", function_callback=None, bg="#000000", fg="#FFFFFF", w=10, h=10, x_pos=10, y_pos=10, fs=14, ff="Helvetica", destroy_status=None):
        def button_callback():
            if function_callback:
                thread = ThreadController(max_threads=1).load_start(function_callback, daemon=True)
        button = Button(self, text=text, command=button_callback, bg=bg, fg=fg, font=(ff, fs))
        button.place(x=x_pos, y=y_pos)
        button.config(width=w, height=h)
        if destroy_status is None: destroy_status = DestructionStage.DONT_DESTROY
        self.ignore_destruction[button] = destroy_status

    def add_image_as_grid(self, card_image, w=5, h=5, pos_x=5, pos_y=5, offset_x=88, offest_y=129, numx=3, numy=2, index=0, destroy_status=None):
        mathx = int(index % numx)
        mathy = int(index / numx)
        posx = pos_x + (mathx * offset_x)
        posy = pos_y + (mathy * offest_y) + (int(index / numx) * numx * numy)

        card_image = card_image.resize((w, h), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(card_image)
        label = Label(self, image=render)
        label.image = render
        label.place(x=posx, y=posy)

        if destroy_status is None: destroy_status = DestructionStage.DONT_DESTROY
        self.ignore_destruction[label] = destroy_status