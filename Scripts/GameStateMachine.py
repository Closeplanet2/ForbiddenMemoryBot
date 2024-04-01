from enum import Enum
import asyncio

class StateList(Enum):
    PRELOAD_EVENT = 0
    STARTING_PROGRAM = 1
    GEN_PLAYER_BOARD = 2
    GEN_PLAYER_HAND = 3
    FIND_BEST_CARD_TO_PLAY = 4
    GEN_AI_BOARD = 5
    COMBAT = 6
    END_TURN = 7
    END_PROGRAM = 8

class StateMachine:
    def __init__(self, debug_state_machine=True):
        self.current_state = StateList.STARTING_PROGRAM
        self.callback_classes = []
        self.debug_state_machine = debug_state_machine

    async def call_callback_classes(self):
        for callback_class in self.callback_classes:
            func = getattr(callback_class, self.current_state.name, None)
            if func is not None and callable(func):
                await func()

    def add_callback_class(self, callback_class):
        self.callback_classes.append(callback_class)

    def reset_state_machine(self):
        self.current_state = StateList.PRELOAD_EVENT

    def trigger_state_machine_async(self, end_program=False):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.trigger_state_machine(end_program=end_program))
        loop.close()

    async def trigger_state_machine(self, end_program=False):
        if self.current_state is StateList.PRELOAD_EVENT:
            self.current_state = StateList.STARTING_PROGRAM
        elif self.current_state is StateList.STARTING_PROGRAM:
            self.current_state = StateList.GEN_PLAYER_BOARD
        elif self.current_state is StateList.GEN_PLAYER_BOARD:
            self.current_state = StateList.GEN_PLAYER_HAND
        elif self.current_state is StateList.GEN_PLAYER_HAND:
            self.current_state = StateList.FIND_BEST_CARD_TO_PLAY
        elif self.current_state is StateList.FIND_BEST_CARD_TO_PLAY:
            self.current_state = StateList.GEN_AI_BOARD
        elif self.current_state is StateList.GEN_AI_BOARD:
            self.current_state = StateList.COMBAT
        elif self.current_state is StateList.COMBAT:
            self.current_state = StateList.END_TURN
        elif self.current_state is StateList.END_TURN:
            self.current_state = StateList.END_PROGRAM if end_program else StateList.GEN_PLAYER_HAND
        await self.call_callback_classes()