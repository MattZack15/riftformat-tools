import RiftScribeAPI
import random

api = RiftScribeAPI.RiftScribeClient()


# 'sets': ['OGN', 'OGS', 'SFD', 'UNL', 'VEN'], 
# 'factions': ['body', 'calm', 'chaos', 'colorless', 'fury', 'mind', 'order'], 
# 'rarities': ['common', 'epic', 'rare', 'showcase', 'uncommon'], 
# 'types': ['Battlefield', 'Gear', 'Legend', 'Rune', 'Spell', 'Unit']

def random_legend():
    return api.random_card(types='Legend')

def random_main_deck_card(factions):
    return api.random_card(factions=factions, exclude_types=["Battlefield", "Legend", "Rune"])

def random_battlefield():
    return api.random_card(types='Battlefield')

def add_card_to_deck(deck_list, card):
    deck_list += "1 "
    deck_list += card
    deck_list += "\n"
    return deck_list

def add_runes_to_deck(deck_list, factions):
    deck_list += "\nRunes:\n"
    rune_count_1 = random.randint(1, 11)
    rune_count_2 = 12 - rune_count_1
    deck_list += f"{rune_count_1} {factions[0]} Rune\n"
    deck_list += f"{rune_count_2} {factions[1]} Rune\n"
    return deck_list


deck_list = "Legend:\n"
legend = api.LEGEND_MAP[random_legend()['name']]
deck_list = add_card_to_deck(deck_list, legend['name'])
deck_list += "\nChampion:\n"
deck_list = add_card_to_deck(deck_list, api.random_chosen_champ_card(legend['name'], 'Legend')['name'])

deck_list += "\nMainDeck:\n"
factions = legend['domains']

print(factions)

for i in range(0, 39):
    deck_list = add_card_to_deck(deck_list, random_main_deck_card(factions)["name"])

deck_list += "\nBattlefields:\n"

for i in range(0, 3):
    deck_list = add_card_to_deck(deck_list, random_battlefield()["name"])

deck_list = add_runes_to_deck(deck_list, factions)

print(deck_list)