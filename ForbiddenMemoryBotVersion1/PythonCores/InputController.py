import win32api
import win32con
import time
from PythonCores.ThreadController import ThreadController
from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller
controller = Controller()

class InputController:
    def __init__(self, debug_info=False):
        self.debug_info = debug_info

    def listen_for_keyboard(self, on_press, on_release):
        def keyboard_listener_thread(thread_index, args):
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        ThreadController(max_threads=1).load_start(method=keyboard_listener_thread, daemon=True)

    def listen_for_mouse(self, on_click):
        def keyboard_listener_thread(thread_index, args):
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()
        ThreadController(max_threads=1).load_start(method=keyboard_listener_thread, daemon=True)

    def click_pos(self, posx=77, posy=188, delay=0.5):
        win32api.SetCursorPos((posx, posy))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, posx, posy, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, posx, posy, 0, 0)
        time.sleep(delay)

    def click_button(self, key, hold_delay=0.5):
        controller.press(key)
        time.sleep(0.1)
        controller.release(key)
        self.debug_key(key_stroke=key)
        time.sleep(hold_delay)

    def left_click_button(self, delay=0.5):
        controller.press(Key.left)
        time.sleep(0.1)
        controller.release(Key.left)
        self.debug_key(key_stroke=Key.left)
        time.sleep(delay)

    def right_click_button(self, delay=0.5):
        controller.press(Key.right)
        time.sleep(0.1)
        controller.release(Key.right)
        self.debug_key(key_stroke=Key.right)
        time.sleep(delay)

    def up_click_button(self, delay=0.5):
        controller.press(Key.up)
        time.sleep(0.1)
        controller.release(Key.up)
        self.debug_key(key_stroke=Key.right)
        time.sleep(delay)

    def down_click_button(self, delay=0.5):
        controller.press(Key.down)
        time.sleep(0.1)
        controller.release(Key.down)
        self.debug_key(key_stroke=Key.right)
        time.sleep(delay)

    def enter_click_button(self, delay=0.5):
        controller.press(Key.enter)
        time.sleep(0.1)
        controller.release(Key.enter)
        self.debug_key(key_stroke=Key.enter)
        time.sleep(delay)

    def debug_key(self, key_stroke):
        if self.debug_info: print(f"Clicked {key_stroke}")