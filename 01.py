import random
from typing import Any


def is_hand(hand: Any) -> bool:
    if type(hand) is not str:
        return False
    elif not hand.isnumeric():
        return False
    return int(hand) in range(3)


def get_hand_name(hand_number: int) -> str:
    num_to_str = [
        'グー',
        'チョキ',
        'パー',
    ]
    return num_to_str[hand_number]


def start_message() -> None:
    print('自分の手を入力してください')


def get_my_hand() -> str:
    message = ', '.join(
        ['{}:{}'.format(i, get_hand_name(i)) for i in range(3)])
    return input(message + '-> ')


def get_your_hand() -> int:
    return random.randint(0, 2)


def view_hands(my_hand: int, your_hand: int) -> None:
    print('自分の手は{}'.format(get_hand_name(my_hand)))
    print('相手の手は{}'.format(get_hand_name(your_hand)))


def get_result(hand_diff: int) -> str:
    if hand_diff == 0:
        return 'draw'
    elif hand_diff == -1 or hand_diff == 2:
        return 'win'
    else:
        return 'lose'


def view_result(my_hand: int, your_hand: int) -> str:
    results = {
        'win': '勝ち',
        'lose': '負け',
        'draw': 'あいこ',
    }
    view_hands(my_hand, your_hand)
    hand_diff = my_hand - your_hand
    result = get_result(hand_diff)
    print(results.get(result))
    return result


def play() -> None:
    result = 'draw'
    print('じゃんけんスタート')
    while result == 'draw':
        start_message()
        my_hand = get_my_hand()
        if not is_hand(my_hand):
            continue
        result = view_result(int(my_hand), get_your_hand())


if __name__ == '__main__':
    play()

