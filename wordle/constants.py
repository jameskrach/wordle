# -*- coding: utf-8 -*-
from enum import Enum, auto
from pathlib import Path


MAX_GUESS = 6
WORD_SIZE = 5
WORD_FILE = Path(__file__).parent / "resources" / "words.txt"


class GameStatus(Enum):
    IN_PROGRESS = auto()
    WON = auto()
    LOST = auto()


class LetterInfo(Enum):
    NOT_IN_WORD = auto()
    IN_WORD = auto()
    IN_POSITION = auto()


Response = tuple[LetterInfo, ...]
