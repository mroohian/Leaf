# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from lettuce import step
from salad.logger import logger
from salad.exceptions import (
    TimeoutException,
    ElementDoesNotExist,
    ElementIsNotVisible,
    ElementAtIndexDoesNotExist
)
from salad.steps.browser import (
    visibility_test,
    PICK_EXPRESSION,
    ELEMENT_THING_STRING,
    contains_test, contains_exactly_test, attribute_test, attribute_value_test)
from salad.steps.browser.finders import ELEMENT_FINDERS
from salad.tests.util import parsed_negator
from salad.waiter import SaladWaiter
from leaf import get_visible_page_element
from leaf.steps.browser.finders import _get_visible_element_in_element

class StepFactory(object):
    def __init__(self, step_pattern, test_function):
        self._step_pattern = step_pattern + '(?: within (\d+) seconds)?$'
        self._test_function = test_function
        self._make_steps()

    def _make_steps(self):
        for finder_string, finder_function in ELEMENT_FINDERS.iteritems():
            self._make_step(finder_string, finder_function)

    def _make_step(self, finder_string, finder_function):
        pattern = self._step_pattern % (PICK_EXPRESSION, ELEMENT_THING_STRING, finder_string)

        @step(pattern)
        def _dynamic_step(step, negate, pick, find_pattern, parent_element_name, *args):
            wait_time = int(args[-1] or 0)
            args = args[:-1]  # Chop off the wait_time arg

            waiter = SaladWaiter(wait_time, ignored_exceptions=AssertionError)
            try:
                waiter.until(self._execute, negate, pick, find_pattern, finder_function, parent_element_name,
                             wait_time, *args)
            except TimeoutException as t:
                expression, func = step._get_match()
                logger.error(t.message)
                logger.error("Encountered error using definition '%s'" %
                             expression.re.pattern)
                message = ("Element not found or assertion failed after %s seconds" % wait_time)
                raise AssertionError(message)
            except Exception as error:
                # BEWARE: only way to get step regular expression
                expression, func = step._get_match()
                logger.error("%s" % error)
                logger.error("Encountered error using definition '%s'" %
                             expression.re.pattern)
                raise

    def _execute(self, negate, pick, find_pattern, finder_function, parent_element_name, wait_time, *args):
        try:
            element = _get_visible_element_in_element(parent_element_name, finder_function,
                                                      pick, find_pattern)
        except (ElementDoesNotExist, ElementIsNotVisible,
                ElementAtIndexDoesNotExist):
            assert parsed_negator(negate)
            element = None

        self._test_function(element, negate, *args)
        return True

visibility_pattern = (r'should( not)? see (?:the|a|an)%s %s %s'
                      ' inside the page element "([^"]+)"')

contains_pattern = (r'should( not)? see that the%s %s %s'
                    ' inside the page element "([^"]+)"'
                    ' (?:has|contains)(?: the text)? "([^"]*)"')
contains_exactly_pattern = (r'should( not)? see that the%s %s %s'
                            ' inside the page element "([^"]+)"'
                            ' (?:is|contains) exactly "([^"]*)"')
attribute_pattern = (r'should( not)? see that the%s %s %s'
                     ' inside the page element "([^"]+)"'
                     ' has (?:an|the) attribute (?:of|named|called) "(\w*)"')
attribute_value_pattern = (r'should( not)? see that the%s %s %s'
                           ' inside the page element "([^"]+)"'
                           ' has (?:an|the) attribute (?:of|named|called) '
                           '"([^"]*)" with(?: the)? value "([^"]*)"')
StepFactory(visibility_pattern, visibility_test)
StepFactory(contains_pattern, contains_test)
StepFactory(contains_exactly_pattern, contains_exactly_test)
StepFactory(attribute_pattern, attribute_test)
StepFactory(attribute_value_pattern, attribute_value_test)
