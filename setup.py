from setuptools import setup
import find_packages
import sys
import os

version = '0.1'

setup(name='cruciverbalist',
      version=version,
      description="Generate crossword puzzles",
      long_description="""\
Generate crossword puzzles""",
      classifiers=[],
      keywords='',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
