from Scripts.GameStateMachine import StateMachine
from Scripts.GameData import GameData, CardAreas, CardType, PlayStyle, CardPositions
from Scripts.CursorCore import CursorCore
from Scripts._LIBS.ScreenGrabController import ScreenGrabController
from Scripts._LIBS.InputController import InputController
from Scripts._LIBS.TextController import TextController
import time

WINDOW_NAME = "RetroArch Beetle PSX HW 0.9.44.1 88929ae"
MENU_TO_EXIT_START = 2
MAX_CARDS_IN_HAND = 5
MAX_CARDS_IN_FIELD = 5
CURSOR_DELAY = 0.5
START_POS = (30, 30)
COORD_CROP_CARDS_US = (35, 676, 588, 742)
COORD_CROP_CARDS_TEST_EMPTY = (47, 675, 848, 734)
COORD_CROP_CARDS_TEST_CARD =  (47, 675, 583, 734)
ARRAY_COLORS_FOR_EMPTY_SPACE = [(0, 0, 0), (3.1, 3.1, 3.1), (8, 8, 8)]


class GameCore:
    def __init__(self, debug_info=False):
        self.first_turn = True
        self.game_data = GameData()
        self.game_data.add_callback_functions(self)
        self.cursor_core = CursorCore(0, MAX_CARDS_IN_HAND - 1, self.LEFT_CURSOR, self.RIGHT_CURSOR)
        self.screen_grab = ScreenGrabController(window_name=WINDOW_NAME, debug_info=debug_info)
        self.input_core = InputController()
        self.text_controller = TextController()
        self.state_machine = StateMachine()
        self.state_machine.add_callback_class(self)

    def game_loop(self):
        self.state_machine.trigger_state_machine_async(end_program=False)

    def LEFT_CURSOR(self, current_cursor, delay):
        self.input_core.left_click_button(delay=delay)

    def RIGHT_CURSOR(self, current_cursor, delay):
        self.input_core.right_click_button(delay=delay)

    async def STARTING_PROGRAM(self):
        print("Starting Program......")
        await self.state_machine.trigger_state_machine(end_program=False)

    async def GEN_PLAYER_BOARD(self):
        print("Generate Player Board Data....")

        # Find the screen pos with the offset of the small window
        screen_pos = self.screen_grab.convert_pos(pos_x=START_POS[0], pos_y=START_POS[1])
        # Find click on the window, close any menus that may be open, and reset the player cursor to 0
        self.input_core.click_pos(posx=screen_pos[0], posy=screen_pos[1])

        for i in range(0, MENU_TO_EXIT_START, 1):
            print(f"Exit out of menu {i}")
            self.input_core.click_button('x')

        print("Default Cursor to 0!")
        await self.cursor_core.default_cursor(delay=CURSOR_DELAY)

        # setup the game for first turn
        if self.first_turn:
            await self.state_machine.trigger_state_machine(end_program=False)
            return

    async def GEN_PLAYER_HAND(self):
        print("Generate Player Hand StoredData....")

        # loop through every card in the player hand
        # find the card name
        # find the card name with the closest value to what we read (Reading text from images has error margin)
        # if we have found this name berfore, return stored value (if the data is incorrect we can manually change the file)
        # add the highest return card to the player hand
        self.game_data.clear_card_area(CardAreas.PlayerHand)
        for i in range(0, MAX_CARDS_IN_HAND, 1):
            await self.cursor_core.set_cursor_position(i, delay=CURSOR_DELAY)
            screenshot = self.screen_grab.take_screenshot_and_crop(box=COORD_CROP_CARDS_US)
            screenshot_text = self.text_controller.image_to_text_pillow(pil_image=screenshot)
            highest_scored_card = self.game_data.find_card_with_closest_name(screenshot_text)
            self.game_data.add_card_to_area(CardAreas.PlayerHand, highest_scored_card)

        await self.state_machine.trigger_state_machine(end_program=False)

    async def FIND_BEST_CARD_TO_PLAY(self):
        currentAIMonsters = self.game_data.return_cards_from_area(CardAreas.AIMonsters)
        currentPlayerHand = self.game_data.return_cards_from_area(CardAreas.PlayerHand)
        currentPlayerMonsters = self.game_data.return_cards_from_area(CardAreas.PlayerMonsters)

        #has our oppoent got a monster on the field
        if len(currentAIMonsters) == 0:
            #do we have a open space on the field
            if len(currentPlayerMonsters) < MAX_CARDS_IN_FIELD:
                highest_card, highest_atk, card_type = self.game_data.return_highest_stat_for_areas(hand_area=currentPlayerHand, field_area=currentPlayerMonsters)
                if card_type == CardType.MONSTER:
                    await self.play_monster_from_hand(highest_card, CardPositions.ATK, PlayStyle.FACE_UP, len(currentPlayerMonsters))
                    await self.state_machine.trigger_state_machine(end_program=False)
                    return
            else:
                print("Create logic for us having 0 spaces free on the field")
        else:
            print("Create logic for oppoent having a monster on the field")

    async def play_monster_from_hand(self, highest_card, card_position: CardPositions, play_style: PlayStyle, index_to_play):
        #if the play style is telling us not to play the card then return
        if play_style == PlayStyle.NO_PLAY: return
        print(f"Play the highest card from our hand... {highest_card}")

        #set the cursor to the card we want to play
        await self.cursor_core.set_cursor_position(self.game_data.index_card_from_area(CardAreas.PlayerHand, highest_card))
        self.input_core.click_button('z', hold_delay=0.5)

        #make sure the card is in the correct rotation
        if play_style is PlayStyle.FACE_UP:
            self.input_core.right_click_button()

        #set the cursor to the position of the zone we want to click
        self.input_core.click_button('z', hold_delay=1)
        await self.cursor_core.default_cursor()
        await self.cursor_core.set_cursor_position(index_to_play)
        self.input_core.click_button('z', hold_delay=1)

        #todo implement card sign
        self.input_core.click_button('z', hold_delay=1)

        #Switch the card between def and atk
        if card_position is CardPositions.DEF:
            self.input_core.click_button('q', hold_delay=1)

        #Remove the card from the players hand
        #Add the card to the players field
        self.game_data.remove_card_from_area(CardAreas.PlayerHand, highest_card)
        highest_card["POS"] = card_position.name
        self.game_data.add_card_to_area(CardAreas.PlayerMonsters, highest_card)

    async def GEN_AI_BOARD(self):
        print("Gen AI Board....")
        #If this is our first turn, player always takes first turn so AI doesnt have any creatures on field
        if self.first_turn:
            await self.state_machine.trigger_state_machine(end_program=False)
            return

        await self.cursor_core.default_cursor()
        self.input_core.up_click_button()
        for i in range(0, MAX_CARDS_IN_FIELD, 1):
            await self.cursor_core.set_cursor_position(i)
            screenshot_A = self.screen_grab.take_screenshot_and_crop(box=COORD_CROP_CARDS_TEST_EMPTY)
            screenshot_B = self.screen_grab.take_screenshot_and_crop(box=COORD_CROP_CARDS_TEST_CARD)
            if not self.screen_grab.does_image_contain_more_than(screenshot_A, ARRAY_COLORS_FOR_EMPTY_SPACE):
                print("Empty Space")
            elif not self.screen_grab.does_image_contain_more_than(screenshot_B, ARRAY_COLORS_FOR_EMPTY_SPACE):
                print("We have found a unknown card")
                self.game_data.add_card_to_area(CardAreas.AIMonsters, self.game_data.return_empty_card())
            else:
                print("We have found a known card")

        await self.cursor_core.default_cursor()
        self.input_core.down_click_button(delay=1)
        await self.state_machine.trigger_state_machine(end_program=False)

    async def COMBAT(self):
        print("Combat....")
        # If this is our first turn, player always takes first turn, cant attack on first turn
        if self.first_turn:
            await self.state_machine.trigger_state_machine(end_program=False)
            return

        #todo loop through all monsters on our field in def and see if we can change those monsters to atk
        #todo if we can change to attack, attack with toehr creatures, then change back to def -> just change all monsters to attack to begin with

        player_cards = self.game_data.return_cards_from_area_with_pos(CardAreas.PlayerMonsters, CardPositions.ATK)
        pc_cards = self.game_data.return_cards_from_area(CardAreas.AIMonsters)

        creatures_attacked = []
        if len(pc_cards) > 0:
            for pc_creature in sorted(pc_cards, key=lambda x: max(x.get('CardAtk', 0), x.get('CardDef', 0)), reverse=True):
                pc_highest_score = max(pc_creature.get('CardAtk', 0), pc_creature.get('CardDef', 0))
                for our_creature in sorted(player_cards, key=lambda x: x.get('CardAtk', 0), reverse=True):
                    if our_creature['CardAtk'] > pc_highest_score and our_creature['CardID'] not in creatures_attacked:
                        print(f"Our creature {our_creature['CardName']} attacks pc's creature {pc_creature['CardName']}")
                        index_of_our_creature = self.game_data.index_card_from_area(CardAreas.PlayerMonsters, our_creature)

                        #click on the monster we want to attack with
                        await self.cursor_core.default_cursor()
                        await self.cursor_core.set_cursor_position(index_of_our_creature, delay=CURSOR_DELAY)
                        self.input_core.click_button('z', hold_delay=1)

                        # click on the monster we want to attack
                        await self.cursor_core.default_cursor()
                        index_of_their_creature = MAX_CARDS_IN_FIELD - 1 - self.game_data.index_card_from_area(CardAreas.AIMonsters, pc_creature)
                        await self.cursor_core.set_cursor_position(index_of_their_creature, delay=CURSOR_DELAY)
                        self.input_core.click_button('z', hold_delay=5)

                        creatures_attacked.append(our_creature['CardID'])
                        self.game_data.remove_card_from_area(CardAreas.AIMonsters, pc_creature)
                        break
            pc_cards = self.game_data.return_cards_from_area(CardAreas.AIMonsters)

        if len(pc_cards) <= 0:
            for our_creature in sorted(player_cards, key=lambda x: x.get('CardAtk', 0), reverse=True):
                if our_creature['CardID'] not in creatures_attacked:
                    print(f"Our creature {our_creature['CardName']} attacks pc directly")
                    index_of_our_creature = self.game_data.index_card_from_area(CardAreas.PlayerMonsters, our_creature)

                    # click on the monster we want to attack with
                    await self.cursor_core.default_cursor()
                    await self.cursor_core.set_cursor_position(index_of_our_creature, delay=CURSOR_DELAY)
                    self.input_core.click_button('z', hold_delay=1)
                    self.input_core.click_button('z', hold_delay=5)

                    creatures_attacked.append(our_creature['CardID'])

        for our_creature in player_cards:
            if our_creature['CardID'] not in creatures_attacked:
                print(f"Our creature {our_creature['CardName']} hasn't attacked this turn!")
                #todo change monster to def if the player monster in atk has a atk thats greater than our attack

        await self.state_machine.trigger_state_machine(end_program=False)

    async def END_TURN(self):
        print("End Turn....")
        time.sleep(1)
        self.input_core.enter_click_button()
        if self.first_turn:
            self.first_turn = False
        time.sleep(20)
        await self.state_machine.trigger_state_machine(end_program=False)

    async def END_PROGRAM(self):
        print("End Program....")