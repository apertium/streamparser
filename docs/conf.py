import os
import sys

sys.path.insert(0, os.path.abspath('..'))


project = 'Apertium Streamparser'
copyright = '2016--2018, Sushain K. Cherivirala, Kevin Brubeck Unhammer'
author = 'Sushain K. Cherivirala, Kevin Brubeck Unhammer'

version = '5.0.2'
release = '5.0.2'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']

source_suffix = ['.rst']

# The master toctree document.
master_doc = 'index'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

html_theme = 'alabaster'
html_theme_options = {
    'github_user': 'apertium',
    'github_repo': 'streamparser',
    'travis_button': True,
    'github_button': True,
}
html_static_path = ['_static']
htmlhelp_basename = 'ApertiumStreamparserdoc'


latex_elements = {}

latex_documents = [
    (master_doc, 'ApertiumStreamparser.tex', 'Apertium Streamparser Documentation',
     'Sushain K. Cherivirala, Kevin Brubeck Unhammer', 'manual'),
]

man_pages = [
    (master_doc, 'apertiumstreamparser', 'Apertium Streamparser Documentation',
     [author], 1),
]

texinfo_documents = [
    (master_doc, 'ApertiumStreamparser', 'Apertium Streamparser Documentation',
     author, 'ApertiumStreamparser', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
