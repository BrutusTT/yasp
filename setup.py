####################################################################################################
#    Copyright (C) 2016-2017 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
#                                                                                                  #
#    This file is part of YASP (Yet Another Speech Package).                                       #
#                                                                                                  #
#    YASP is free software: you can redistribute it and/or modify it under the terms of the        #
#    GNU Affero General Public License as published by the Free Software Foundation, either        #
#    version 3 of the License, or (at your option) any later version.                              #
#                                                                                                  #
#    YASP is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;             #
#    without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.     #
#    See the GNU Affero General Public License for more details.                                   #
#                                                                                                  #
#    You should have received a copy of the GNU Affero General Public License                      #
#    along with YASP.  If not, see <http://www.gnu.org/licenses/>.                                 #
####################################################################################################
import os

from setuptools import setup, find_packages

version = open(os.path.join("yasp", "version.txt")).read().strip()

setup( name                 = 'YASP',
       version              = version,
       description          = "Yet Another Speech Package",
       long_description     = open("README.md").read(),
       # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
       classifiers          = [
         "Programming Language :: Python",
         "Topic :: Software Development :: Libraries :: Python Modules",
         ],
       keywords             = '',
       author               = 'Ingo Keller',
       author_email         = 'brutusthetschiepel@gmail.com',
       url                  = '',
       license              = 'AGPL v3',
       packages             = find_packages(exclude=['ez_setup']),
       namespace_packages   = [],
       include_package_data = True,
       zip_safe             = False,
       install_requires     = [
           'setuptools',
           # -*- Extra requirements: -*-
           'numpy',
           'pyaudio'
       ],
       entry_points         = """
       # -*- Entry points: -*-
       """,

       scripts = [
           'scripts/MSpeak',
           'scripts/MaryTTS',
           'scripts/startMary.sh',
           'scripts/stopMary.sh',
       ]
     )
