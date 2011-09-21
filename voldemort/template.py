#! /usr/bin/env python
#
# Jinja2 Template engine
#
# @author: Sreejith K
# Created On 19th Sep 2011


import os

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


# template's environment
env = Environment()


def get_rendered_page(filename):
    """ Obtain the rendered template including the exported 
    macros and variables .
    """
    page = {}
    with open(filename, 'r') as f:
        content = f.read()
        template = env.from_string(content)
        for attr in dir(template.module):
            if not attr.startswith('_'):
                page[attr] = getattr(template.module, attr)
        page['content'] = template.render()
        page['filename'] = os.path.basename(filename)
    return page


def setup_template_dirs(root_dir):
    """ Add search paths to template environment.
    """
    template_dirs = [root_dir]
    for dir in os.listdir(root_dir):
        if dir.startswith('_') or dir.endswith('~'):
            continue
        dir = os.path.join(root_dir, dir)
        if os.path.isdir(dir):
            template_dirs.append(dir)
    env.loader = FileSystemLoader(template_dirs)


def render(template, values):
    """ Render Jinja2 templates.
    """
    tmpl = env.get_template(template)
    return tmpl.render(values)