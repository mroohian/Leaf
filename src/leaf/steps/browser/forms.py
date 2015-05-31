# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from lettuce import world, step
from leaf import get_visible_page_element
from salad.steps.browser.forms import (
    _type_slowly,
    _fill_in_text,
    _get_visible_element,
    transform_key_string
)
from salad.tests.util import (
    wait_for_completion,
    assert_value,
    transform_for_upper_lower_comparison,
    store_with_case_option
)

from selenium.webdriver.support.ui import Select

# TODO: add a step definition for file upload fields


# TODO: add type or enter here and also in salad
@step(r'(slowly )?type "([^"]*)" into the page element "([^"]*)"$')
def _this_step(step, slowly, text, element_name):
    page_element = get_visible_page_element(element_name)
    if slowly and slowly != "":
        _type_slowly(page_element, text)
    else:
        page_element.send_keys(text)

@step(r'deselect all options from the page element "([^"]*)"$')
def _this_step(step, element_name):
    page_element = get_visible_page_element(element_name)
    select = Select(page_element)
    select.deselect_all()

@step(r'(de)?select the option with the (index|value|text)'
      '( that is the stored value of)? "([^"]+)" '
      'from the page element "([^"]+)"$')
def _this_step(step, negate, by_what, stored, value, element_name):
    page_element = get_visible_page_element(element_name)
    select = Select(page_element)
    # get value from storage if necessary
    if stored:
        value = world.stored_values[value]
    # adjust variables for proper Select usage
    if by_what == 'text':
        by_what = 'visible_text'
    elif by_what == 'index':
        value = int(value)
    # select or deselect according to negate
    attribute_mask = 'deselect_by_%s' if negate else 'select_by_%s'
    # get the method
    select_method = getattr(select, attribute_mask % (by_what, ))
    # select the correct option
    select_method(value)

@step(r'fill in the page element "([^"]+)" with "([^"]*)"$')
def _this_step(step, element_name, text):
    page_element = get_visible_page_element(element_name)
    _fill_in_text(page_element, text)

@step(r'fill in the page element "([^"]+)" with the stored value of "([^"]*)"$')
def _this_step(step, element_name, name):
    page_element = get_visible_page_element(element_name)
    assert(world.stored_values[name])
    _fill_in_text(page_element, world.stored_values[name])

@step(r'attach "([^"]*)" onto the page element "([^"]+)"$')
def _this_step(step, file_name, element_name):
    page_element = get_visible_page_element(element_name)
    _fill_in_text(page_element, file_name)

@step(r'focus on the page element "([^"]+)"$')
def _this_step(step, element_name):
    page_element = get_visible_page_element(element_name)
    page_element.click()

@step(r'(?:blur|move) from the page element "([^"]+)"$')
def _this_step(step, element_name):
    # make sure the element is visible anyway
    get_visible_page_element(element_name)
    # then click on the body of the html document
    ele = _get_visible_element('find_by_tag', None, 'body')
    ele.click()

@step(r'should( not)? see that the (value|text|html|outer html) of '
      'the page element "([^"]+)" (is|contains) "([^"]*)"'
      '(?: within (\d+) seconds)?$')
def _this_step(step, negate, attribute, element_name, type_of_match, value, wait_time):
    def assert_element_attribute_is_or_contains_text(
            negate, attribute, element_name,
            type_of_match, value):
        ele_value = _get_attribute_of_element(element_name, attribute)
        assert_value(type_of_match, value, ele_value, negate)
        return True
    wait_for_completion(
        wait_time, assert_element_attribute_is_or_contains_text,
        negate, attribute, element_name, type_of_match, value)

@step(r'should( not)? see that the (value|text|html|outer html) of '
      'the page element "([^"]+)" (is|contains) the stored( lowercase| uppercase|'
      ' case independent)? value of "([^"]*)"'
      '(?: within (\d+) seconds)?$')
def _this_step(step, negate, attribute, element_name, type_of_match, upper_lower, name, wait_time):
    def assert_element_attribute_is_or_contains_stored_value(
            negate, attribute, element_name, type_of_match,
            upper_lower, name):
        current = _get_attribute_of_element(element_name, attribute)
        stored = world.stored_values[name]
        if upper_lower:
            stored, current = transform_for_upper_lower_comparison(
                stored, current, upper_lower)
        assert_value(type_of_match, stored, current, negate)
        return True
    wait_for_completion(
        wait_time,
        assert_element_attribute_is_or_contains_stored_value, negate,
        attribute, element_name, type_of_match, upper_lower,
        name)

@step(r'hit the "([^"]*)" key in the page element "([^"]+)"$')
def _this_step(step, key_string, element_name):
    page_element = get_visible_page_element(element_name)
    key = transform_key_string(key_string)
    page_element.send_keys(key)

@step(r'(?:store|remember) the( lowercase| uppercase)? '
      '(value|text|html|outer html) of the page element "([^"]+)" as "([^"]+)"$')
def _this_step(step, upper_lower, what, element_name, name):
    ele_value = _get_attribute_of_element(element_name, what)
    store_with_case_option(name, ele_value, upper_lower)


def _get_attribute_of_element(element_name, attribute):
    page_element = get_visible_page_element(element_name)
    if attribute == 'text':
        return page_element.text
    elif attribute == 'outer html':
        return page_element.get_attribute('outerHTML')
    elif attribute == 'html':
        return page_element.get_attribute('innerHTML')
    else:
        return page_element.get_attribute(attribute)