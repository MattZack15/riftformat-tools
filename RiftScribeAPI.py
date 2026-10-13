from __future__ import annotations

import random
from typing import Any

import requests


class RiftScribeClient:
    BASE_URL = "https://riftscribe.gg/api"

    def __init__(self):
        self.session = requests.Session()

        # Download every card once
        self._cards = self.load_all_cards()
        print(f"Loaded {len(self._cards)} cards.")

    def _get(self, endpoint: str, **params) -> Any:
        params = {k: v for k, v in params.items() if v is not None}

        response = self.session.get(
            f"{self.BASE_URL}/{endpoint}",
            params=params,
            timeout=10,
        )
        #print(response.status_code)
        #print(response.text)

        response.raise_for_status()
        return response.json()

    def load_all_cards(self):
        cards = []
        offset = 0
        limit = 200

        while True:
            batch = self._get("cards", limit=limit, offset=offset)

            if not batch:
                break

            cards.extend(batch)

            # Last page
            if len(batch) < limit:
                break

            offset += limit

        return cards

    @property
    def cards(self) -> list[dict]:
        """Returns the cached list of all cards."""
        return self._cards

    def random_card(
        self,
        *,
        sets: str | list[str] | None = None,
        factions: str | list[str] | None = None,
        rarities: str | list[str] | None = None,
        types: str | list[str] | None = None,
        exclude_types: str | list[str] | None = None,
    ) -> dict:
        """
        Returns a random card matching the supplied filters.

        All filters are optional.

        Lists are OR'd together.

        Example:
            factions=["fury", "order"]
            types=["Unit", "Spell"]

        means:
            (fury OR order)
            AND
            (Unit OR Spell)
        """

        cards = self._cards

        def make_set(value):
            if value is None:
                return None
            if isinstance(value, str):
                return {value}
            return set(value)

        sets = make_set(sets)
        factions = make_set(factions)
        rarities = make_set(rarities)
        types = make_set(types)
        exclude_types = make_set(exclude_types)

        if sets:
            cards = [c for c in cards if c.get("set_id") in sets]

        if factions:
            cards = [c for c in cards if c.get("faction") in factions]

        if rarities:
            cards = [c for c in cards if c.get("rarity") in rarities]

        if types:
            cards = [c for c in cards if c.get("type") in types]

        if exclude_types:
            cards = [c for c in cards if c.get("type") not in exclude_types]

        if not cards:
            raise ValueError("No cards matched the supplied filters.")

        return random.choice(cards)

    def search(self, query: str):
        return [
            card
            for card in self._cards
            if query.lower() in card.get("name", "").lower()
        ]

    def card(self, card_id: str):
        for card in self._cards:
            if card["card_id"] == card_id:
                return card
        return None

    def filters(self):
        return self._get("cards/filters")
    
    def random_chosen_champ_card(
        self,
        legend_name: str,
        exclude_types: str | list[str] | None = None,
    ):
        """
        Example:
            'Draven, Glorious Executioner'
                -> searches for 'Draven'

            'Master Yi, Wuju Master'
                -> searches for 'Master Yi'
        """

        champion = legend_name.split(",")[0].strip()

        if isinstance(exclude_types, str):
            exclude_types = {exclude_types}
        elif exclude_types:
            exclude_types = set(exclude_types)
        else:
            exclude_types = set()

        cards = [
            card
            for card in self._cards
            if champion.lower() in card["name"].lower()
            and card["type"] not in exclude_types
        ]

        if not cards:
            raise ValueError(f"No cards found for {champion}")

        return random.choice(cards)
    

    LEGEND_MAP = {
    "Daughter of the Void": {
        "name": "Kai'Sa, Daughter of the Void",
        "domains": ["fury", "chaos"],
    },
    "Relentless Storm": {
        "name": "Volibear, Relentless Storm",
        "domains": ["body", "fury"],
    },
    "Loose Cannon": {
        "name": "Jinx, Loose Cannon",
        "domains": ["chaos", "fury"],
    },
    "Hand of Noxus": {
        "name": "Darius, Hand of Noxus",
        "domains": ["order", "fury"],
    },
    "Nine-Tailed Fox": {
        "name": "Ahri, Nine-Tailed Fox",
        "domains": ["calm", "mind"],
    },
    "Blind Monk": {
        "name": "Lee Sin, Blind Monk",
        "domains": ["body", "calm"],
    },
    "Unforgiven": {
        "name": "Yasuo, Unforgiven",
        "domains": ["calm", "chaos"],
    },
    "Radiant Dawn": {
        "name": "Leona, Radiant Dawn",
        "domains": ["calm", "order"],
    },
    "Swift Scout": {
        "name": "Teemo, Swift Scout",
        "domains": ["mind", "chaos"],
    },
    "Herald of the Arcane": {
        "name": "Ryze, Herald of the Arcane",
        "domains": ["mind", "order"],
    },
    "Bounty Hunter": {
        "name": "Miss Fortune, Bounty Hunter",
        "domains": ["chaos", "order"],
    },
    "The Boss": {
        "name": "Sett, The Boss",
        "domains": ["body", "order"],
    },
    "Dark Child - Starter": {
        "name": "Annie, Dark Child",
        "domains": ["chaos", "fury"],
    },
    "Wuju Bladesman - Starter": {
        "name": "Master Yi, Wuju Bladesman",
        "domains": ["body", "calm"],
    },
    "Lady of Luminosity - Starter": {
        "name": "Lux, Lady of Luminosity",
        "domains": ["mind", "order"],
    },
    "Might of Demacia - Starter": {
        "name": "Garen, Might of Demacia",
        "domains": ["body", "order"],
    },
    "Mechanized Menace": {
        "name": "Rumble, Mechanized Menace",
        "domains": ["fury", "mind"],
    },
    "Purifier": {
        "name": "Lucian, Purifier",
        "domains": ["body", "fury"],
    },
    "Glorious Executioner": {
        "name": "Draven, Glorious Executioner",
        "domains": ["chaos", "fury"],
    },
    "Void Burrower": {
        "name": "Rek'Sai, Void Burrower",
        "domains": ["order", "fury"],
    },
    "Fire Below the Mountain": {
        "name": "Ornn, Fire Below the Mountain",
        "domains": ["mind", "calm"],
    },
    "Grandmaster at Arms": {
        "name": "Jax, Grandmaster at Arms",
        "domains": ["body", "calm"],
    },
    "Blade Dancer": {
        "name": "Irelia, Blade Dancer",
        "domains": ["calm", "chaos"],
    },
    "Emperor of the Sands": {
        "name": "Azir, Emperor of the Sands",
        "domains": ["calm", "order"],
    },
    "Prodigal Explorer": {
        "name": "Ezreal, Prodigal Explorer",
        "domains": ["chaos", "mind"],
    },
    "Chem-Baroness": {
        "name": "Renata Glasc, Chem-Baroness",
        "domains": ["mind", "order"],
    },
    "Battle Mistress": {
        "name": "Sivir, Battle Mistress",
        "domains": ["body", "chaos"],
    },
    "Grand Duelist": {
        "name": "Fiora, Grand Duelist",
        "domains": ["body", "order"],
    },
    "Virtuoso": {
        "name": "Jhin, Virtuoso",
        "domains": ["fury", "mind"],
    },
    "Pridestalker": {
        "name": "Rengar, Pridestalker",
        "domains": ["body", "fury"],
    },
    "Bloodharbor Ripper": {
        "name": "Pyke, Bloodharbor Ripper",
        "domains": ["chaos", "fury"],
    },
    "Piltover Enforcer": {
        "name": "Vi, Piltover Enforcer",
        "domains": ["order", "fury"],
    },
    "Bashful Bloom": {
        "name": "Lillia, Bashful Bloom",
        "domains": ["calm", "mind"],
    },
    "Wuju Master": {
        "name": "Master Yi, Wuju Master",
        "domains": ["body", "calm"],
    },
    "Gloomist": {
        "name": "Vex, Gloomist",
        "domains": ["chaos", "calm"],
    },
    "Green Father": {
        "name": "Ivern, Green Father",
        "domains": ["calm", "order"],
    },
    "Scorn of the Moon": {
        "name": "Diana, Scorn of the Moon",
        "domains": ["chaos", "mind"],
    },
    "Deceiver": {
        "name": "LeBlanc, Deceiver",
        "domains": ["order", "mind"],
    },
    "Voidreaver": {
        "name": "Kha'Zix, Voidreaver",
        "domains": ["body", "chaos"],
    },
    "Keeper of the Hammer": {
        "name": "Poppy, Keeper of the Hammer",
        "domains": ["body", "order"],
    },
}