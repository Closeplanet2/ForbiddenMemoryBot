from enum import Enum

class CardAreas(Enum):
    PlayerMonsters = 1
    PlayerSpells = 2
    PlayerHand = 3
    AIMonsters = 4
    AISpells = 5

class CardStorage:
    def __init__(self, debug_info=True):
        self.debug_info = debug_info
        self.callback_functions = []
        self.card_areas = {}
        self.card_areas[CardAreas.PlayerMonsters.name] = []
        self.card_areas[CardAreas.PlayerSpells.name] = []
        self.card_areas[CardAreas.PlayerHand.name] = []
        self.card_areas[CardAreas.AIMonsters.name] = []
        self.card_areas[CardAreas.AISpells.name] = []

    def add_callback_functions(self, callback_function):
        self.callback_functions.append(callback_function)

    def call_callback_functions(self, card_area, card_added, card):
        for callback_function in self.callback_functions:
            callback_function(card_area, card_added, card)

    def return_cards_from_area(self, card_area):
        return self.card_areas[card_area.name]

    def return_card_from_index(self, card_area, index):
        return self.card_areas[card_area.name][index]

    def move_card_between_areas(self, card_areaA, card_areaB, card):
        self.remove_card_from_area(card_areaA, card)
        self.add_card_to_area(card_areaB, card)

    def add_card_to_area(self, card_area, card):
        self.card_areas[card_area.name].append(card)
        self.call_callback_functions(card_area, True, card)

    def remove_card_from_area(self, card_area, card):
        self.card_areas[card_area.name].pop(card)
        self.call_callback_functions(card_area, False, card)

    def is_card_in_area(self, card_area, card):
        for x in self.card_areas[card_area.name]:
            if x['CardID'] == card['CardID']: return True
        return False

    def index_card_from_area(self, card_area, card):
        return self.card_areas[card_area.name].index(card)

    def set_card_at_index(self, card_area, card, index):
        self.card_areas[card_area.name][index] = card
        self.call_callback_functions(card_area, True, card)

    def pop_card_at_index(self, card_area, index):
        card = self.return_card_from_index(card_area, index)
        self.card_areas[card_area.name].pop(index)
        self.call_callback_functions(card_area, False, card)

    def clear_card_area(self, card_area, trigger_callback=False):
        cards = self.return_cards_from_area(card_area)
        self.card_areas[card_area.name].clear()
        if not trigger_callback: return
        for card in cards:
            self.call_callback_functions(card_area, False, card)