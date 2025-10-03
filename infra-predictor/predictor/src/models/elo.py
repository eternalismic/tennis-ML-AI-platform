from dataclasses import dataclass, field
from typing import Dict, Tuple

@dataclass
class EloModel:
    k: float = 32.0
    base: float = 1500.0
    ratings: Dict[Tuple[str,str], float] = field(default_factory=dict)  # (player, surface)->rating

    def _key(self, player: str, surface: str|None) -> Tuple[str,str]:
        return (player, surface or "overall")

    def get(self, player: str, surface: str|None=None) -> float:
        return self.ratings.get(self._key(player, surface), self.base)

    def expected(self, a: str, b: str, surface: str|None=None) -> float:
        ra = self.get(a, surface); rb = self.get(b, surface)
        return 1.0 / (1.0 + 10 ** ((rb - ra) / 400))

    def update(self, winner: str, loser: str, surface: str|None=None, margin: float|None=None):
        exp = self.expected(winner, loser, surface)
        k_eff = self.k * (1.0 + 0.1*(margin or 0.0))
        wkey = self._key(winner, surface); lkey = self._key(loser, surface)
        self.ratings[wkey] = self.get(winner, surface) + k_eff * (1 - exp)
        self.ratings[lkey] = self.get(loser, surface)  - k_eff * (1 - exp)

    def prob_win(self, a: str, b: str, surface: str|None=None) -> float:
        return self.expected(a, b, surface)
