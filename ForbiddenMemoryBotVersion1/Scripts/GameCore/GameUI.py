from PythonCores.TkinterController import TkinterController, DestructionStage
from Scripts.GameCore.GameUISettings import GameUISettings

class GameUI:
    def __init__(self, next_state_callback, auto_trigger_callback, debug_info=True):
        self.game_ui_settings = GameUISettings()
        self.tkinter_controller = TkinterController(debug_info=debug_info)
        self.next_state_callback = next_state_callback
        self.auto_trigger_callback = auto_trigger_callback
        self.create_game_ui_window()

    def create_game_ui_window(self):
        self.tkinter_controller.create_window(
            function_thread_callback=self.tkinter_thread_callback,
            wh=self.game_ui_settings.window_height,
            ww=self.game_ui_settings.window_width,
            wt=self.game_ui_settings.game_ui_title,
            bg=self.game_ui_settings.window_background_color,
            update_gui_per_second=self.game_ui_settings.update_gui_per_second
        )

        self.tkinter_controller.add_button(
            text="Next State!",
            function_callback=self.next_state_callback,
            bg="#FF8181",
            fg="#000000",
            w=int(self.game_ui_settings.window_width / 11),
            h=1,
            x_pos=0,
            y_pos=862,
            destroy_status=DestructionStage.DONT_DESTROY
        )

        self.tkinter_controller.add_button(
            text="Toggle Auto Trigger!",
            function_callback=self.auto_trigger_callback,
            bg="#FF8181",
            fg="#000000",
            w=int(self.game_ui_settings.window_width / 11),
            h=1,
            x_pos=0,
            y_pos=820,
            destroy_status=DestructionStage.DONT_DESTROY
        )

        self.tkinter_controller.start_window()

    def tkinter_thread_callback(self):
        pass