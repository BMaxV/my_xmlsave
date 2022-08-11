import os
import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

setuptools.setup(
    name = "my_save_function",
    version = "0.1",
    author = "Brumo Maximilian Voss",
    author_email = "bruno.m.voss@gmail.com",
    description = ("dump and load simple python data types to xml"),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    license = "MIT",
)
