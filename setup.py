try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='tweetvote',
    version='0.1',
    description='A generic tweet vote counter',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://pudo.org/',
    install_requires=[
        "Pylons>=0.9.7rc6",
        "SQLAlchemy>=0.4",
        "python-twitter>=0.5",
        "FormEncode>=1.2.1",
        "feedparser>=4.1",
        "BeautifulSoup>=3.1",
        "python-memcached>=1.43",
        "simplejson>=2.0.9"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'tweetvote': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'tweetvote': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = tweetvote.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
