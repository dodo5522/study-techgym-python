from typing import List
import random


data = [
  ['見', '貝'],
  ['土', '士'],
  ['眠', '眼'],
]
labels = {
  'A': 0,
  'B': 1,
  'C': 2,
  'D': 3,
  'E': 4,
}

levels = [
  # row, col
  [3, 3],
  [3, 4],
  [4, 4],
  [4, 5],
  [5, 5],
  [5, 6],
  [6, 6],
  [6, 7],
  [7, 7],
  [7, 8],
  [8, 8],
  [8, 9],
  [9, 9],
]


def change_input_number(input_s: str, col: int) -> int:
  col_num = labels.get(input_s[0])
  row_num = int(input_s[1], 10) - 1
  return col_num + row_num * col


def change_string(input_n: int, row: int, col: int) -> str:
  col_num = input_n % col
  row_num = input_n // row
  return '{}{}'.format(list(labels.keys())[col_num], row_num + 1)


def is_correct_number(mistake_number: int, input_number: int) -> bool:
  return mistake_number == input_number


def view_result(is_correct: bool) -> bool:
  print('正解！' if is_correct else '不正解')
  return is_correct


def start_message() -> None:
  print('違う漢字の番号(例:A1)を入力してください')


def section_message(level: int) -> int:
  print('レベル:{}'.format(level + 1))


def view_question(row: int, col: int) -> None:
  selected_data = data[random.randint(0, 2)]
  mistake_number = random.randint(0, row * col - 1)

  print('{}'.format(selected_data))
  print('/ |{}'.format('  '.join(list(labels.keys())[i] for i in range(col))))
  print('{}'.format(''.join(['-' for _ in range(3 * (col +  1))])))

  row_ = 0
  while row_ < row:
    col_ = 0
    print('{} |'.format(row_ + 1), end='')
    while col_ < col:
      idx = 1 if mistake_number is row_ * col + col_ else 0
      print('{} '.format(selected_data[idx]), end='')
      col_ += 1
    print('')
    row_ += 1

  return mistake_number


def play() -> None:
  level = 0
  start_message()

  while 0 <= level < len(levels):
    row = levels[level][0]
    col = levels[level][1]

    section_message(level)
    mistake_number = view_question(row, col)

    choice = input('(例:A1)')
    #print('デバッグ:choice  = {}'.format(choice))

    input_number = change_input_number(choice, col)
    #print('デバッグ:input_number = {}'.format(change_input_number(choice)))

    if not view_result(is_correct_number(mistake_number, input_number)):
      print(change_string(mistake_number, row, col))
      level -= 1
    else:
      level += 1


if __name__ == '__main__':
  play()
