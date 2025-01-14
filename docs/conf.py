# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Open edX Events'
copyright = '2023, Open edX Community'
author = 'Open edX Community'

# The full version, including alpha/beta/rc tags
release = 'latest'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib.contentui',
    'sphinx_copybutton',
    'sphinx.ext.graphviz',
    'sphinxcontrib.mermaid',
    'code_annotations.contrib.sphinx.extensions.openedx_events',
    'sphinx.ext.intersphinx',
    'code_annotations.contrib.sphinx.extensions.settings',
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_book_theme'

html_theme_options = {
    "repository_url": "https://github.com/openedx/openedx-events",
    "repository_branch": "main",
    "path_to_docs": "docs/",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "extra_footer": """
        <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
            <img
                alt="Creative Commons License"
                style="border-width:0"
                src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png">
        </a>
        <br>
        These works by
            <a
                xmlns:cc="https://creativecommons.org/ns#"
                href="https://openedx.org"
                property="cc:attributionName"
                rel="cc:attributionURL"
            >Axim Collaborative</a>
        are licensed under a
            <a
                rel="license"
                href="https://creativecommons.org/licenses/by-sa/4.0/"
            >Creative Commons Attribution-ShareAlike 4.0 International License</a>.
    """
}

# Note the logo won't show up properly yet because there is an upstream
# bug in the theme that needs to be fixed first.
# If you'd like you can temporarily copy the logo file to your `_static`
# directory.
html_logo = "https://logos.openedx.org/open-edx-logo-color.png"
html_favicon = "https://logos.openedx.org/open-edx-favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Read the Docs Specific Configuration
# Define the canonical URL if you are using a custom domain on Read the Docs
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    if "html_context" not in globals():
        html_context = {}
    html_context["READTHEDOCS"] = True

# -- Extension configuration -------------------------------------------------

# Intersphinx Extension Configuration
DIGITS_ONLY = r"^\d+$"
rtd_language = os.environ.get("READTHEDOCS_LANGUAGE", "en")
rtd_version = os.environ.get("READTHEDOCS_VERSION", "latest")
if re.search(DIGITS_ONLY, rtd_version):
    # This is a PR build, use the latest versions of the other repos.
    rtd_version = "latest"

intersphinx_mapping = {
    "docs.openedx.org": (
        f"https://docs.openedx.org/{rtd_language}/{rtd_version}",
        None,
    ),
    "openedx-proposals": (
        # Not setting the version on purpose because we always want the latest version
        # of OEPs
        f"https://docs.openedx.org/projects/openedx-proposals/{rtd_language}/latest",
        None,
    ),
}
