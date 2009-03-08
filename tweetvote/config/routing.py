"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE    
    
    # don't like map.resource, DIY
    map.connect('/votes.{format}', controller='votes', action='index')
    map.connect('/votes', controller='votes', action='index', format='html')
    
    map.connect('/votes/{id}.{format}', controller='votes', action='vote_dispatch')
    map.connect('/votes/{id}', controller='votes', action='vote_dispatch', format='html')
    
    map.connect('/search', controller='search', action='index')
    map.connect('/search/add', controller='search', action='add')
    map.connect('/search/del', controller='search', action='delete')
    
    map.connect('/', controller='system', action='index')
    map.connect('', controller='system', action='index')

    map.connect('/classify', controller='twitterator', action='index')

    map.connect('/faq.doc', controller='system', action='faq')
    map.connect('/api.doc', controller='system', action='api')
    map.connect('/login', controller='system', action='login')
    map.connect('/logout', controller='system', action='logout')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
