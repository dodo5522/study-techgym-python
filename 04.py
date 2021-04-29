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

  def bet(self) -> list[str, int]:
    raise NotImplementedError

  def set_bet_coins(self, bet_cell: str, bet_coins: int) -> None:
    self.bets[bet_cell] = bet_coins


players: list[Player] = []


class Human(Player):
  def __init__(self, name: str, coins: int):
    super().__init__(name, coins)

  def bet(self) -> list[str, int]:
    bet_coins = ''
    bet_cell = ''
    while not self.verify_bet_coin(bet_coins):
      bet_coins = input('何枚BETしますか？ (1-99) -> ')
    while not self.verify_bet_cell(bet_cell):
      bet_cell = input('どこにBETしますか？ (R,B,1-8) -> ')
    self.coins -= int(bet_coins)
    return bet_cell, int(bet_coins)

  def verify_bet_coin(self, coins: str) -> bool:
    if not str.isdecimal(coins):
      return False
    coins_ = int(coins)
    return self.MIN_BET <= coins_ <= self.MAX_BET

  def verify_bet_cell(self, cell_name: str) -> bool:
    cell_names = [i.name for i in filter(lambda row: row.name == cell_name, table)]
    return cell_names.count(cell_name) != 0


class Computer(Player):
  def __init__(self, name: str, coins: int):
    super().__init__(name, coins)

  def bet(self) -> list[str, int]:
    cell_names = [row.name for row in table]
    bet_cell = cell_names[random.randint(0, len(cell_names) - 1)]
    bet_coins = random.randint(self.MIN_BET, self.MAX_BET)
    bet_coins = bet_coins if bet_coins <= self.coins else self.coins
    self.coins -= bet_coins
    return bet_cell, bet_coins


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
  for p in players:
    p.info()


def bet_players():
  global players
  for p in players:
    cell, coins = p.bet()
    p.set_bet_coins(cell, coins)
    print('{}は{}コインを{}にBETしました'.format(p.name, coins, cell))


def play():
  global players
  create_players()
  show_table()
  bet_players()
  show_table()


if __name__ == '__main__':
  create_table()
  play()
