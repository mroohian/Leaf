# -*- coding: utf-8 -*-

from leaf import leaf_world
from home_page import HomePage

leaf_world.base_url = 'http://127.0.0.1'

leaf_world.available_pages.update({
    'home': HomePage
})