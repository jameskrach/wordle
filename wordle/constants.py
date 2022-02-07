# -*- coding: utf-8 -*-
from enum import Enum, auto
from pathlib import Path


MAX_GUESS = 6
WORD_SIZE = 5
GUESSABLE_NONWORD_FILE = Path(__file__).parent / "resources" / "guessable_nonwords.txt"
ANSWER_FILE = Path(__file__).parent / "resources" / "answers.txt"


with open(GUESSABLE_NONWORD_FILE) as f1, open(ANSWER_FILE) as f2:
    ANSWERS = f2.read().splitlines()
    ALL_WORDS = f1.read().splitlines() + ANSWERS


class GameStatus(Enum):
    IN_PROGRESS = auto()
    WON = auto()
    LOST = auto()


class LetterInfo(Enum):
    NOT_IN_WORD = auto()
    IN_WORD = auto()
    IN_POSITION = auto()


Response = tuple[LetterInfo, ...]
