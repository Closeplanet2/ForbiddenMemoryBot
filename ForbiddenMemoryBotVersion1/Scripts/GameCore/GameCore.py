from Scripts.GameCore.GameUI import GameUI
from Scripts.GameCore.StateMachine import StateMachine, StateList
from Scripts.GameCore.CardStorage import CardAreas, CardStorage
from Scripts.GameCore.CursorCore import CursorCore

from PythonCores.ScreenGrabController import ScreenGrabController
from PythonCores.InputController import InputController
from PythonCores.TextController import TextController

import time
import asyncio

class GameCore:
    def __init__(self, debug_info=True):
        self.auto_trigger = False
        self.turn_count = 0
        self.debug_info = debug_info

        self.card_storage = CardStorage(debug_info)
        self.cursor_core = CursorCore(0, 4, self.left_cursor, self.right_cursor)

        self.screen_grab_controller = ScreenGrabController("RetroArch Beetle PSX HW 0.9.44.1 88929ae", debug_info=debug_info)
        self.input_controller = InputController(debug_info=debug_info)
        self.text_controller = TextController()

        self.state_machine = StateMachine()
        self.state_machine.add_callback_class(self)
        self.game_ui = GameUI(self.next_stage_callback, self.auto_trigger_callback, debug_info)

    def next_stage_callback(self, thread_index, args):
        if self.auto_trigger: return
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.state_machine.trigger_state_machine())
        loop.close()

    def auto_trigger_callback(self, thread_index, args):
        self.auto_trigger = not self.auto_trigger
        if not self.auto_trigger: return
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.state_machine.trigger_state_machine())
        loop.close()

    def left_cursor(self, current_cursor, delay):
        self.input_controller.left_click_button(delay=delay)

    def right_cursor(self, current_cursor, delay):
        self.input_controller.right_click_button(delay=delay)

    async def STARTING_PROGRAM(self):
        await self.Auto_Trigger()

    async def GEN_PLAYER_HAND(self):
        self.turn_count += 1
        if self.debug_info: print(f"{self.turn_count}:[Starting Hand Gen]")

        self.card_storage.clear_card_area(CardAreas.PlayerHand, True)
        screen_pos = self.screen_grab_controller.convert_pos(pos_x=30, pos_y=30)
        self.input_controller.click_pos(posx=screen_pos[0], posy=screen_pos[1])
        self.input_controller.click_button('x')
        await self.cursor_core.set_cursor_position(0, delay=0.5)

        for i in range(0, 5, 1):
            await self.cursor_core.set_cursor_position(i, delay=0.5)
            screenshot = self.screen_grab_controller.take_screenshot_and_crop(box=(35, 676, 588, 742))
            screenshot_text = self.text_controller.image_to_text_pillow(pil_image=screenshot)
            print(screenshot_text)

        await self.Auto_Trigger()

    async def FIND_BEST_CARD_TO_PLAY(self):
        print("3")
        await self.Auto_Trigger()

    async def GEN_AI_BOARD(self):
        print("4")
        await self.Auto_Trigger()

    async def COMBAT(self):
        print("5")
        await self.Auto_Trigger()

    async def END_TURN(self):
        print("6")
        await self.Auto_Trigger()

    async def END_PROGRAM(self):
        print("7")
        await self.Auto_Trigger()

    async def Auto_Trigger(self):
        if self.auto_trigger:
            time.sleep(1)
            await self.state_machine.trigger_state_machine()
