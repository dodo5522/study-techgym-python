from typing import List
from typing import Tuple
from typing import Dict
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


class Player:
  def __init__(self, name: str, coins: int):
    global table
    Player.MIN_BET = 1
    Player.MAX_BET = 99
    self.name = name
    self.coins = coins
    self.bets: dict[str, int] = {name: 0 for name in table.keys()}

  def info(self):
    print('{} has {} coins'.format(self.name, self.coins))

  def bet(self) -> Tuple[str, int]:
    raise NotImplementedError

  def set_bet_coins(self, bet_cell: str, bet_coins: int) -> None:
    self.bets[bet_cell] = bet_coins

  def reset_table(self):
    for name in self.bets.keys():
      self.bets[name] = 0

  def get_bet_cell_names(self) -> List[str]:
    return list(filter(lambda name : self.bets.get(name) > 0, self.bets.keys()))


table: Dict[str, Cell] = {}
players: List[Player] = []


class Human(Player):
  def __init__(self, name: str, coins: int):
    super().__init__(name, coins)

  def bet(self) -> Tuple[str, int]:
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
    return (self.MIN_BET <= coins_ <= self.MAX_BET) and (coins_ <= self.coins)

  def verify_bet_cell(self, cell_name: str) -> bool:
    return list(table.keys()).count(cell_name) > 0


class Computer(Player):
  def __init__(self, name: str, coins: int):
    super().__init__(name, coins)

  def bet(self) -> Tuple[str, int]:
    cell_names = [name for name in table.keys()]
    bet_cell = cell_names[random.randint(0, len(cell_names) - 1)]
    bet_coins = random.randint(self.MIN_BET, self.MAX_BET)
    bet_coins = bet_coins if bet_coins <= self.coins else self.coins
    self.coins -= bet_coins
    return bet_cell, bet_coins


def initialize() -> None:
  def create_table() -> None:
    table['R'] = Cell('R', 2, ColorRed)
    table['B'] = Cell('B', 2, ColorBlack)
    table['1'] = Cell('1', 8, ColorRed)
    table['2'] = Cell('2', 8, ColorBlack)
    table['3'] = Cell('3', 8, ColorRed)
    table['4'] = Cell('4', 8, ColorBlack)
    table['5'] = Cell('5', 8, ColorRed)
    table['6'] = Cell('6', 8, ColorBlack)
    table['7'] = Cell('7', 8, ColorRed)
    table['8'] = Cell('8', 8, ColorBlack)

  def create_players() -> None:
    players.append(Human('MY', 500))
    players.extend([Computer('C{}'.format(i), 500) for i in range(3)])
    for p in players:
      p.info()

  create_table()
  create_players()


def show_table() -> None:
  def green_bar():
    return '{}|{}'.format('\033[0;32m', '\033[0m')

  title = '| _____ | {} |'.format(' | '.join([p.name for p in players])).replace('|', green_bar())
  print(title)
  for name in table.keys():
    line = '| {} | {} |'.format(table.get(name), ' | '.join(['{:02d}'.format(p.bets.get(name)) for p in players])).replace('|', green_bar())
    print(line)


def reset_table() -> None:
  for p in players:
    p.reset_table()


def bet_players() -> None:
  for p in players:
    cell, coins = p.bet()
    p.set_bet_coins(cell, coins)
    print('{}は{}コインを{}にBETしました'.format(p.name, coins, cell))


def check_hit() -> None:
  loose_cell_names = ('R', 'B')
  target_cell_names = list(table.keys())
  for cell_name in loose_cell_names:
    target_cell_names.remove(cell_name)

  name = random.choice(target_cell_names)
  cell = table.get(name)
  color = cell.color
  print('選ばれたのは{}({}), レートは{}'.format(name, color[0], cell.rate))

  def is_match_color(p: Player):
    bet_name = p.get_bet_cell_names()[0]
    bet_color = table.get(bet_name).color
    if bet_name in loose_cell_names:
      return bet_color == color
    else:
      return bet_name == name

  hit_players = list(filter(is_match_color, players))
  if len(hit_players) > 0:
    for p in hit_players:
      bet_name = p.get_bet_cell_names()[0]
      bet_cell = table.get(bet_name)
      got_coins = bet_cell.rate * p.bets.get(bet_name)
      p.coins += got_coins
      print('{}は当たり{}コインを獲得しました'.format(p.name, got_coins))
  else:
    print('当たりはいませんでした')


def show_coins() -> None:
  results = ['{}:{}'.format(p.name, p.coins) for p in players]
  print('[持ちコイン] {}'.format(' / '.join(results)))


def is_game_end() -> bool:
  return any(map(lambda p: p.coins <= 0, players))


def end_game() -> None:
  lost_players = filter(lambda p: p.coins <= 0, players)
  print('{}のコインがなくなったため、ゲームを終了します'.format(
    ', '.join([p.name for p in lost_players])))


def play_once():
  bet_players()
  show_table()
  check_hit()
  show_coins()


def play():
  while is_game_end() is False:
    play_once()
    reset_table()
  else:
    end_game()


if __name__ == '__main__':
  initialize()
  play()
