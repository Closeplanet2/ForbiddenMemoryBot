from Scripts.Enums.FilePaths import FilePaths
from Scripts.WebCrawler.CardData import gen_card_data, gen_fusion_data
from Scripts.GameCore.GameCore import GameCore
import os

if bool(input("Do you need to download the card data?")) or not os.path.exists(FilePaths().CardData):
    gen_card_data()

if bool(input("Do you need to download the fusion data? ")) or not os.path.exists(FilePaths().FusionData):
    gen_fusion_data()

#Run the game core
game_core = GameCore(debug_info=True)