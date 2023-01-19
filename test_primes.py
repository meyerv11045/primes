from primes import *


def test_deal_cards():
    res = deal_cards(6)
    assert len(res) == 6
    for card in res:
        assert card in list(range(1, 14))


def test_is_valid_postfix():
    demo1 = "12,1,+,3,13,*,5,+,5,*,+"
    demo2 = "12,1,+"
    demo3 = "12,+"
    demo4 = "12,2,+,+ "

    assert is_valid_postfix(demo1)
    assert is_valid_postfix(demo2)
    assert not is_valid_postfix(demo3)
    assert not is_valid_postfix(demo4)


def test_eval_postfix():
    demo1 = "12,1,+"
    demo2 = "12,1,+,3,13,*,5,+,5,*,+"

    assert eval_postfix(demo1) == 13
    assert eval_postfix(demo2) == 233


def test_postfix_to_infix():
    postfix = "1,3,-,5,5,12,*,13,-,*,+"
    infix = "((1-3)+(5*((5*12)-13)))"
    assert postfix_to_infix(postfix) == infix
