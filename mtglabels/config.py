API_ENDPOINT = "https://api.scryfall.com"

# Set types we are interested in
SET_TYPES = (
    "core",
    "expansion",
    "starter",  # Portal, P3k, welcome decks
    "masters",
    "commander",
    "planechase",
    "draft_innovation",  # Battlebond, Conspiracy
    "duel_deck",  # Duel Deck Elves,
    "premium_deck",  # Premium Deck Series: Slivers, Premium Deck Series: Graveborn
    "from_the_vault",  # Make sure to adjust the MINIMUM_SET_SIZE if you want these
    "archenemy",
    "box",
    "funny",  # Unglued, Unhinged, Ponies: TG, etc.
    # "memorabilia",  # Commander's Arsenal, Celebration Cards, World Champ Decks
    # "spellbook",
    # These are relatively large groups of sets
    # You almost certainly don't want these
    # "token",
    # "promo",
)

# Only include sets at least this size
# For reference, the smallest proper expansion is Arabian Nights with 78 cards
MINIMUM_SET_SIZE = 50

# Set codes you might want to ignore
IGNORED_SETS = (
    "cmb1",  # Mystery Booster Playtest Cards
    "amh1",  # Modern Horizon Art Series
    "cmb2",  # Mystery Booster Playtest Cards Part Deux
    "fbb",  # Foreign Black Border
    "sum",  # Summer Magic / Edgar
    "4bb",  # Fourth Edition Foreign Black Border
    "bchr",  # Chronicles Foreign Black Border
    "rin",  # Rinascimento
    "ren",  # Renaissance
    "rqs",  # Rivals Quick Start Set
    "itp",  # Introductory Two-Player Set
    "sir",  # Shadows over Innistrad Remastered
    "sis",  # Shadows of the Past
    "cst",  # Coldsnap Theme Decks
)

# Used to rename very long set names
RENAME_SETS = {
    "Adventures in the Forgotten Realms Minigames": "Forgotten Realms Minigames",
    "Adventures in the Forgotten Realms": "Forgotten Realms",
    "Angels: They're Just Like Us but Cooler and with Wings": "Angels: They're Just Like Us",
    "Archenemy: Nicol Bolas Schemes": "Archenemy: Bolas Schemes",
    "Commander Anthology Volume II": "Commander Anthology II",
    "Commander Legends: Battle for Baldur's Gate": "CMDR Legends: Baldur's Gate",
    "Crimson Vow Commander": "CMDR Crimson Vow",
    "Dominaria United Commander": "CMDR Dominaria United",
    "Duel Decks Anthology: Divine vs. Demonic": "DDA: Divine vs. Demonic",
    "Duel Decks Anthology: Elves vs. Goblins": "DDA: Elves vs. Goblins",
    "Duel Decks Anthology: Garruk vs. Liliana": "DDA: Garruk vs. Liliana",
    "Duel Decks Anthology: Jace vs. Chandra": "DDA: Jace vs. Chandra",
    "Duel Decks: Ajani vs. Nicol Bolas": "DD: Ajani vs. Nicol Bolas",
    "Duel Decks: Blessed vs. Cursed": "DD: Blessed vs. Cursed",
    "Duel Decks: Divine vs. Demonic": "DD: Divine vs. Demonic",
    "Duel Decks: Elspeth vs. Kiora": "DD: Elspeth vs. Kiora",
    "Duel Decks: Elspeth vs. Tezzeret": "DD: Elspeth vs. Tezzeret",
    "Duel Decks: Elves vs. Goblins": "DD: Elves vs. Goblins",
    "Duel Decks: Elves vs. Inventors": "DD: Elves vs. Inventors",
    "Duel Decks: Garruk vs. Liliana": "DD: Garruk vs. Liliana",
    "Duel Decks: Heroes vs. Monsters": "DD: Heroes vs. Monsters",
    "Duel Decks: Jace vs. Chandra": "DD: Jace vs. Chandra",
    "Duel Decks: Knights vs. Dragons": "DD: Knights vs. Dragons",
    "Duel Decks: Merfolk vs. Goblins": "DD: Merfolk vs. Goblins",
    "Duel Decks: Nissa vs. Ob Nixilis": "DD: Nissa vs. Ob Nixilis",
    "Duel Decks: Phyrexia vs. the Coalition": "DD: Phyrexia vs. Coalition",
    "Duel Decks: Speed vs. Cunning": "DD: Speed vs. Cunning",
    "Duel Decks: Zendikar vs. Eldrazi": "DD: Zendikar vs. Eldrazi",
    "Forgotten Realms Commander": "CMDR Forgotten Realms",
    "Fourth Edition Foreign Black Border": "Fourth Edition FBB",
    "Global Series Jiang Yanggu & Mu Yanling": "Jiang Yanggu & Mu Yanling",
    "Innistrad: Crimson Vow Minigames": "Crimson Vow Minigames",
    "Introductory Two-Player Set": "Intro Two-Player Set",
    "Kaldheim Commander": "CMDR Kaldheim",
    "March of the Machine Commander": "CMDR March of the Machine",
    "March of the Machine: The Aftermath": "March of the Machine: Aftermath",
    "Midnight Hunt Commander": "CMDR Midnight Hunt",
    "Mystery Booster Playtest Cards 2019": "MB Playtest Cards 2019",
    "Mystery Booster Playtest Cards 2021": "MB Playtest Cards 2021",
    "Mystery Booster Playtest Cards": "Mystery Booster Playtest",
    "Mystery Booster Retail Edition Foils": "Mystery Booster Retail Foils",
    "Neon Dynasty Commander": "CMDR Neon Dynasty",
    "New Capenna Commander": "CMDR New Capenna",
    "Phyrexia: All Will Be One Commander": "CMDR Phyrexia: One",
    "Planechase Anthology Planes": "Planechase Anth. Planes",
    "Premium Deck Series: Fire and Lightning": "PD: Fire & Lightning",
    "Premium Deck Series: Graveborn": "Premium Deck Graveborn",
    "Premium Deck Series: Slivers": "Premium Deck Slivers",
    "Starter Commander Decks": "CMDR Starter Decks",
    "Strixhaven: School of Mages Minigames": "Strixhaven Minigames",
    "Tales of Middle-earth Commander": "CMDR The Lord of the Rings",
    "The Brothers' War Commander": "CMDR The Brothers' War",
    "The Brothers' War Retro Artifacts": "The Brothers' War Retro",
    "The Lord of the Rings: Tales of Middle-earth": "The Lord of the Rings",
    "The Lost Caverns of Ixalan Commander": "CMDR Lost Caverns of Ixalan",
    "Warhammer 40,000 Commander": "CMDR Warhammer 40K",
    "Wilds of Eldraine Commander": "CMDR Wilds of Eldraine",
    "World Championship Decks 1997": "World Championship 1997",
    "World Championship Decks 1998": "World Championship 1998",
    "World Championship Decks 1999": "World Championship 1999",
    "World Championship Decks 2000": "World Championship 2000",
    "World Championship Decks 2001": "World Championship 2001",
    "World Championship Decks 2002": "World Championship 2002",
    "World Championship Decks 2003": "World Championship 2003",
    "World Championship Decks 2004": "World Championship 2004",
    "Zendikar Rising Commander": "CMDR Zendikar Rising",
}

"""
Proxy/real (box)
Color
Type
Mana cost
Alphabetical
"""

"""
Optional fields:
- 'font-size'
- 'font-weight'
- 'fill'
"""
COLOR_SYMBOLS = [
    {"title": {"text": "White"}, "symbol": "{W}"},
    {"title": {"text": "Blue"}, "symbol": "{U}"},
    {"title": {"text": "Black"}, "symbol": "{B}"},
    {"title": {"text": "Red"}, "symbol": "{R}"},
    {"title": {"text": "Green"}, "symbol": "{G}"},
    {"title": {"text": "Colorless"}, "symbol": "{C}"},
    {"title": {"text": "Azorius"}, "symbol": "{W}{U}"},
    {"title": {"text": "Boros"}, "symbol": "{W}{R}"},
    {"title": {"text": "Dimir"}, "symbol": "{U}{B}"},
    {"title": {"text": "Golgari"}, "symbol": "{B}{G}"},
    {"title": {"text": "Gruul"}, "symbol": "{R}{G}"},
    {"title": {"text": "Izzet"}, "symbol": "{U}{R}"},
    {"title": {"text": "Orzhov"}, "symbol": "{W}{B}"},
    {"title": {"text": "Rakdos"}, "symbol": "{B}{R}"},
    {"title": {"text": "Selesnya"}, "symbol": "{W}{G}"},
    {"title": {"text": "Simic"}, "symbol": "{U}{G}"},
    {"title": {"text": "Abzan"}, "symbol": "{W}{B}{G}"},
    {"title": {"text": "Bant"}, "symbol": "{W}{U}{G}"},
    {"title": {"text": "Esper"}, "symbol": "{W}{U}{B}"},
    {"title": {"text": "Grixis"}, "symbol": "{U}{B}{R}"},
    {"title": {"text": "Jeskai"}, "symbol": "{W}{U}{R}"},
    {"title": {"text": "Jund"}, "symbol": "{B}{R}{G}"},
    {"title": {"text": "Mardu"}, "symbol": "{W}{B}{R}"},
    {"title": {"text": "Naya"}, "symbol": "{W}{R}{G}"},
    {"title": {"text": "Sultai"}, "symbol": "{U}{B}{G}"},
    {"title": {"text": "Temur"}, "symbol": "{U}{R}{G}"},
    {"title": {"text": "Dune"}, "symbol": "{W}{B}{R}{G}"},
    {"title": {"text": "Glint"}, "symbol": "{U}{B}{R}{G}"},
    {"title": {"text": "Ink"}, "symbol": "{W}{U}{R}{G}"},
    {"title": {"text": "Witch"}, "symbol": "{W}{U}{B}{G}"},
    {"title": {"text": "Yore"}, "symbol": "{W}{U}{B}{R}"}
]


TYPE_SYMBOLS = [
    {"title": {"text": "Artifact"}, "icon": "artifact.png"},
    {"title": {"text": "Creature"}, "icon": "creature.png"},
    {"title": {"text": "Enchantment"}, "icon": "enchantment.png"},
    {"title": {"text": "Instant/Sorcery"}, "icon": "instant_sorcery.png"},
    {"title": {"text": "Planeswalker"}, "symbol": "{PW}"},
    {"title": {"text": "Misc"}, "icon": "misc.png"}
]

COST_SYMBOLS = [
    {
        "title": {
            "text": "Cost: 0-3",
        },
        "symbol": "{0}{1}{2}{3}"
    },
    {
        "title": {
            "text": "Cost: 4-6"
        },
        "symbol": "{4}{5}{6}"
    },
    {
        "title": {
            "text": "Cost: 7+ / X",
        },
        "symbol": "{7}{X}"
    }
]

alpha_offset_x = 80
alpha_offset_y = -10

ALPHABETICAL_SYMBOLS = [
    {"title": {"font-size": "70px", "text": "A-D", "x_offset": alpha_offset_x * 0, "y_offset": alpha_offset_y}},
    {"title": {"font-size": "70px", "text": "E-H", "x_offset": alpha_offset_x * 1, "y_offset": alpha_offset_y}},
    {"title": {"font-size": "70px", "text": "I-L", "x_offset": alpha_offset_x * 2, "y_offset": alpha_offset_y}},
    {"title": {"font-size": "70px", "text": "M-Q", "x_offset": alpha_offset_x * 3, "y_offset": alpha_offset_y}},
    {"title": {"font-size": "70px", "text": "R-T", "x_offset": alpha_offset_x * 4, "y_offset": alpha_offset_y}},
    {"title": {"font-size": "70px", "text": "U-Z", "x_offset": alpha_offset_x * 5, "y_offset": alpha_offset_y}}
]

# Backup of ~2k even splits.
# ALPHABETICAL_SYMBOLS = [
#     {"name": "A"},
#     {"name": "B"},
#     {"name": "C"},
#     {"name": "D"},
#     {"name": "E-F"},
#     {"name": "G-H"},
#     {"name": "I-L"},
#     {"name": "M-N"},
#     {"name": "O-Q"},
#     {"name": "R"},
#     {"name": "Sa-Sm"},
#     {"name": "Sn-Sz"},
#     {"name": "T"},
#     {"name": "U-Z"}
# ]

TYPE_COST_ALPHA_SYMBOLS = TYPE_SYMBOLS + COST_SYMBOLS + ALPHABETICAL_SYMBOLS

ALL_SYMBOLS = COLOR_SYMBOLS + TYPE_SYMBOLS + COST_SYMBOLS + ALPHABETICAL_SYMBOLS

"""
Card quantity starting with given letter.
As of 07/2024.

Letter	Quantity
a	2046
b	1835
c	2224
d	1787
e	1149
f	1350
g	1735
h	1133
i	856
j	379
k	872
l	983
m	1875
n	736
o	678
p	1444
q	117
r	1728
s	4207
t	2144
u	428
v	848
w	1091
x	35
y	138
z	188
"""

LETTER_WIDTH = 2160  # Letter paper width in mm
LETTER_HEIGHT = 2790  # Letter paper height in mm
