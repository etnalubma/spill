#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='spill',
    version='0.8dev',
    author=u'Francisco Herrero',
    author_email='francisco.herrero@gmail.com',
    url='http://github.com/etnalubma/spill',
    description = 'Herramienta de linea de comandos apra publicar en ltmo',
    entry_points = {
        'console_scripts': [
            'spill = spill.scripts:do_spill',
        ],
    }

)

