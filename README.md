# Wordle Solver
The consequences of being [nerd sniped](https://xkcd.com/356/) by
[wordle](https://en.wikipedia.org/wiki/Wordle). This repo contains:
  - [interactive.py](scripts/interactive.py) a script to play on the command line (with pretty colors!)
  - [benchmark.py](scripts/benchmark.py): a way to benchmark programmatic guessing strategies
  - [wordle](wordle): extendable classes useful for implementing wordle strategies  


## Installation
Requires `Python 3.10+` to run and `poetry>=1.0.0` or `pip>=21.0` to install. To start,
clone this repository and change directories to it.
```shell script
$ git clone https://gitlab.com/james.krach/wordle.git
$ cd wordle
```

### Pip
If you're just here to play wordle, simply run:
```shell script
$ pip install .
```

To develop and test new guessing strategies, pass the `-e` flag as such:
```shell script
$ pip install -e .
```

### Poetry
```shell script
$ poetry install
```

## Play Wordle
```shell script
$ python scripts/interactive.py
```

## Developing a Strategy
  1. Extend `wordle.player.PlayerInterface` by implementing a `.guess()` method (and any
     other methods necessary for your strategy)
  2. Add your class to the `player_implementations` variable in `scripts/benchmark.py`

To benchmark your strategy against other strategies run:
``` shell script
$ python scripts/benchmark.py
```
