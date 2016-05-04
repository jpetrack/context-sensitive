
[notebook-fork]: https://github.com/hmc-cs111-spring2016/project-notebook/fork
[CS111-projects]: https://github.com/hmc-cs111-spring2016/hmc-cs111-spring2016.github.io/wiki/Project-links

[Description]: documents/description.md
[Plan]: documents/plan.md
[DesignAndImplementation]: documents/design_and_implementation.md
[Final]: documents/final.md

# ContextSensitive

## Overview

ContextSensitive is a language for creating abstract animations built up from small primitive animations, which are in turn built up from basic shapes. The user defines shapes, uses those shapes to define primitive animations in which each frame is a shape, and then defines rules that render those primitives or call other rules (or themselves).

## Running the language

To run a program in the language, there are a few dependencies: 
* Python 2.7 must be installed.
* The Parcon library is used for parsing within Python. It can be installed with pip or easy_install, i.e. `pip install parcon` or `easy_install parcon` from the command line. 
* PIL, the Python Imaging Library, is used for back-end image generation. Unfortunately PIL is actually deprecated (which I did not realize when I was using it), and so cannot be installed with easy_install or pip. To install it, download the [source code](http://www.pythonware.com/products/pil/#pil117), go to the folder that it installs, and run `python setup.py install`. Additionally this will not work if Pillow (the more recent undeprecated version of PIL) is installed; if Pillow is installed it must be first uninstalled with `pip uninstall Pillow` before running setup.py. This will hopefully change in a future version of the language.
* [FFmpeg](https://ffmpeg.org/) is required for anything other than rendering individual frames. An FFmpeg executable can be downloaded from their site; it is not included here as I'm not completely certain that I'm legally allowed to. The executable should be placed in the same directory as the source code files and program file. If the executable is not included, the program will default to generating individual frames.

Place the source code for ContextSensitive, the ffmpeg executable, and the source code for your program in the same directory. Then simply run `python main.py sourcecode.txt` where sourcecode.txt is the name of your ContextSensitive program file.