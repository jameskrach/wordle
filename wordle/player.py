# -*- coding: utf-8 -*-
import re
import random
from abc import ABC, abstractmethod
from concurrent.futures import Executor
from pathlib import Path
from string import ascii_lowercase

from .constants import MAX_GUESS, WORD_SIZE, WORD_FILE, LetterInfo, Response
from .game import TurnOutcome


class PlayerInterface(ABC):
    """Bare minimum API that players must implement in order to play."""
    def __init__(self, word_size: int = WORD_SIZE, max_guess: int = MAX_GUESS, word_file: Path = WORD_FILE) -> None:
        self.guesses: list[str] = []
        self.responses: list[Response] = []
        self.word_size = word_size
        self.max_guess = max_guess
        self.turns_remaining = max_guess

        with open(word_file) as f:
            self.all_words = f.read().splitlines()

    def receive_response(self, turn_outcome: TurnOutcome) -> None:
        self.guesses.append(turn_outcome.guess)
        self.responses.append(turn_outcome.response)
        self.turns_remaining = turn_outcome.turns_remaining

    @abstractmethod
    def guess(self) -> str:
        ...


class BasePlayer(PlayerInterface):
    """ABC with a few methods that are likely useful to all player implementations."""
    def __init__(self, word_size: int = WORD_SIZE, max_guess: int = MAX_GUESS, word_file: Path = WORD_FILE) -> None:
        super().__init__(word_size=word_size, max_guess=max_guess, word_file=word_file)
        self._cache_guesses: list[str] = []
        self._cache_remaining_words: list[str] = self.all_words.copy()

    @property
    def bad_letters(self) -> str:
        """Letters that have been excluded by previous responses."""
        bad_letters = set()

        for guess, response in zip(self.guesses, self.responses):
            for letter, letter_info in zip(guess, response):
                if letter_info == LetterInfo.NOT_IN_WORD:
                    bad_letters.add(letter)

        return "".join(bad_letters)

    @property
    def remaining_letters(self) -> str:
        """Letters that have not been excluded by previous responses."""
        return "".join(i for i in ascii_lowercase if i not in self.bad_letters)

    @property
    def implied_regex(self) -> re.Pattern:
        """A compiled regex that matches words that conform to previous responses."""
        in_pos = {}
        for guess, response in zip(self.guesses, self.responses):
            for idx, letter_and_info in enumerate(zip(guess, response)):
                if letter_and_info[1] == LetterInfo.IN_POSITION:
                    in_pos[idx] = letter_and_info[0]

        if not self.bad_letters:
            pattern = ".*"
        else:
            pattern = "".join(in_pos.get(i, f"[^{self.bad_letters}]") for i in range(self.word_size))
        return re.compile(pattern)

    @property
    def remaining_words(self) -> list[str]:
        """The remaining words that conform to previous responses."""
        if self.guesses != self._cache_guesses:
            self._cache_guesses = self.guesses.copy()
            self._cache_remaining_words = list(filter(self.implied_regex.fullmatch, self._cache_remaining_words))

        return self._cache_remaining_words

    @property
    def letter_frequencies(self) -> dict[str, int]:
        """The frequency of letters in the remaining words that confrm to previous responses."""
        return {i: sum(1 for j in self.remaining_words if i in j) for i in self.remaining_letters}

    @abstractmethod
    def guess(self) -> str:
        ...


class PlayerRandom(BasePlayer):
    """A first attempt at a player with a guessing strategy."""
    def __init__(self, word_size: int = WORD_SIZE, max_guess: int = MAX_GUESS, word_file: Path = WORD_FILE) -> None:
        super().__init__(word_size=word_size, max_guess=max_guess, word_file=word_file)

    def guess(self) -> str:
        return random.choice(self.remaining_words)
