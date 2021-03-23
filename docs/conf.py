"""Sphinx configuration file."""

import geomstats


project = 'Geomstats'
copyright = '2019-2020, Geomstats, Inc.'
author = 'Geomstats Team'
release = version = geomstats.__version__

extensions = [
    'nbsphinx',
    'nbsphinx_link',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx_gallery.load_style',  # load CSS for gallery (needs SG >= 0.6)
    'sphinx.ext.viewcode',
    
]

# Configure napoleon for numpy docstring
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = False
napoleon_use_ivar = False
napoleon_use_rtype = False
napoleon_include_init_with_doc = False

# Configure nbsphinx for notebooks execution
nbsphinx_execute = 'never'
nbsphinx_allow_errors = True

# To get a prompt similar to the Classic Notebook, use
nbsphinx_input_prompt = ' In [%s]:'
nbsphinx_output_prompt = ' Out [%s]:'

# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = 'notebooks/' + env.doc2path(env.docname, base=None) %}

.. raw:: html

    <div class="admonition note">
      <p>Notebook source code:
        <a class="reference external" href="https://github.com/geomstats/geomstats/blob/master/notebooks>{{ docname|e }}</a>
        <br>Run it yourself on binder
        <a href="https://hub-binder.mybinder.ovh/user/geomstats-geomstats-hgpq7inb/notebooks/notebooks/01_data_on_manifolds.ipynb"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>
      </p>
    </div>

.. raw:: latex

    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from
    \sphinxcode{\sphinxupquote{\strut {{ docname | escape_latex }}}} \dotfill}}
"""


templates_path = ['_templates']

source_suffix = ['.rst', '.ipynb']

master_doc = 'index'

language = None

exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']

pygments_style = None

html_theme = 'sphinx_rtd_theme'
html_baseurl = 'geomstats.github.io'
htmlhelp_basename = 'geomstatsdoc'
html_last_updated_fmt = '%c'

latex_elements = {
}


latex_documents = [
    (master_doc, 'geomstats.tex', 'geomstats Documentation',
     'Geomstats Team', 'manual'),
]

man_pages = [
    (master_doc, 'geomstats', 'geomstats Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'geomstats', 'geomstats Documentation',
     author, 'geomstats', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project
epub_exclude_files = ['search.html']