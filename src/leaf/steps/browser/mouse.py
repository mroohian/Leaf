# -*- coding: utf-8 -*-
from leaf.steps.browser.finders import _get_visible_element_in_element

__author__ = 'mroohian'

from lettuce import world, step
from leaf import get_visible_page_element
from salad.steps.browser.finders import (
    ELEMENT_FINDERS,
    ELEMENT_THING_STRING,
    PICK_EXPRESSION,
    _get_visible_element
)
from salad.steps.browser.mouse import ACTIONS, ACTION_ASSOCIATIONS
from selenium.webdriver.common.action_chains import ActionChains

def _generate_action_step(action_string, action_function):
    @step('%s the page element "([^"]+)"' % action_string)
    def _the_step(step, element_name):
        page_element = get_visible_page_element(element_name)

        if action_function == 'click':
            page_element.click()
            return

        action_chain = ActionChains(world.browser.driver)
        function = getattr(action_chain, ACTION_ASSOCIATIONS[action_function])
        if action_function == 'mouse_out':
            function(5000, 5000)
        else:
            function(page_element)
        action_chain.perform()

    return _the_step


def _generate_action_step_inside(finder_string, finder_function, action_string, action_function):
    pattern = ('%s (?:a|the)%s %s %s inside the page element "([^"]+)"' %
          (action_string, PICK_EXPRESSION, ELEMENT_THING_STRING, finder_string))

    @step('%s (?:a|the)%s %s %s inside the page element "([^"]+)"' %
          (action_string, PICK_EXPRESSION, ELEMENT_THING_STRING, finder_string))
    def _the_step(step, pick, find_pattern, parent_name):
        page_element = _get_visible_element_in_element(parent_name, finder_function, pick, find_pattern)

        if action_function == 'click':
            page_element.click()
            return

        action_chain = ActionChains(world.browser.driver)
        function = getattr(action_chain, ACTION_ASSOCIATIONS[action_function])
        if action_function == 'mouse_out':
            function(5000, 5000)
        else:
            function(page_element)
        action_chain.perform()

    return _the_step

def _generate_hybrid_drag_and_drop(finder_string, finder_function):
    @step(r'drag the%s %s %s and drop it on the page element "([^"]+)"$' % (
          PICK_EXPRESSION, ELEMENT_THING_STRING, finder_string))
    def _drag_thing_2_page_el(step, pick, find_pattern, element_name):
        src = _get_visible_element(finder_function, pick, find_pattern)
        target = get_visible_page_element(element_name)

        action_chain = ActionChains(world.browser.driver)
        action_chain.drag_and_drop(src, target)
        action_chain.perform()

    @step(r'drag the page element "([^"]+)" and drop it on the%s %s %s$' % (
          PICK_EXPRESSION, ELEMENT_THING_STRING, finder_string))
    def _drag_page_el_2_thing(step, element_name, pick, find_pattern):
        src = get_visible_page_element(element_name)
        target = _get_visible_element(finder_function, pick, find_pattern)

        action_chain = ActionChains(world.browser.driver)
        action_chain.drag_and_drop(src, target)
        action_chain.perform()

def _generate_drag_and_drop():
    @step(r'drag the page element "([^"]+)" and drop it on the page element "([^"]+)"$')
    def _drag_page_el_2_page_el(step, elemant_name_src, element_name_target):
        src = get_visible_page_element(elemant_name_src)
        target = get_visible_page_element(element_name_target)

        action_chain = ActionChains(world.browser.driver)
        action_chain.drag_and_drop(src, target)
        action_chain.perform()

for _action_string, _action_function in ACTIONS.iteritems():
    _generate_action_step(_action_string, _action_function)

    for finder_string, finder_function in ELEMENT_FINDERS.iteritems():
        _generate_action_step_inside(finder_string, finder_function, _action_string, _action_function)

_generate_drag_and_drop()

for finder_string, finder_function in ELEMENT_FINDERS.iteritems():
    _generate_hybrid_drag_and_drop(finder_string, finder_function)
