# -*- coding: utf-8 -*-

__author__ = 'mroohian'
__version__ = '0.1'

import threading
from page_object import PageObject
from salad.steps.browser.finders import _get_element

# #### global info ######
leaf_world = threading.local()
leaf_world.base_url = None
leaf_world.available_pages = {}
leaf_world.pages = {}
leaf_world.current_page = None

# #### public utility function ####
def get_page_element(element_name):
    element = leaf_world.current_page.get_element(element_name)
    assert element is not None
    return element


def get_visible_page_element(element_name):
    element = leaf_world.current_page.get_visible_element(element_name)
    assert element is not None
    return element

# #### get element decorators ######
def _get_element_wrapper_decorator(pattern, finder_function):
    def func_decorator(scope):
        def get_element(self):
            element = _get_element(finder_function, None, pattern)

            assert element is not None

            return element

        return get_element

    return func_decorator

def element_by_name(name):
    return _get_element_wrapper_decorator(name, 'find_by_name')


def element_by_id(id):
    return _get_element_wrapper_decorator(id, 'find_by_id')


def element_by_css(selector):
    return _get_element_wrapper_decorator(selector, 'find_by_css')


def element_by_xpath(query):
    return _get_element_wrapper_decorator(query, 'find_by_xpath')


def element_by_tag(selector):
    return _get_element_wrapper_decorator(selector, 'find_by_tag')


def link_by_text(selector):
    return _get_element_wrapper_decorator(selector, 'find_link_by_text')


def link_by_partial_text(selector):
    return _get_element_wrapper_decorator(selector, 'find_link_by_partial_text')
