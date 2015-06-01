# -*- coding: utf-8 -*-

from abc import abstractmethod
from leaf import PageObject, element_by_id

class MasterLayout(PageObject):
    @abstractmethod
    def __init__(self):
        pass

    @element_by_id('logo')
    def get_logo(self): pass    