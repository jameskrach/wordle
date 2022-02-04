#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from pprint import pprint
from typing import Type

from wordle.constants import GameStatus, MAX_GUESS
from wordle.game import Game, WORD_FILE
from wordle.player import PlayerInterface, PlayerRandom


# Players to benchmark
player_implementations: list[Type[PlayerInterface]] = [PlayerRandom, ]


@dataclass
class BenchmarkResult:
    max_guess: int = MAX_GUESS

    def __post_init__(self) -> None:
        self.outcome_freq: dict[int, int] = dict(zip(range(self.max_guess + 1), [0] * (self.max_guess + 1)))

    def add_outcome(self, num_turns: int) -> None:
        if num_turns not in self.outcome_freq:
            raise ValueError("num_turns must be in {0, 1, ..., Maximum Number of Turns}")

        self.outcome_freq[num_turns] += 1

    @property
    def win_rate(self) -> float:
        tot = sum(self.outcome_freq.values())
        return (tot - self.outcome_freq[0]) / tot

    @property
    def turns_per_win(self) -> float | None:
        wins = {k: v for k, v in self.outcome_freq.items() if k}
        tot = sum(v for k, v in self.outcome_freq.items() if k)
        try:
            tpr = sum((k * v for k, v in wins.items())) / tot
        except ZeroDivisionError:
            tpr = None

        return tpr

    @property
    def summary(self) -> dict[str, float]:
        return {
            "win_rate": self.win_rate,
            "turns_per_win": self.turns_per_win,
        }


def run_benchmark(player: Type[PlayerInterface]) -> BenchmarkResult:
    with open(WORD_FILE) as f:
        all_words = f.read().splitlines()

    b = BenchmarkResult()

    for word in all_words:
        p = player()
        g = Game(secret_word=word)

        game_status = GameStatus.IN_PROGRESS

        while game_status == GameStatus.IN_PROGRESS:
            guess = p.guess()
            turn_outcome = g.handle_guess(guess)
            p.receive_response(turn_outcome)
            game_status = turn_outcome.game_status

        if game_status == GameStatus.LOST:
            b.add_outcome(0)
        else:
            b.add_outcome(MAX_GUESS - turn_outcome.turns_remaining)

    return b


def main():
    pprint({impl.__name__: run_benchmark(impl).summary for impl in player_implementations})


if __name__ == "__main__":
    main()