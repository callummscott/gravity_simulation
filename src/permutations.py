""" Module for assisting with navigating pairwise relationships frequently encountered in gravity simulations. """

from typing import Generator


def ordered_pairs_permutations(a: list) -> Generator[tuple]:
    """
    Takes in a list, yields unique ordered pairings of its elements.\n
    For example: [1,2,3] -> (1,2), (1,3), (2,3).
    """
    copy = a.copy()
    for elem1 in a:
        copy.remove(elem1)
        for elem2 in copy:
            yield elem1, elem2


def unordered_pairs_permutations(a: list) -> Generator[tuple]:
    """
    Takes in a list, yields all unordered pairings of its elements.\n
    For example: [1,2,3] -> (1,2), (1,3), (2,1), (2,3), (3,1), (3,2).
    """
    for elem1 in a:
        copy = a.copy()
        copy.remove(elem1)
        for elem2 in copy:
            yield elem1, elem2


def get_others(elem, a: list) -> tuple:
    """ Returns a list of every *other* element """
    others = a.copy()
    others.remove(elem)
    return others


def all_chosen_and_others(a: list) -> Generator[tuple]:
    """
    Takes in a list, yields a tuples of an element and a list o
    f the other elements.\n
    For example: [1,2,3] -> (1, [2,3]), (2, [1,3]), (3, [1,2]).
    """
    for elem in a:
        yield elem, get_others(elem, a)
