from typing import List
from typing import NewType
import random


InningSide = NewType('InningSide', int)
InningTop = InningSide(0)
InningBottom = InningSide(1)


class Team:
  def __init__(self, name: str, attack: int, defense: int) -> None:
    self.name = name
    self.attack = attack
    self.defense = defense
    self.total_score = 0

  def info(self) -> str:
    return '{}: 攻撃力: {} / 守備力: {}'.format(self.name, self.attack, self.defense)

  def get_hit_rate(self) -> int:
    return random.randint(10, self.attack)

  def get_out_rate(self) -> int:
    return random.randint(10, self.defense)

  def add_score(self, score):
    self.total_score += score


teams = []
team_info = [
  {'name': 'attackers', 'attack': 80, 'defence': 20},
  {'name': 'defenders', 'attack': 30, 'defence': 70},
  {'name': 'averages',  'attack': 50, 'defence': 50},
]
playing_teams: dict[str, Team] = {
  'myself': None,
  'enemy': None,
}


def create_teams() -> None:
  global teams
  teams = [Team(i.get('name'), i.get('attack'), i.get('defence')) for i in team_info]


def show_teams() -> None:
  global teams
  for i, t in enumerate(teams):
    print('{}. {}'.format(i + 1, t.info()))


def choice_team(player: str) -> None:
  global playing_teams
  playser_jp = '自分' if player == 'myself' else '相手'
  num = input('{}のチームを選択してください(1~3): '.format(playser_jp))
  playing_teams[player] = teams[int(num) - 1]
  print('{}のチームは「{}」です'.format(playser_jp, playing_teams.get(player).name))


def get_play_inning(side: InningSide) -> int:
  global playing_teams
  myself = playing_teams.get('myself')
  enemy = playing_teams.get('enemy')
  if side == InningTop:
    score = (myself.get_hit_rate() - enemy.get_out_rate()) // 10 
  else:
    score = (enemy.get_hit_rate() - myself.get_out_rate()) // 10
  return 0 if score < 0 else score


def play() -> None:
  last_inning = 9
  score_boards = ['____ |', '自分 |', '相手 |']

  create_teams()
  print('全チームの情報')
  show_teams()
  choice_team('myself')
  choice_team('enemy')

  for inning in range(1, last_inning + 1):
    score_boards[0] += ' {} |'.format(inning)
  score_boards[0] += ' R |'

  for side in InningTop, InningBottom:
    for inning in range(1, last_inning + 1):
      player = list(playing_teams.keys())[side]
      if inning == last_inning and side == InningBottom:
        myself_total = playing_teams.get('myself').total_score
        enemy_total = playing_teams.get('enemy').total_score
        if enemy_total > myself_total:
          score_boards[side + 1] += ' X |'
        else:
          score = get_play_inning(side)
          playing_teams[player].add_score(score)
          score_boards[side + 1] += ' {} |'.format(score)
      else:
        score = get_play_inning(side)
        playing_teams[player].add_score(score)
        score_boards[side + 1] += ' {} |'.format(score)

  for i, player in enumerate(playing_teams.keys()):
      score_boards[i + 1] += ' {} |'.format(playing_teams.get(player).total_score)

  for board in score_boards:
    print(board)


if __name__ == '__main__':
  play()