#!/usr/bin/env python
# -*- coding: utf-8 -*-
from colorama import Back, Fore, init

from wordle.game import Game, GameStatus, LetterInfo, Response


init(autoreset=True)
FORES = {
    LetterInfo.IN_POSITION: Fore.LIGHTWHITE_EX,
    LetterInfo.IN_WORD: Fore.BLACK,
    LetterInfo.NOT_IN_WORD: Fore.LIGHTWHITE_EX,
}

BACKS = {
    LetterInfo.IN_POSITION: Back.LIGHTGREEN_EX,
    LetterInfo.IN_WORD: Back.LIGHTYELLOW_EX,
    LetterInfo.NOT_IN_WORD: Back.BLACK,
}


def pretty_response(guess: str, response: Response) -> str:
    return "".join(FORES[j] + BACKS[j] + i for i, j in zip(guess, response))


def main() -> None:
    g = Game()
    game_status = GameStatus.IN_PROGRESS

    while game_status == GameStatus.IN_PROGRESS:
        while True:
            guess = input(f"Guess {g.turn + 1} of {g.max_guess}: ")

            try:
                turn_outcome = g.handle_guess(guess)
            except ValueError as e:
                print(f"{Fore.LIGHTRED_EX}{e}")
                continue
            else:
                break

        game_status = turn_outcome.game_status
        print(pretty_response(guess, turn_outcome.response))

        if game_status == GameStatus.WON:
            print(f"{Fore.LIGHTGREEN_EX}Correct! The word was '{g.secret_word}'")
        elif game_status == GameStatus.LOST:
            print(f"{Fore.LIGHTRED_EX}Game Over: The word was '{g.secret_word}'")
        else:
            pass


if __name__ == "__main__":
    main()
