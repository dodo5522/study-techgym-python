from typing import Any
from typing import NewType
import random


Color = NewType('Color', [str, str])
ColorRed = Color(['red', '\033[0;31m'])
ColorBlack = Color(['black', '\033[0m'])


class Cell:
  def __init__(self, name: str, rate: int, color: Color):
    self.name = name
    self.rate = rate
    self.color = color

  def __str__(self):
    return '{}{}(x{})\033[0m'.format(self.color[1], self.name, self.rate)


table: list[Cell] = []


class Player:
  def __init__(self, name: str, coins: int):
    global table
    Player.MIN_BET = 1
    Player.MAX_BET = 99
    self.name = name
    self.coins = coins
    self.bets: dict[str, int] = {row.name: 0 for row in table}

  def info(self):
    print('{} has {} coins'.format(self.name, self.coins))

  def bet(self) -> int:
    raise NotImplementedError


players: list[Player] = []


class Human(Player):
  def __init__(self, name: str, coins: int):
    super().__init__(name, coins)

  def bet(self) -> int:
    bet_coins = 'invalid'
    while not self.verify_bet_coin(bet_coins):
      bet_coins = input('何枚BETしますか？ (1-99) -> ')
    self.coins -= int(bet_coins)
    return bet_coins

  def verify_bet_coin(self, coins: str) -> bool:
    if not str.isdecimal(coins):
      return False
    coins_ = int(coins)
    return self.MIN_BET <= coins_ <= self.MAX_BET


class Computer(Player):
  def __init__(self, name: str, coins: int):
    super().__init__(name, coins)

  def bet(self) -> int:
    bet_coin = random.randint(self.MIN_BET, self.MAX_BET)
    bet_coin = bet_coin if bet_coin <= self.coins else self.coins
    self.coins -= bet_coin
    return bet_coin


def create_table():
  table.append(Cell('R', 8, ColorRed))
  table.append(Cell('B', 8, ColorBlack))
  table.append(Cell('1', 2, ColorRed))
  table.append(Cell('2', 2, ColorBlack))
  table.append(Cell('3', 2, ColorRed))
  table.append(Cell('4', 2, ColorBlack))
  table.append(Cell('5', 2, ColorRed))
  table.append(Cell('6', 2, ColorBlack))
  table.append(Cell('7', 2, ColorRed))
  table.append(Cell('8', 2, ColorBlack))


def show_table():
  def green_bar():
    return '{}|{}'.format('\033[0;32m', '\033[0m')

  global players
  title = '| _____ | {} |'.format(' | '.join([p.name for p in players])).replace('|', green_bar())
  print(title)
  for row in table:
    line = '| {} | {} |'.format(row, ' | '.join(['{:02d}'.format(p.bets.get(row.name)) for p in players])).replace('|', green_bar())
    print(line)


def create_players():
  global players
  players = [Human('MY', 500)]
  players.extend([Computer('C{}'.format(i), 500) for i in range(3)])


def play():
  global players
  create_players()
  show_table()
  for p in players:
    p.info()
  for p in players:
    bet_coin = p.bet()
    print('{}は{}コインBETしました'.format(p.name, bet_coin))
  for p in players:
    p.info()


if __name__ == '__main__':
  create_table()
  play()
