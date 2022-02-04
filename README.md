# Wordle Solver

## Installation

### Pip
```shell script
pip install .
```

### Poetry
```shell script
poetry install
```

## Play Wordle

### Interactively

```shell script
$ python scripts/interactive.py
```

### Benchmark a Player Implementation

  1. Subclass `wordle.player.PlayerInterface` by implementing a `.guess()` method
  2. Add your class to the `player_implementations` variable in `scripts/benchmark.py`
  3. Run `$ python scripts/benchmark.py`
