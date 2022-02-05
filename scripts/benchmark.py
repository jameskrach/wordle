#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
from dataclasses import dataclass
from functools import cached_property, partial
from multiprocessing import cpu_count
from typing import Iterator, Type

from tabulate import tabulate
from tqdm.contrib.concurrent import process_map

from wordle.constants import GameStatus, MAX_GUESS
from wordle.game import Game, WORD_FILE
from wordle.player import PlayerInterface, PlayerRandom


@dataclass(frozen=True, repr=False, unsafe_hash=True)
class BenchmarkResult:
    outcomes: Iterator[int]
    max_guess: int = MAX_GUESS

    @cached_property
    def outcome_freq(self) -> Counter[int, int]:
        c = Counter(self.outcomes)

        # needs to come after potentially exhausting self.outcome
        if not set(c).issubset(set(range(self.max_guess + 1))):
            raise ValueError("outcomes only contain elements in {0, 1, ..., max_guess}")

        return c

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


def word_benchmark(player: PlayerInterface, game: Game, word: str) -> int:
    player.reset()
    game.reset(secret_word=word)

    game_status = GameStatus.IN_PROGRESS

    while game_status == GameStatus.IN_PROGRESS:
        guess = player.guess()
        turn_outcome = game.handle_guess(guess)
        player.receive_response(turn_outcome)
        game_status = turn_outcome.game_status

    if game_status == GameStatus.LOST:
        outcome = 0
    else:
        outcome = MAX_GUESS - turn_outcome.turns_remaining

    return outcome


def player_benchmark(player: Type[PlayerInterface]) -> BenchmarkResult:
    with open(WORD_FILE) as f:
        words = f.read().splitlines()
    p = player()
    g = Game()
    fn = partial(word_benchmark, p, g)
    outcomes = process_map(fn, words, max_workers=cpu_count() - 1, desc=player.__name__, ncols=88, chunksize=100)
    return BenchmarkResult(outcomes)


def main():
    players: list[Type[PlayerInterface]] = [PlayerRandom, ]
    benchmark_results = {impl.__name__: player_benchmark(impl) for impl in players}
    headers = ("Strategy", "Win Rate", "Turns/Win")
    table = sorted(
        ((k, v.win_rate, v.turns_per_win) for k, v in benchmark_results.items()),
        key=lambda x: x[1],
        reverse=True
    )
    print("\n" + tabulate(table, headers, tablefmt="psql") + "\n")


if __name__ == "__main__":
    main()
