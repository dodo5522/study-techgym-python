import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import requests
from typing import List
from typing import NewType


Result = NewType('Result', int)
NoResult = Result(0)
Win = Result(1)
Lose = Result(2)

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


class Human(Player):
  def __init__(self):
    super().__init__('myself')


class Computer(Player):
  def __init__(self):
    super().__init__('ai')


def load_image() -> List[np.ndarray]:
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


def create_cards(card_images: List[np.ndarray]) -> List[Card]:
  cards: List[Card] = []
  marks = ['ハート', 'スペード', 'ダイヤ', 'クローバー']
  display_names = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
  numbers = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

  for i, mark in enumerate(marks):
    for j, number in enumerate(numbers):
      cards.append(Card(mark, display_names[j], number, card_images[i * len(numbers) + j]))

  return cards


def deal_card(cards: List[Card], player: Player) -> Card:
  cards_not_dealed = list(filter(lambda c: not c.is_dealed(), cards))
  dealing_card_index = random.randint(0, len(cards_not_dealed) - 1)
  dealing_card = cards_not_dealed[dealing_card_index]
  dealing_card.dealed()

  player.cards.append(dealing_card)
  player.total_number += 1

  return dealing_card


def result(player: Player) -> Result:
  s = sum([c.number for c in player.cards])
  print('sum: {}'.format(s))
  if s == 21:
    return Win
  elif s > 21:
    return Lose
  else:
    return NoResult


def show_card(player: Player) -> None:
  print('{} has {}'.format(player.name, ', '.join(['{}{}'.format(c.mark, c.display_name) for c in player.cards])))
  for i, c in enumerate(player.cards):
    plt.subplot(1, 6, i + 1)
    plt.axis("off")
    plt.imshow(c.image)
  plt.show()


def play() -> None:
  players = [Human(), Computer()]
  cards = create_cards(load_image())

  counter = 0
  player = None
  winner = None
  loser = None

  while True:
    player = players[counter & 1]
    card = deal_card(cards, player)
    print('{}: {}'.format(player.name, card.number))
    print(result(player))
    if result(player) == Win:
      winner = player
      break
    elif result(player) == Lose:
      loser = player
      break

  if winner != None:
    print('Winner is {}!'.format(winner.name))
    show_card(winner)
  elif loser != None:
    print('Loser is {}...'.format(loser.name))
    show_card(loser)
  else:
    print('no one')


if __name__ == '__main__':
  play()
