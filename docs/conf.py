import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import streamparser  # noqa: E402

project = 'Apertium Streamparser'
copyright = streamparser.__copyright__
author = streamparser.__author__

version = release = streamparser.__version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']

source_suffix = ['.rst']

master_doc = 'index'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

html_theme = 'alabaster'
html_static_path = ['_static']
htmlhelp_basename = 'ApertiumStreamparserdoc'

latex_documents = [
    (master_doc, 'ApertiumStreamparser.tex', 'Apertium Streamparser Documentation',
     streamparser.__author__, 'manual'),
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
