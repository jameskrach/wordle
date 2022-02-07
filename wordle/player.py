# -*- coding: utf-8 -*-
import re
import random
from abc import ABC, abstractmethod
from string import ascii_lowercase

from .constants import ALL_WORDS, MAX_GUESS, WORD_SIZE, LetterInfo, Response
from .game import TurnOutcome


class PlayerInterface(ABC):
    """Bare minimum API that players must implement in order to play."""
    def __init__(self, word_size: int = WORD_SIZE, max_guess: int = MAX_GUESS) -> None:
        self.guesses: list[str] = []
        self.responses: list[Response] = []
        self.word_size = word_size
        self.max_guess = max_guess
        self.turns_remaining = self.max_guess

    def receive_response(self, turn_outcome: TurnOutcome) -> None:
        self.guesses.append(turn_outcome.guess)
        self.responses.append(turn_outcome.response)
        self.turns_remaining = turn_outcome.turns_remaining

    @abstractmethod
    def guess(self) -> str:
        """Use the player's strategy to guess the Wordle."""
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the player for a new game."""
        ...


class BasePlayer(PlayerInterface):
    """ABC with a few methods that are likely useful to all player implementations."""
    def __init__(self, word_size: int = WORD_SIZE, max_guess: int = MAX_GUESS) -> None:
        super().__init__(word_size=word_size, max_guess=max_guess)
        self._cache_guesses: list[str] = []
        self._cache_remaining_words: list[str] = ALL_WORDS.copy()

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
        position_parts = {i: {True: "", False: set(self.bad_letters)} for i in range(self.word_size)}

        for guess, response in zip(self.guesses, self.responses):
            for idx, letter_and_info in enumerate(zip(guess, response)):
                if letter_and_info[1] == LetterInfo.IN_POSITION:
                    position_parts[idx][True] = letter_and_info[0]
                elif letter_and_info[1] == LetterInfo.IN_WORD:
                    position_parts[idx][False].add(letter_and_info[0])

        if not self.bad_letters:
            pattern = ".*"
        else:
            pattern = ""

            for idx, mapping in position_parts.items():
                if mapping[True]:
                    pattern += mapping[True]
                else:
                    pattern += f"[^{''.join(mapping[False])}]"

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
        """The frequency of letters in the remaining words that confirm to previous responses."""
        return {i: sum(1 for j in self.remaining_words if i in j) for i in self.remaining_letters}

    def reset(self) -> None:
        self.guesses: list[str] = []
        self.responses: list[Response] = []
        self.turns_remaining = self.max_guess
        self._cache_guesses: list[str] = []
        self._cache_remaining_words: list[str] = ALL_WORDS.copy()

    @abstractmethod
    def guess(self) -> str:
        ...


class PlayerRandom(BasePlayer):
    """A first attempt at a player with a guessing strategy."""
    def __init__(self, word_size: int = WORD_SIZE, max_guess: int = MAX_GUESS) -> None:
        super().__init__(word_size=word_size, max_guess=max_guess)

    def guess(self) -> str:
        return random.choice(self.remaining_words)
