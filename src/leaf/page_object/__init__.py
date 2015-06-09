# -*- coding: utf-8 -*-

__author__ = 'mroohian'

from abc import ABCMeta, abstractmethod
from salad.exceptions import ElementIsNotVisible
from salad.logger import logger

class PageObject:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_url(self, **args):
        raise NotImplemented(' get_url is undefined in page %s' % self.__class__.__name__)

    @abstractmethod
    def is_current(self, url, page_url):
        raise NotImplemented(' is_current is undefined in page %s' % self.__class__.__name__)

    def get_element(self, element_name):
        func_name = 'get_' + element_name
        try:
            func = getattr(self, func_name)
        # check if function exists
        except AttributeError:
            return None

        # TODO: make sure function doesn't throw an error
        element = func()

        # make sure element is not null
        if element is None:
            logger.warn(' %s element could not be found in page %s' % (element_name, self.__class__.__name__))

        return element

    def get_visible_element(self, element_name):
        element = self.get_element(element_name)
        if not element:
            raise ValueError('"%s" element could not be found in page %s' % (element_name, self.__class__.__name__))
        if not element.is_displayed():
            raise ElementIsNotVisible("The page element exist, but it is not visible. "
                                      "page element: %s, page: %s" %
                                      (element_name, self.__class__.__name__))
        return element

