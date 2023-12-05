import sys
import dataclasses
from typing import List, Mapping
import sys
from functools import cached_property

@dataclasses.dataclass
class Card:
    game : str
    winning : List[int]
    hand : List[int]

    @property
    def index(self):
        return int(self.game[4:])

    @cached_property
    def wins(self):
        return len(set(self.winning).intersection(set(self.hand)))

    @property
    def score(self):
        count = self.wins
        return 2 ** (count - 1) if count > 0 else 0

def parse_card(line:str):
    pgame = line.find(':')
    pwinning = line.find('|', pgame)
    
    return Card(line[:pgame], [int(x) for x in line[pgame+1:pwinning].split()], [int(x) for x in line[pwinning+1:].split()])

cards = []
with open('Problem 4/input.txt', 'r') as f:
    for line in f.readlines():
        card = parse_card(line)
        #print(f'Parsed card: {card} -> {card.score}')
        cards.append(card)


if len(sys.argv) <= 1 or sys.argv[1] == 'part1':
    total = sum(c.score for c in cards)
    print(f'Total = {total}')
else:
    pending : List[Card] = cards[:]
    counts : Mapping[str, int] = dict((c.game, 1) for c in cards)
    i = 0
    for c in cards:
        for copy in cards[c.index : c.index + c.wins]:
            counts[copy.game] += counts[c.game]

    total = sum(counts.values())
    print(f'Total = {total}')