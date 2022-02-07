# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from random import choice

from .constants import ALL_WORDS, ANSWERS, GameStatus, LetterInfo, MAX_GUESS, WORD_SIZE, Response


@dataclass
class TurnOutcome:
    turns_remaining: int
    guess: str
    response: Response

    def __post_init__(self) -> None:
        if self.turns_remaining < 0:
            raise ValueError("Number of remaining turns must be >0")

    @property
    def game_status(self) -> GameStatus:
        if set(self.response) == {LetterInfo.IN_POSITION}:
            return GameStatus.WON
        elif not self.turns_remaining:
            return GameStatus.LOST
        else:
            return GameStatus.IN_PROGRESS


@dataclass
class Game:
    max_guess: int = MAX_GUESS
    word_size: int = WORD_SIZE
    guesses: list[str] = field(default_factory=list)
    secret_word: str | None = None

    def __post_init__(self) -> None:
        if not self.secret_word:
            self.secret_word = choice(ANSWERS)

    def reset(self, secret_word: str | None = None) -> None:
        self.guesses = []

        if secret_word is None:
            self.secret_word = choice(ANSWERS)
        elif secret_word not in ALL_WORDS:
            raise ValueError("secret_word is not a valid word")
        else:
            self.secret_word = secret_word

    @property
    def turn(self) -> int:
        return len(self.guesses)

    def validate_guess(self, guess: str) -> None:
        if not guess.isalpha() or guess != guess.lower():
            raise ValueError("guess must only contain [a-z]")
        elif len(guess) != self.word_size:
            raise ValueError(f"guess must be {self.word_size} characters long")
        elif guess not in ALL_WORDS:
            raise ValueError("characters in guess do not form a valid word")
        else:
            pass

    def handle_guess(self, guess: str) -> TurnOutcome:
        self.validate_guess(guess)
        self.guesses.append(guess)
        response_parts: list[LetterInfo] = []

        for idx, letter in enumerate(guess):
            if self.secret_word[idx] == letter:
                response_parts.append(LetterInfo.IN_POSITION)
            elif letter in self.secret_word:
                response_parts.append(LetterInfo.IN_WORD)
            else:
                response_parts.append(LetterInfo.NOT_IN_WORD)

        return TurnOutcome(
            turns_remaining=self.max_guess - len(self.guesses),
            guess=guess,
            response=tuple(response_parts)
        )
