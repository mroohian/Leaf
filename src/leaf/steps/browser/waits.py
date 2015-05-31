# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from lettuce import world, step
from leaf import get_visible_page_element
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from salad.steps.browser.waits import THING_STRING
from selenium.webdriver.support import expected_conditions as EC
from leaf.support.expected_conditions import (
    page_element_selection_state_to_be,
    presence_of_page_element,
    visibility_of_page_element,
    page_element_to_be_clickable,
    invisibility_of_page_element,
    text_to_be_present_in_page_element,
    text_to_be_present_in_page_element_value)
WAIT_SELECTED_OPTIONS = {
    'be selected': (page_element_selection_state_to_be, True),
    'be unselected': (page_element_selection_state_to_be, False),
}

WAIT_OPTIONS = {
    'be present': presence_of_page_element,
    'be visible': visibility_of_page_element,
    'be clickable': page_element_to_be_clickable,
    'be invisible': invisibility_of_page_element,
}
WAIT_TEXT_OPTIONS = {
    'have the text "([^"]+)"': text_to_be_present_in_page_element,
    'have the value "([^"]+)"': text_to_be_present_in_page_element_value
}
WAIT_STALE_OPTIONS = {
    '(be stale|be gone|disappear)': EC.staleness_of,
}

def _wait_for_selected_generator(condition_string, expected_condition, expected_selection_state):
    @step(r'wait for the page element "([^"]+)" to %s(?: within (\d+) seconds)?$' % condition_string)
    def _this_step(step, element_name, wait_time):
        wait_time = int(wait_time or 10)
        wait = WebDriverWait(world.browser.driver, wait_time)
        try:
            wait.until(expected_condition(element_name,
                                          expected_selection_state))
        except TimeoutException as e:
            msg = ("The page element '%s' was not '%s' within %s seconds. "
                   "The error message was: '%s'." %
                   (element_name, condition_string, wait_time, e))
            raise AssertionError(msg)


def _wait_for_generator(condition_string, expected_condition):
    @step(r'wait for the page element "([^"]+)" to %s(?: within (\d+) seconds)?$' % condition_string)
    def _this_step(step, element_name, wait_time):
        wait_time = int(wait_time or 10)
        wait = WebDriverWait(world.browser.driver, wait_time)
        try:
            wait.until(expected_condition(element_name))
        except TimeoutException as e:
            msg = ("The page element '%s' was not '%s' within %s seconds. "
                   "The error message was: '%s'." %
                   (element_name, condition_string, wait_time, e))
            raise AssertionError(msg)


def _wait_for_text_generator(condition_string, expected_condition):
    @step(r'wait for the page element "([^"]+)" to %s(?: within (\d+) seconds)?$' % condition_string)
    def _this_step(step, element_name, text, wait_time):
        wait_time = int(wait_time or 10)
        wait = WebDriverWait(world.browser.driver, wait_time)
        try:
            wait.until(expected_condition(element_name, text))
        except TimeoutException as e:
            msg = ("The page element '%s' did not %s '%s' within %s seconds. "
                   "The error message was: '%s'." %
                   (element_name, condition_string, text,
                    wait_time, e))
            raise AssertionError(msg)

def _wait_for_stale_generator(condition_string, expected_condition):
    @step(r'wait for the page element "([^"]+)" to %s(?: within (\d+) seconds)?$' % condition_string)
    def _this_step(step, element_name, text, wait_time):
        wait_time = int(wait_time or 10)
        wait = WebDriverWait(world.browser.driver, wait_time)
        try:
            element = get_visible_page_element(element_name)
            wait.until(expected_condition(element))
        except TimeoutException as e:
            msg = ("The page element '%s' was not %s within %s seconds. "
                   "The error message was: '%s'." %
                   (element_name, condition_string,
                    wait_time, e))
            raise AssertionError(msg)
        except (NoSuchElementException, StaleElementReferenceException,
                WebDriverException) as n:
            msg = ("The page element must first be present and not stale so that "
                   "it can become stale later.\nError msg was: '%s'" % (n, ))
            raise AssertionError(msg)

for condition_string, ec_tuple in WAIT_SELECTED_OPTIONS.iteritems():
    expected_condition, expected_selection_state = ec_tuple
    _wait_for_selected_generator(condition_string, expected_condition, expected_selection_state)

for condition_string, expected_condition in WAIT_OPTIONS.iteritems():
    _wait_for_generator(condition_string, expected_condition)

for condition_string, expected_condition in WAIT_TEXT_OPTIONS.iteritems():
    _wait_for_text_generator(condition_string, expected_condition)

for condition_string, expected_condition in WAIT_STALE_OPTIONS.iteritems():
    _wait_for_stale_generator(condition_string, expected_condition)
