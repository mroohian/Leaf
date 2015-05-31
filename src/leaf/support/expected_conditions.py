# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from leaf import get_page_element

# based on class:
# selenium.webdriver.support.expected_conditions.element_located_selection_state_to_be
class page_element_selection_state_to_be(object):
    """ An expectation to locate a page element and check if the selection state
    specified is in that state.
    element_name is the name of page element
    is_selected is a boolean
    """
    def __init__(self, element_name, is_selected):
        self.element_name = element_name
        self.is_selected = is_selected

    def __call__(self, driver):
        try:
            element = get_page_element(self.element_name)
            return element.is_selected() == self.is_selected
        except StaleElementReferenceException:
            return False

# based on class:
# selenium.webdriver.support.expected_conditions.presence_of_element_located
class presence_of_page_element(object):
    """ An expectation for checking that a page element is present on the DOM
    of a page. This does not necessarily mean that the element is visible.
    element_name is the name of page element
    returns the WebElement once it is located
    """
    def __init__(self, element_name):
        self.element_name = element_name

    def __call__(self, driver):
        return get_page_element(self.element_name)

# based on class:
# selenium.webdriver.support.expected_conditions.visibility_of_element_located
class visibility_of_page_element(object):
    """ An expectation for checking that a page element is present on the DOM of a
    page and visible. Visibility means that the page element is not only displayed
    but also has a height and width that is greater than 0.
    element_name is the name of page element
    returns the WebElement once it is located and visible
    """
    def __init__(self, element_name):
        self.element_name = element_name

    def __call__(self, driver):
        try:
            return EC._element_if_visible(get_page_element(self.element_name))
        except StaleElementReferenceException:
            return False

# based on class:
# selenium.webdriver.support.expected_conditions.element_to_be_clickable
# TODO: report documentation bug to selenium
class page_element_to_be_clickable(object):
    """ An Expectation for checking a page element is visible and enabled such that
    you can click it.
    element_name is the name of page element
    returns the WebElement once it is located and clickable
    """
    def __init__(self, element_name):
        self.element_name = element_name

    def __call__(self, driver):
        element = visibility_of_page_element(self.element_name)(driver)
        if element and element.is_enabled():
            return element
        else:
            return False

# based on class:
# selenium.webdriver.support.expected_conditions.invisibility_of_element_located
# TODO: report documentation bug to selenium
class invisibility_of_page_element(object):
    """ An Expectation for checking that a page element is either invisible or not
    present on the DOM.

    element_name is the name of page element
    returns True once it is not visible
    """
    def __init__(self, element_name):
        self.element_name = element_name

    def __call__(self, driver):
        try:
            return not get_page_element(self.element_name).is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            # In the case of NoSuchElement, returns true because the element is
            # not present in DOM. The try block checks if the element is present
            # but is invisible.
            # In the case of StaleElementReference, returns true because stale
            # element reference implies that element is no longer visible.
            return True

# based on class:
# selenium.webdriver.support.expected_conditions.text_to_be_present_in_element
# TODO: report documentation bug to selenium
class text_to_be_present_in_page_element(object):
    """ An expectation for checking if the given text is present in the
    specified page element.
    element_name is the name of page element
    text
    """
    def __init__(self, element_name, text_):
        self.element_name = element_name
        self.text = text_

    def __call__(self, driver):
        try :
            element_text = get_page_element(self.element_name).text
            return self.text in element_text
        except StaleElementReferenceException:
            return False

# based on class:
# selenium.webdriver.support.expected_conditions.text_to_be_present_in_element_value
# TODO: report documentation bug to selenium
class text_to_be_present_in_page_element_value(object):
    """
    An expectation for checking if the given text is present in the page element's
    element_name is the name of page element
    text
    """
    def __init__(self, element_name, text_):
        self.element_name = element_name
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = get_page_element(self.element_name).get_attribute("value")
            if element_text:
                return self.text in element_text
            else:
                return False
        except StaleElementReferenceException:
                return False


# based on class:
# selenium.webdriver.support.expected_conditions.

# based on class:
# selenium.webdriver.support.expected_conditions.