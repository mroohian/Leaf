# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from lettuce import world
from salad.exceptions import ElementIsNotVisible, ElementDoesNotExist, ElementAtIndexDoesNotExist
from salad.steps.browser.finders import (
    PATTERN_ASSOCIATION,
    FINDER_ASSOCIATION
)
from salad.steps.parsers import pick_to_index
from leaf import get_visible_page_element

def _get_visible_element_in_element(parent_name, finder_function, pick, pattern):
    parent_element = get_visible_page_element(parent_name)
    if not parent_element:
        exception, msg = world.failure
        raise exception(msg)

    element = _get_element_in_element(parent_element, finder_function, pick, pattern)
    if not element:
        exception, msg = world.failure
        raise exception(msg)
    if not element.is_displayed():
        raise ElementIsNotVisible("The element exist, but it is not visible. "
                                  "function: %s, pattern: %s, index: %s" %
                                  (finder_function, pattern, pick))
    return element


def _get_element_in_element(parent_element, finder_function, pick, pattern):
    # to support the splinter legacy functions
    legacy_functions = ['by_value', 'by_partial_href', 'by_href']
    for lf in legacy_functions:
        if lf in finder_function:
            finder_function = "find_by_css"
            pattern = PATTERN_ASSOCIATION[lf] % (pattern, )

    finder_function = FINDER_ASSOCIATION[finder_function]
    element = parent_element.__getattribute__(finder_function)(pattern)
    if not element:
        msg = ("function: %s, pattern: %s, index: %s" %
               (finder_function, pattern, pick))
        world.failure = (ElementDoesNotExist, msg)
        return None

    index = pick_to_index(pick)
    try:
        element = element[index]
    except IndexError:
        msg = ("There are elements that match your search, but the index is "
               "out of range.\nfunction: %s, pattern: %s, index: %s" %
               (finder_function, pattern, pick))
        world.failure = (ElementAtIndexDoesNotExist, msg)
        return None

    world.current_element = element
    return element

