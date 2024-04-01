from enum import Enum

class StateList(Enum):
    STARTING_PROGRAM = 0
    GEN_PLAYER_HAND = 1
    FIND_BEST_CARD_TO_PLAY = 2
    GEN_AI_BOARD = 3
    COMBAT = 4
    END_TURN = 5
    END_PROGRAM = 6

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

    async def trigger_state_machine(self, end_program=False):
        if self.current_state is StateList.STARTING_PROGRAM:
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