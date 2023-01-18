from typing import List
import random
from itertools import chain
from collections import namedtuple

State = namedtuple("State", ['expr', 'cards', 'ops_used'])

OPERATION_COUNT = 0

START = 1
END = 13
N_CARDS = 6

def deal_cards(n_cards):
    cards = []

    while len(cards) < n_cards:
        card = random.randint(START, END)

        if cards.count(card) < 4:
            cards.append(card)

    return cards

seen_exprs = {} # key: expr, val: eval(expr)
# acts as discovered and cache

def solve(target_prime: int, cards: List[int]):
    cards.sort(reverse=True)
    stack = []
    stack.append(State('', cards, 0))
    operators = ['*','+', '-'] # TODO: test whether we need /

    while len(stack) > 0:
        cur_state = stack.pop()
        expr = cur_state.expr
        if expr not in seen_exprs:
            val = None

            if is_valid_postfix(expr):
                try:
                    val = eval_postfix(expr)
                except IndexError:
                    pass

            if val == target_prime:
                return expr

            seen_exprs[expr] = val

            if cur_state.ops_used < 5 and len(expr) > 2:
                nxt_possible_items = chain(cur_state.cards, operators)
            else:
                nxt_possible_items = cur_state.cards

            for item in nxt_possible_items:
                # using operators is no longer valid
                remaining_cards = cur_state.cards.copy()
                ops_used = cur_state.ops_used
                if item in operators:
                    ops_used += 1
                elif item in remaining_cards:
                    remaining_cards.remove(item)

                if expr == '':
                    nxt_state = State(f'{item}', remaining_cards, ops_used)
                else:
                    nxt_state = State(f'{expr},{item}', remaining_cards, ops_used)

                stack.append(nxt_state)

    return "no solution found"


def is_valid_postfix(postfix_expr):
    tokens = postfix_expr.split(',')
    counter = 0

    for c in tokens:
        if c.isnumeric():
            counter += 1
        else:
            counter -= 1

        if counter < 0:
            return False

    return counter == 1


def eval_postfix(postfix_expr):
    stack = []
    tokens = postfix_expr.split(',')

    for token in tokens:
        if token.isnumeric():
            stack.append(int(token))
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            res = evaluate(token, operand1, operand2)
            stack.append(res)

    return stack.pop()

def evaluate(operator, operand1, operand2):
    global OPERATION_COUNT
    OPERATION_COUNT += 1

    if operator == "*":
        return operand1 * operand2
    elif operator == "/":
        return operand1 / operand2
    elif operator == "+":
        return operand1 + operand2
    else:
        return operand1 - operand2


if __name__ == '__main__':
    #print(deal_cards(N_CARDS))

    demo1 = "12,1,+,3,13,*,5,+,5,*,+"
    demo2 = "12,1,+"
    demo3 = "12,+"
    demo4 = "12,2,+,+ "

    # print(OPERATION_COUNT)
    # print(eval_postfix(demo1))
    # print(eval_postfix(demo2))

    # assert is_valid_postfix(demo1)
    # assert is_valid_postfix(demo2)
    # assert not is_valid_postfix(demo3)
    # assert not is_valid_postfix(demo4)

    print(solve(113, [5, 6, 9, 3, 2, 1]))

    sol = solve(233, [13, 12, 5, 5, 3, 1])
    print(sol)
    assert eval_postfix(sol) == 233

    print(f'number of operations used: {OPERATION_COUNT}')