# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from lettuce import step, world
from salad.logger import logger
from salad.tests.util import wait_for_completion, assert_with_negate
from leaf import leaf_world

def open_page(page_url):
    if leaf_world.base_url is None:
        raise ValueError('leaf_world.base_url is not set.')
    world.browser.visit(leaf_world.base_url + page_url)

def get_page_url(url):
    return url[len(leaf_world.base_url):]

def create_page_object(page):
    # Check if already created
    if page in leaf_world.pages:
        return leaf_world.pages[page]

    if page not in leaf_world.available_pages:
        raise KeyError('"%s" page is undefined.' % page)

    try:
        page_class = leaf_world.available_pages[page]
    except KeyError:
        logger.error(' "%s" page is undefined.' % page)
        return None

    page_object = page_class()

    leaf_world.pages.update({
        page: page_object
    })

    return page_object

def _check_is_on_page(page, negate):
    if page not in leaf_world.available_pages:
        raise KeyError('"%s" page is undefined.' % page)

    if page not in leaf_world.pages:
        try:
            page_object = create_page_object(page)
        except KeyError:
            raise
    else:
        page_object = leaf_world.pages[page]

    is_on_page = page_object.is_current(world.browser.url, get_page_url(world.browser.url))

    assert_with_negate(is_on_page, negate)

    leaf_world.current_page = page_object

@step(r'(?:visit|access|open) the "([^"]+)" page(?: with args ([^$]+))?$')
def visit_page(step, page, args):
    if args is not None:
        arg_segments = args.split()

        args = {}
        for arg in arg_segments:
            try:
                [key, value] = arg.split(':')
                args[key] = value
            except ValueError, e:
                raise ValueError('Parameters must have key:value format.\nBase Error: ' + e.message)

    page_object = create_page_object(page)
    assert page_object is not None
    leaf_world.current_page = page_object
    open_page(page_object.get_url(**args))

@step(r'(?:visit|access|open) the homepage(?: with args ([^$]+))?$')
def visit_homepage(step, args):
    visit_page(step, 'home', args)

@step(r'should( not)? be on the "([^"]+)" page(?: within (\d+) seconds)?$')
@step(r'should( not)? see that current page is "([^"]+)"(?: within (\d+) seconds)?')
@step(r'should( not)? expect to navigate to "([^"]+)" page(?: within (\d+) seconds)?')
def should_be_in_page(step, negate, page, wait_time):
    def _assert_on_page():
        _check_is_on_page(page, negate)
        return True

    wait_for_completion(wait_time, _assert_on_page)