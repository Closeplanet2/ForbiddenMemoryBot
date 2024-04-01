from Scripts._LIBS.JSONController import JSONController
from difflib import SequenceMatcher
from enum import Enum
import numpy as np

STORED_CARDS_FILE_PATH = "StoredData/CardData.json"
FUSION_DATA_FILE_PATH = "StoredData/FusionData.json"
ALREADY_VISITED_NAMES_FILE_PATH = "StoredData/SerialisedNames.json"

class CardAreas(Enum):
    PlayerMonsters = 1
    PlayerSpells = 2
    PlayerHand = 3
    AIMonsters = 4
    AISpells = 5

class CardType(Enum):
    FUSION_MONSTER = 0
    MONSTER = 1
    SPELL = 2
    TRAP = 3

class PlayStyle(Enum):
    NO_PLAY = 0
    FACE_UP = 1
    FACE_DOWN = 2

class CardPositions(Enum):
    ATK = 1
    DEF = 2

class GameData:
    def __init__(self, debug_info=True):
        self.debug_info = debug_info
        self.callback_classes = []
        self.card_areas = {}
        self.clear_card_area(CardAreas.PlayerMonsters, trigger_callback=False)
        self.clear_card_area(CardAreas.PlayerSpells, trigger_callback=False)
        self.clear_card_area(CardAreas.PlayerHand, trigger_callback=False)
        self.clear_card_area(CardAreas.AIMonsters, trigger_callback=False)
        self.clear_card_area(CardAreas.AISpells, trigger_callback=False)
        self.stored_cards = JSONController().return_dict_from_json(STORED_CARDS_FILE_PATH, False)
        self.stored_fusion_combos = JSONController().return_dict_from_json(FUSION_DATA_FILE_PATH, False)
        self.stored_visited_names = JSONController().return_dict_from_json(ALREADY_VISITED_NAMES_FILE_PATH, False)

    def return_stored_cards(self):
        return self.stored_cards['Cards']

    def return_card_by_id(self, card_id):
        for card in self.return_stored_cards():
            if card['CardID'] is card_id:
                return card
        return None

    def return_card_by_name(self, card_name):
        for card in self.return_stored_cards():
            if card['CardName'] == card_name:
                return card
        return None

    def return_fusion_combos_from_fusion(self, card_id):
        return self.stored_fusion_combos[card_id] if card_id in self.stored_fusion_combos else None

    def find_card_with_closest_name(self, text):
        if text in self.stored_visited_names:
            stored_name = self.stored_visited_names[text]
            print(f"{text}:{stored_name}")
            return self.return_card_by_name(stored_name)

        highest_score = 0
        highest_card = None
        for card in self.stored_cards['Cards']:
            score = SequenceMatcher(None, card['CardName'], text).ratio()
            if score > highest_score:
                highest_score = score
                highest_card = card
        self.stored_visited_names[text] = highest_card['CardName']
        print(f"{text}:{highest_card['CardName']}")
        JSONController().dump_dict_to_json(self.stored_visited_names, file=ALREADY_VISITED_NAMES_FILE_PATH, overwrite=False)
        return highest_card

    def add_callback_functions(self, callback_class):
        self.callback_classes.append(callback_class)

    def call_callback_functions(self, card_area: CardAreas, card_added, card):
        for callback_class in self.callback_classes:
            func = getattr(callback_class, card_area.name, None)
            if func is not None and callable(func):
                func(card_added, card)

    def return_cards_from_area(self, card_area: CardAreas):
        return self.card_areas[card_area.name] if card_area.name in self.card_areas else []

    def return_cards_from_area_with_pos(self, card_area: CardAreas, card_pos: CardPositions):
        set_data = []
        for card in self.return_cards_from_area(card_area):
            if "POS" not in card: continue
            if card["POS"] == card_pos.name: set_data.append(card)
        return set_data

    def return_card_from_index(self, card_area: CardAreas, index):
        return self.card_areas[card_area.name][index]

    def move_card_between_areas(self, card_areaA: CardAreas, card_areaB: CardAreas, card):
        self.remove_card_from_area(card_areaA, card)
        self.add_card_to_area(card_areaB, card)

    def add_card_to_area(self, card_area: CardAreas, card):
        self.card_areas[card_area.name].append(card)
        self.call_callback_functions(card_area, True, card)

    def remove_card_from_area(self, card_area: CardAreas, card):
        self.card_areas[card_area.name].remove(card)
        self.call_callback_functions(card_area, False, card)

    def is_card_in_area(self, card_area: CardAreas, card):
        for x in self.card_areas[card_area.name]:
            if x['CardID'] == card['CardID']: return True
        return False

    def index_card_from_area(self, card_area: CardAreas, card):
        return self.card_areas[card_area.name].index(card)

    def set_card_at_index(self, card_area: CardAreas, card, index):
        self.card_areas[card_area.name][index] = card
        self.call_callback_functions(card_area, True, card)

    def pop_card_at_index(self, card_area: CardAreas, index):
        card = self.return_card_from_index(card_area, index)
        self.card_areas[card_area.name].pop(index)
        self.call_callback_functions(card_area, False, card)

    def clear_card_area(self, card_area: CardAreas, trigger_callback=False):
        cards = self.return_cards_from_area(card_area)
        self.card_areas[card_area.name] = []
        if not trigger_callback: return
        for card in cards:
            self.call_callback_functions(card_area, False, card)

    def return_highest_stat_for_areas(self, hand_area, field_area, stat_key="CardAtk", normal=True, fusion=True):
        highest_atk = 0
        highest_card = None
        card_type = None

        #check every card in the hand
        if normal:
            for card in hand_area:
                #if the key is missing or the len of the data is 0, we should skip
                if stat_key not in card: continue
                if len(card[stat_key]) == 0: continue
                if int(card[stat_key]) > highest_atk:
                    highest_atk = int(card[stat_key])
                    highest_card = card
                    card_type = CardType.MONSTER

        if fusion:
            for card in self.return_all_fusions_based_on_cards(hand_area, field_area):
                #if the key is missing or the len of the data is 0, we should skip
                if stat_key not in card: continue
                if len(card[stat_key]) == 0: continue
                if int(card[stat_key]) > highest_atk:
                    highest_atk = int(card['CardATK'])
                    highest_card = card
                    card_type = CardType.FUSION_MONSTER

        return highest_card, highest_atk, card_type

    def return_all_fusions_based_on_cards(self, hand_area, field_area):
        fusions_to_make = []
        full_cards_from_area = hand_area + field_area
        for fusion_id in self.stored_fusion_combos:
            for index_a in range(0, len(full_cards_from_area), 1):
                card_a = full_cards_from_area[index_a]
                card_a_id = card_a['CardID']
                if card_a_id in self.stored_fusion_combos[fusion_id]:
                    other_cards_in_combos = self.stored_fusion_combos[fusion_id][card_a_id]
                    for index_b in range(0, len(full_cards_from_area), 1):
                        if index_a == index_b: continue
                        card_b = full_cards_from_area[index_b]
                        card_b_id = card_b['CardID']
                        if card_b_id in other_cards_in_combos:
                            fusions_to_make.append(self.return_card_by_id(fusion_id))
        return fusions_to_make

    def return_empty_card(self):
        return {
                    "CardID": "000",
                    "CardName": "BlankCard",
                    "CardAtk": "0",
                    "CardDef": "0",
                    "POS": CardPositions.DEF.name
                }




