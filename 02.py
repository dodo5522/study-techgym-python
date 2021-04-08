from typing import List
import random


data = [
  ['見', '見'],
  ['土', '土'],
  ['眼', '眼'],
]
labels = {
  'A': 0,
  'B': 1,
  'C': 2,
  'D': 3,
  'E': 4,
}
level = 1
col = 5
row = 4


def change_input_number(input_s: str) -> int:
  col_num = labels.get(input_s[0])
  row_num = int(input_s[1], 10) - 1
  return col_num + row_num * col


def change_string(input_n: int) -> str:
  col_num = input_n % col
  row_num = input_n // row
  return '{}{}'.format(list(labels.keys())[col_num], row_num + 1)


def is_correct_number(mistake_number: int, input_number: int) -> bool:
  return mistake_number == input_number


def view_result(is_correct: bool) -> bool:
  print('正解！' if is_correct else '不正解')
  return is_correct


def start_message() -> None:
  print('違う感じの番号(例:A1)を入力してください')


def section_message() -> int:
  print('レベル:{}'.format(level))


def view_question() -> None:
  selected_data = data[random.randint(0, 2)]
  mistake_number = random.randint(0, row * col - 1)

  print('デバッグ:mistake_number = {}'.format(mistake_number))
  print('{}'.format(selected_data))

  print('/ |{}'.format('  '.join(labels.keys())))
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
  start_message()
  mistake_number = view_question()
  section_message()

  choice = input('(例:A1)')
  print('デバッグ:choice  = {}'.format(choice))

  input_number = change_input_number(choice)
  print('デバッグ:input_number = {}'.format(change_input_number(choice)))

  if not view_result(is_correct_number(mistake_number, input_number)):
    print(change_string(mistake_number))


if __name__ == '__main__':
  play()
