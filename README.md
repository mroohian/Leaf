# Leaf
Page objects support for salad and lettuce testing framework


## Installation

Clone the repository and perform: 

    mkvirtualenv leaf.
    pip install -r leaf/pip_dependency.txt
    pip install -e leaf

## Example

Sample voting app tests tree structure is as follows:

    .
    ├── leaf (cloned from github)
    ├── voting
    │   ├── candidates.feature
    │   └── sources
    │       ├── steps.py
    │       └── terrain.py
    └── voting_pages
        ├── __init__.py
        ├── home_page.py
        └── master_layout.py

Let's create a sample feature file *candidates.feature*:

    Feature: voting app candidates page feature
    
      Scenario: check that the page loads currectly
        Given I visit the homepage
        
        When I look around
        
        Then I should be on the "home" page within 2 seconds

The content of the *terrain.py* is as follows:

    # -*- coding: utf-8 -*-
    
    from salad.terrains.everything import *
    import voting_pages
    
And the content of the *steps.py* is as follows:

    # -*- coding: utf-8 -*-
    
    from salad.steps.everything import *
    from leaf.steps.everything import *
    
Now we need to create the leaf page objects for the project. The sample app has a master layout 
and only a home page which inherits from the master layout.
 
The content of the *master_layout.py* is as follows:
 
     # -*- coding: utf-8 -*-
     
     from abc import abstractmethod
     from leaf import PageObject, element_by_id
     
     class MasterLayout(PageObject):
         @abstractmethod
         def __init__(self):
             pass
     
         @element_by_id('logo')
         def get_logo(self): pass
 
The content of the *home_page.py* is as follows:

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
        
Finally we need to configure **Leaf** to know about the app and pages in the *__init__.py*.

    # -*- coding: utf-8 -*-
    
    from leaf import leaf_world
    from home_page import HomePage
    
    leaf_world.base_url = 'http://127.0.0.1'
    
    leaf_world.available_pages.update({
        'home': HomePage
    })
    
## Executing Tests

Run the test suite using salad:

    salad voting
    
## Changelog

* 31-May-2015 initial version
