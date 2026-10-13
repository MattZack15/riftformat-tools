# Riftformat Tools

A small Python tool that generates a random, correctly formatted **Riftbound** decklist: pick a random Legend, add its Chosen Champion, fill the main deck from the Legend's two domains, add three Battlefields, and split 12 Runes between the domains.

It is a deck-*building* helper only. It does not simulate or replicate Riftbound gameplay.

## Sample output (text mock-up)

```
Legend:
1 Master Yi, Wuju Bladesman

Champion:
1 Master Yi, Tempered

MainDeck:
3 Charm
3 Defy
3 Discipline
2 En Garde
...

Battlefields:
1 The Arena's Greatest
1 Emperor's Dais
1 Seat of Power

Runes:
7 Body Rune
5 Calm Rune
```

## How it works

1. `RiftScribeAPI.py` downloads the card list once and caches it in memory.
2. `main.py` picks a random Legend and looks up its domains.
3. It picks the Chosen Champion, 39 main-deck cards in the Legend's domains (no Battlefields, Legends or Runes), 3 Battlefields, and a random 12-rune split.
4. The decklist is printed as plain text.

## Riot API usage

> **Edit this section before submitting.** Say, in two or three sentences, which Riot API endpoints or data you will use, why, and what the product does with them. Example: "Card names, text and types are read from the Riot API and displayed unmodified."

Current prototype data source: the community RiftScribe card API (`riftscribe.gg`).

## Run it

```bash
pip install -r requirements.txt
python main.py
```

## Legal

Riftformat Tools isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
