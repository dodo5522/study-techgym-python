import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import requests
from typing import List
from typing import NewType


Choice = NewType('Choice', int)
NoChoice = Choice(0)
ChoiceHit = Choice(1)
ChoiceStand = Choice(2)


Result = NewType('Result', int)
NoResult = Result(0)
ResultBurst = Result(1)
ResultBlackJack = Result(2)


class Card:
  def __init__(self, mark: str, display_name: str, number: int, image: np.ndarray):
    self.mark = mark
    self.display_name = display_name
    self.number = number
    self.image = image
    self.dealed_ = False

  def dealed(self) -> None:
    self.dealed_ = True

  def is_dealed(self) -> bool:
    return self.dealed_

  def reset(self) -> None:
    self.dealed_ = False


class Player:
  def __init__(self, name: str):
    self.name = name
    self.cards: List[Card] = []
    self.total_number: int = 0
    self.result_: Result = NoResult
    self.coins = 500
    self.bet_coins = 0

  def reset(self) -> None:
    self.cards: List[Card] = []
    self.total_number: int = 0
    self.result_: Result = NoResult

  def choice(self) -> Choice:
    return NoChoice

  def bet(self) -> bool:
    coins_ = 100
    if self.coins <= 0:
      return False

    coins = coins_ if coins_ < self.coins else self.coins
    self.bet_coins = coins
    self.coins -= coins
    print('{}がBETしたコインは{}'.format(self.name, self.bet_coins))
    return True

  def add_coins(self) -> None:
    self.coins += self.bet_coins * 2

  def deal(self, cards: List[Card]) -> Result:
    cards_not_dealed = list(filter(lambda c: not c.is_dealed(), cards))
    dealing_card_index = random.randint(0, len(cards_not_dealed) - 1)
    dealing_card = cards_not_dealed[dealing_card_index]
    dealing_card.dealed()

    self.cards.append(dealing_card)
    self.total_number += dealing_card.number
    self.total_number = self.calc_total(self.total_number)

    if self.total_number > 21:
      self.result_ = ResultBurst
    elif self.total_number == 21:
      self.result_ = ResultBlackJack

    print('{} is dealed to {}, total {}, result {}'.format(
      dealing_card.number, self.name, self.total_number, self.result_))
    return self.result_

  def result(self) -> Result:
    return self.result_

  def total(self) -> int:
    return self.total_number

  def calc_total(self, current_total: int) -> int:
    if current_total <= 21:
      return current_total

    total = sum([c.number for c in self.cards])
    aces = len(list(filter(lambda c: c.display_name == 'A', self.cards)))

    for _ in range(aces):
      total -= 11
      total += 1
      if total <= 21:
        break

    return total


class Human(Player):
  def __init__(self):
    super().__init__('myself')
    self.stand = False

  def reset(self) -> None:
    super().reset()
    self.stand = False

  def choice(self) -> Choice:
    if len(self.cards) <= 1:
      return ChoiceHit

    if self.stand:
      return ChoiceStand

    in_data = ''
    while True:
      in_data = input('Hit(1) or stand(2)? > ').strip()
      if in_data.isdigit() is True and (int(in_data) >= 1 and int(in_data) <= 2):
        break

    self.stand = Choice(int(in_data)) == ChoiceStand
    return Choice(int(in_data))

  def bet(self) -> bool:
    if self.coins <= 0:
      return False

    coins_max = 100 if self.coins >= 100 else self.coins
    bet_coins = 0
    while True:
      coins_s = input('何枚BETしますか？ : (10-{}) > '.format(coins_max))
      if coins_s.isdigit() and (10 <= int(coins_s) <= coins_max):
        bet_coins = int(coins_s)
        break

    self.bet_coins = bet_coins
    self.coins -= bet_coins
    print('{}がBETしたコインは{}'.format(self.name, self.bet_coins))
    return True


class Computer(Player):
  def __init__(self):
    super().__init__('ai')

  def choice(self) -> Choice:
    if self.total_number > 17:
      return ChoiceStand
    else:
      return ChoiceHit


class BlackJack:
  def __init__(self):
    self.me: Player = Human()
    self.ai: Player = Computer()
    self.cards: List[Card] = self.create_cards(self.load_image())

  def load_image(self):
    card_images: List[np.ndarray] = []
    image_name = 'cards.jpg'
    vsplit_number = 4
    hsplit_number = 13

    if not os.path.isfile(image_name):
      response = requests.get('http://3156.bz/techgym/cards.jpg', allow_redirects=False)
      with open(image_name, 'wb') as image:
        image.write(response.content)

    img = cv.imread('./{}'.format(image_name))
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
  
    h, w = img.shape[:2]
    crop_img = img[:h // vsplit_number * vsplit_number, :w // hsplit_number * hsplit_number]

    for h_image in np.vsplit(crop_img, vsplit_number):
      for v_image in np.hsplit(h_image, hsplit_number):
        card_images.append(v_image)

    return card_images

  def create_cards(self, card_images: List[np.ndarray]) -> List[Card]:
    cards: List[Card] = []
    marks = ['ハート', 'スペード', 'ダイヤ', 'クローバー']
    display_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    numbers = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    for i, mark in enumerate(marks):
      for j, number in enumerate(numbers):
        cards.append(Card(mark, display_names[j], number, card_images[i * len(numbers) + j]))

    return cards

  def show_result(self, winner: Player) -> None:
    max_cards = max([len(p.cards) for p in [self.me, self.ai]])

    for p in [self.me, self.ai]:
      print('{} w/ total {}, cards {}'.format(
        p.name, p.total(), ', '.join(['{}{}'.format(c.mark, c.display_name) for c in p.cards])))

    if winner is None:
      print('Draw')
    else:
      print('{} win!!'.format(winner.name))

      for i, p in enumerate([self.me, self.ai]):
        for j, c in enumerate(p.cards):
          plt.subplot(2, max_cards, (i * max_cards) + j + 1)
          plt.axis("off")
          plt.imshow(c.image)
      plt.show()

  def judge(self) -> Player:
    if all([p.result() == ResultBlackJack for p in [self.me, self.ai]]):
      return None
    elif all([p.result() == ResultBurst for p in [self.me, self.ai]]):
      return None
    elif self.me.result() == ResultBurst:
      return self.ai
    elif self.ai.result() == ResultBurst:
      return self.me
    elif self.me.total() > self.ai.total() or self.me.result() == ResultBlackJack:
      return self.me
    elif self.me.total() < self.ai.total() or self.ai.result() == ResultBlackJack:
      return self.ai
    else:
      return None

  def reset(self):
    for p in [self.me, self.ai]:
      p.reset()
    for c in self.cards:
      c.reset()

  def play(self) -> None:
    while True:
      can_bet = True
      for p in [self.me, self.ai]:
        print('{}の持ちコインは{}枚'.format(p.name, p.coins))
        if not p.bet():
          can_bet = False

      if not can_bet:
        print('終了します')
        break

      while True:
        my_choice = self.me.choice()
        if my_choice == ChoiceHit:
          if self.me.deal(self.cards) == ResultBurst:
            break

        ai_choice = self.ai.choice()
        if ai_choice == ChoiceHit:
          if self.ai.deal(self.cards) == ResultBurst:
            break

        if all([my_choice == ChoiceStand, ai_choice == ChoiceStand]):
          break

      winner = self.judge()
      if winner != None:
        winner.add_coins()
      self.show_result(winner)
      self.reset()


if __name__ == '__main__':
  game = BlackJack()
  game.play()
