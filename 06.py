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


class Player:
  def __init__(self, name: str):
    self.name = name
    self.cards: List[Card] = []
    self.total_number: int = 0
    self.result_: Result = NoResult

  def choice(self) -> Choice:
    return NoChoice

  def deal(self, cards: List[Card]) -> Result:
    cards_not_dealed = list(filter(lambda c: not c.is_dealed(), cards))
    dealing_card_index = random.randint(0, len(cards_not_dealed) - 1)
    dealing_card = cards_not_dealed[dealing_card_index]
    dealing_card.dealed()

    self.cards.append(dealing_card)
    self.total_number += dealing_card.number

    if self.total_number > 21:
      self.result_ = ResultBurst
    elif self.total_number == 21:
      self.result_ = ResultBlackJack

    print('{} is dealed to {}, total {}, result {}'.format(
      dealing_card.number, self.name, self.total_number, self.result_))
    return self.result_

  def result(self):
    return self.result_

  def total(self):
    return self.total_number


class Human(Player):
  def __init__(self):
    super().__init__('myself')
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


class Computer(Player):
  def __init__(self):
    super().__init__('ai')

  def choice(self) -> Choice:
    if self.total_number > 17:
      return ChoiceStand
    else:
      return ChoiceHit


class Game:
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
    for p in [self.me, self.ai]:
      print('{} w/ total {}, cards {}'.format(
        p.name, p.total(), ', '.join(['{}{}'.format(c.mark, c.display_name) for c in p.cards])))

    if winner is None:
      print('Draw')
    else:
      print('{} win!!'.format(winner.name))

      for i, p in enumerate([self.me, self.ai]):
        for j, c in enumerate(p.cards):
          plt.subplot(2, 6, (i * 6) + j + 1)
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

  def play(self) -> None:
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

    self.show_result(self.judge())


if __name__ == '__main__':
  game = Game()
  game.play()
