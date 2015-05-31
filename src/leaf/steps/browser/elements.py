# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from lettuce import step
from leaf import get_visible_page_element

from salad.logger import logger
from salad.waiter import SaladWaiter, TimeoutException

from salad.steps.browser.elements import (
    visibility_test,
    contains_test,
    contains_exactly_test,
    attribute_test,
    attribute_value_test
)

class StepFactory(object):
    def __init__(self, step_pattern, test_function):
        self._step_pattern = step_pattern + '(?: within (\d+) seconds)?$'
        self._test_function = test_function
        self._make_step()

    def _make_step(self):
        @step(self._step_pattern)
        def _dynamic_step(step, negate, element_name, *args):
            wait_time = int(args[-1] or 0)
            args = args[:-1]  # Chop off the wait_time arg

            waiter = SaladWaiter(wait_time, ignored_exceptions=AssertionError)
            try:
                waiter.until(self._execute, negate, element_name,
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

    def _execute(self, negate, element_name, wait_time, *args):
        page_element = get_visible_page_element(element_name)
        self._test_function(page_element, negate, *args)
        return True

visibility_pattern = r'should( not)? see (?:the|a) page element "([^"]+)"'
contains_pattern = (r'should( not)? see that the page element "([^"]+)" (?:has|contains)'
                    '(?: the text)? "([^"]*)"')
contains_exactly_pattern = (r'should( not)? see that the page element "([^"]+)" '
                            '(?:is|contains) exactly "([^"]*)"')
attribute_pattern = (r'should( not)? see that the page element "([^"]+)" has (?:an|the) '
                     'attribute (?:of|named|called) "(\w*)"')
attribute_value_pattern = (r'should( not)? see that the page element "([^"]+)" has '
                           '(?:an|the) attribute (?:of|named|called) '
                           '"([^"]*)" with(?: the)? value "([^"]*)"')

StepFactory(visibility_pattern, visibility_test)
StepFactory(contains_pattern, contains_test)
StepFactory(contains_exactly_pattern, contains_exactly_test)
StepFactory(attribute_pattern, attribute_test)
StepFactory(attribute_value_pattern, attribute_value_test)
