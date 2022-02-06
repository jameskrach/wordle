#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textwrap import dedent

from wordle.constants import Response
from wordle.game import Game, LetterInfo, TurnOutcome
from wordle.player import PlayerRandom


CHAR_TO_LETTER_INFO = {
    "Y": LetterInfo.IN_POSITION,
    "M": LetterInfo.IN_WORD,
    "N": LetterInfo.NOT_IN_WORD,
}


def parse_input(game: Game, user_input: str, num_prev_guess: int) -> TurnOutcome:
    guess, response_text = user_input.split(",")

    try:
        game.validate_guess(guess)
    except ValueError:
        raise
    else:
        response: Response = tuple((CHAR_TO_LETTER_INFO[i] for i in response_text))

    return TurnOutcome(
        turns_remaining=game.max_guess - num_prev_guess,
        guess=guess,
        response=response,
    )


def instructions() -> None:
    print(dedent("""\
    __        __            _ _
    \ \      / /__  _ __ __| | | ___
     \ \ /\ / / _ \| '__/ _` | |/ _ \\
      \ V  V / (_) | | | (_| | |  __/
     _ \_/\_/ \___/|_|  \__,_|_|\___|
    | | | | ___| |_ __   ___ _ __
    | |_| |/ _ \ | '_ \ / _ \ '__|
    |  _  |  __/ | |_) |  __/ |
    |_| |_|\___|_| .__/ \___|_|
                  |_|

    Instructions:
      1. Start a game of Wordle
      2. As you guess, enter your guess and response here
      3. Guesses should be formatted as '<guess>,<response>' where:

             Y = the letter is in the correct position
             M = the letter is in the word
             N = the letter is not in the word

      4. For example if the Wordle was 'sharp' and you guessed 'heart'
         you would enter 'heart,NMYYN'
      5. Special commands:

             ? = receive a guess
             exit = exit the game
             new = start a new game
    """))


def main() -> None:
    p = PlayerRandom()
    g = Game()
    instructions()

    while True:
        user_input = input(">>> ")

        if user_input == "?":
            print(p.guess())
            continue
        elif user_input == "new":
            p.reset()
            continue
        elif user_input == "exit":
            exit(0)
        else:
            pass

        try:
            turn_outcome = parse_input(g, user_input, len(p.guesses))
        except ValueError:
            raise
        else:
            p.receive_response(turn_outcome)


if __name__ == "__main__":
    main()
