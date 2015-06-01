# -*- coding: utf-8 -*-

from leaf import element_by_css
from master_layout import MasterLayout

class HomePage(MasterLayout):
    def __init__(self):
        pass
        
    def get_url(self):
        return '/'
        
    def is_current(self, url, page_url):
        if page_url == '/' or page_url == '/content/home':
            return True
        return False
        
    @element_by_css('div.header')
    def get_header(self): pass    