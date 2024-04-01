from PythonCores.JSONController import JSONController
from Scripts.Enums.FilePaths import FilePaths

class CardData:
    def __init__(self):
        self.stored_cards = JSONController().return_dict_from_json(FilePaths().CardData)
        self.stored_fusion_combos = JSONController().return_dict_from_json(FilePaths().FusionData)

    def return_stored_cards(self):
        return self.stored_cards['Cards']

    def return_card_by_id(self, card_id):
        for card in self.return_stored_cards():
            if card['CardID'] is card_id:
                return card
        return None

    def return_card_by_name(self, card_name):
        for card in self.return_stored_cards():
            if card['CardName'] is card_name:
                return card
        return None

    def return_fusion_combos_from_fusion(self, card_id):
        return self.stored_fusion_combos[card_id] if card_id in self.stored_fusion_combos else None