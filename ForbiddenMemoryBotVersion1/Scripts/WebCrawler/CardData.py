from PythonCores.WebsiteController import WebsiteController
from PythonCores.JSONController import JSONController
from Scripts.Enums.FilePaths import FilePaths
from Scripts.Enums.WebsitePath import WebsitePaths
from Scripts.Enums.StoredCardKeys import StoredCardKeys


def find_guardian_stars_in_row(table_column):
    stars = []
    for c in table_column.contents:
        content = c.replace("\n", "")
        if len(content) > 0: stars.append(content)
    return stars


def gen_fusion_data_from_table_and_header(table):
    data = {}
    for tr_element in table.find_all('tr'):
        td_elements = tr_element.find_all('td')
        if len(td_elements) <= 0: continue
        for mat1 in td_elements[0].find_all('li'):
            for mat2 in td_elements[1].find_all('li'):
                mat_1_id = ''.join(str(mat1))[5:8]
                mat_2_id = ''.join(str(mat2))[5:8]
                if not mat_1_id in data: data[mat_1_id] = []
                data[mat_1_id].append(mat_2_id)
    return data


def gen_card_data():
    card_dict = {}
    stored_cards = []

    website_controller = WebsiteController()
    card_website = website_controller.return_webpage(WebsitePaths().CardData)
    table = card_website.find('table', class_="wikitable")
    table_rows = table.find_all('tr')

    for i in range(1, len(table_rows), 1):
        table_columns = table_rows[i].find_all('td')

        stored_card = {}
        stored_card[StoredCardKeys().CardID] = str(table_columns[0].contents[0].replace("\n", ""))
        stored_card[StoredCardKeys().CardURL] = f"{WebsitePaths().BaseWebsite}{str(table_columns[1].find('a')['href'])}"
        stored_card[StoredCardKeys().CardName] = str(table_columns[1].contents[0].contents[0].replace('\n', ''))
        stored_card[StoredCardKeys().CardType] = str(table_columns[2].contents[0].contents[0])
        stored_card[StoredCardKeys().Type] = str(table_columns[3].contents[0].contents[0]) if len(str(table_columns[3])) > 10 else ""
        stored_card[StoredCardKeys().GuardianStars] = find_guardian_stars_in_row(table_columns[4])
        stored_card[StoredCardKeys().CardLevel] = str(table_columns[5].contents[0]).replace("\n", "")
        stored_card[StoredCardKeys().CardAtk] = str(table_columns[6].contents[0]).replace("\n", "")
        stored_card[StoredCardKeys().CardDef] = str(table_columns[7].contents[0]).replace("\n", "")
        stored_card[StoredCardKeys().CardPassword] = str(table_columns[8].contents[0]).replace("\n", "")
        stored_card[StoredCardKeys().SCCost] = str(table_columns[9].contents[0]).replace("\n", "")
        stored_cards.append(stored_card)

    card_dict['Cards'] = stored_cards
    JSONController().dump_dict_to_json(card_dict, FilePaths().CardData, True)
    website_controller.chrome_driver.close()


def gen_fusion_data():
    fusion_dict = {}
    website_controller = WebsiteController()

    for fusion_data_url in WebsitePaths().return_all_fusion_websites():
        fusion_data_website = website_controller.return_webpage(fusion_data_url)
        headers = fusion_data_website.find_all('span', class_="mw-headline")
        for i in range(0, len(headers), 1):
            card_id = "".join(str(headers[i].contents)[2:5])
            fusion_dict[card_id] = gen_fusion_data_from_table_and_header(fusion_data_website.find_all('table', class_="wikitable")[i])

    JSONController().dump_dict_to_json(fusion_dict, FilePaths().FusionData, True)
    website_controller.chrome_driver.close()
