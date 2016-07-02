# The Game

## Requirements

* Python3
* MongoDB
* Pip

## Installation

(Assuming you have mongodb and python3 installed)

1. `pip -r requirements.txt`
1. `cp env-sample .env`
1. Dump your api key into the .env file.

## Running

`python3 thegame.py`

## Commands

### List Items

#### Usage:

`list_items`

Lists the items, their rarity, and the description. Take note of the number for use.

### Use Item

#### Usage:

`use_item 252`

`use_item 252 kdiale`

Uses the item on yourself in the first invocation and on a particular target in the second invocation. The number is the ID from `list_items`.

### Points

#### Usage:

`points kdiale`

Gives some metadata about the provided target.

### Effects

#### Usage:

`effects kdiale`

Gives some metadata about the provided target.

### Exiting

Use `CTRL+C` to exit the program.
