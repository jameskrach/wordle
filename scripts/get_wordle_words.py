#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pathlib import Path

from wordle.constants import WORD_FILE, WORD_SIZE


WORD_RE = re.compile(rf"^[a-z]{{{WORD_SIZE}}}$", flags=re.ASCII)
WORD_SOURCE_PATH = Path(Path.home().root) / "usr" / "share" / "dict" / "words"


def main() -> None:
    WORD_FILE.parent.mkdir(exist_ok=True)

    with open(WORD_SOURCE_PATH) as f_in:
        with open(WORD_FILE, "w") as f_out:
            for word in f_in:
                if WORD_RE.match(word.strip()):
                    f_out.write(word)

    return


if __name__ == "__main__":
    main()
