from typing import Any
from typing import NewType
import random


class Player:
  def __init__(self, name: str, coins: int):
    Player.MIN_BET = 1
    Player.MAX_BET = 99
    self.name = name
    self.coins = coins

  def info(self):
    print('{} has {} coins'.format(self.name, self.coins))

  def bet(self) -> int:
    raise NotImplementedError


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


players: list[Player] = []


def create_players():
  global players
  players = [Human('MY', 500)]
  players.extend([Computer('C{}'.format(i), 500) for i in range(3)])


def play():
  global players
  create_players()
  for p in players:
    p.info()
  for p in players:
    bet_coin = p.bet()
    print('{}は{}コインBETしました'.format(p.name, bet_coin))
  for p in players:
    p.info()


if __name__ == '__main__':
  play()
