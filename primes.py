import random
import statistics
from collections import namedtuple
from itertools import chain
from typing import List

State = namedtuple("State", ["expr", "cards", "ops_used"])

OPERATION_COUNT = 0

START = 1
END = 13
N_CARDS = 6


def deal_cards(n_cards: int) -> List[int]:
    cards = []

    while len(cards) < n_cards:
        card = random.randint(START, END)

        if cards.count(card) < 4:
            cards.append(card)

    return cards


def solve(target_prime: int, cards: List[int]):
    seen_exprs = set()

    cards.sort(reverse=True)
    stack = []
    stack.append(State("", cards, 0))
    operators = ["*", "+", "-"]  # empirically it appears we do not need / operator

    while len(stack) > 0:
        cur_state = stack.pop()
        expr = cur_state.expr
        if expr not in seen_exprs:
            val = None

            # only evaluate once we have a finished possible expression
            if cur_state.ops_used == 5 and is_valid_postfix(expr):
                # is valid postfix is a quick check with some edges cases that are missed
                try:
                    val = eval_postfix(expr)
                except IndexError:
                    pass

            if val == target_prime:
                return postfix_to_infix(expr)

            seen_exprs.add(expr)

            if cur_state.ops_used < 5 and len(expr) > 2:
                nxt_possible_items = chain(cur_state.cards, operators)
            else:
                nxt_possible_items = cur_state.cards

            for item in nxt_possible_items:
                remaining_cards = cur_state.cards.copy()
                ops_used = cur_state.ops_used
                if item in operators:
                    ops_used += 1
                elif item in remaining_cards:
                    remaining_cards.remove(item)

                if expr == "":
                    nxt_state = State(f"{item}", remaining_cards, ops_used)
                else:
                    nxt_state = State(f"{expr},{item}", remaining_cards, ops_used)

                stack.append(nxt_state)

    return "no solution found"


def is_valid_postfix(postfix_expr):
    tokens = postfix_expr.split(",")
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
    tokens = postfix_expr.split(",")

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
        return int(operand1 / operand2)
    elif operator == "+":
        return operand1 + operand2
    else:
        return operand1 - operand2


def postfix_to_infix(postfix_expr):
    tokens = postfix_expr.split(",")

    stack = []

    for token in tokens:
        if token.isnumeric():
            stack.append(token)

        else:
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(f"({op2}{token}{op1})")

    return stack.pop()


def run_experiments(primes, n_deals):
    global OPERATION_COUNT

    no_soln = []
    stats = {}
    for prime in primes:
        ops = []
        for _ in range(n_deals):
            OPERATION_COUNT = 0
            cards = deal_cards(6)
            res = solve(prime, cards)
            print(f"target: {prime} | res: {res} | ops: {OPERATION_COUNT}")

            if res == "no solution found":
                no_soln.append((prime, cards))
            else:
                ops.append(OPERATION_COUNT)

        avg_ops = statistics.mean(ops)
        std_ops = statistics.stdev(ops)
        stats[prime] = (avg_ops, std_ops)
        print("------------------------------------------------------------")
        print(f"{prime} | avg {avg_ops:.0f} operations | std {std_ops:.2f}")
        print("------------------------------------------------------------")

    print(f"number of no found solution: {len(no_soln)}")
    print(no_soln)

    print(stats)
    return stats


if __name__ == "__main__":
    primes = [359, 163, 373, 293, 269, 197, 151, 349, 317, 109]
    n_deals = 10
    run_experiments(primes, n_deals)
