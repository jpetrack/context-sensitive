# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 17:14:16 2016

@author: josh
"""

from parcon import number, ZeroOrMore, Literal, SignificantLiteral, alpha_word, alphanum_word, Optional, rational

# METADATA
metadata = "Name:" + alphanum_word + "Canvas:" + number + "x" + number + "Format:" + alphanum_word + "Frames:" + number + "Framerate:" + number + "Default Depth Limit:" + number


# MODIFICATIONS & SPECIFICATIONS (can use same kind of syntax)
modification = alpha_word + ":" + (rational | "(" + number + "," + number + ")")
modifications = "{" + ZeroOrMore(modification) + "}"


# SHAPES
basicShapeName = SignificantLiteral("Rectangle") |\
                 SignificantLiteral("Ellipse") |\
                 SignificantLiteral("Triangle")
shape = alphanum_word + ":" + basicShapeName + modifications
shapes = "Shapes:" + ZeroOrMore(shape)

# PRIMITIVES

basicFrame = alphanum_word + modifications
framesGenerator = "(" + number + "times)" + modifications
framesDescription = basicFrame + Optional(framesGenerator)
primitive = alphanum_word + "{" + ZeroOrMore(framesDescription) + "}"
primitives = "Primitives:" + ZeroOrMore(primitive)


# RULES
ruleStep = alphanum_word + modifications
rule = Optional(rational) + alphanum_word + "{" + ZeroOrMore(ruleStep) + "}"
rules = "Rules:" + ZeroOrMore(rule)

# LIMITS
limit = alphanum_word + ":" + number
limits = Optional(Literal("Limits:")) + ZeroOrMore(limit)

# START TIMES
starttime = alphanum_word + ":" + number
starttimes = Optional(Literal("Start times:")) + ZeroOrMore(starttime)

def parse(text):
    # Allow the user to type .5 instead of 0.5.
    text = text.replace(" .", " 0.")
    text = text.replace("-.", "-0.")
    text = text.replace(":.", ":0.")
    return (metadata + shapes + primitives + rules + limits + starttimes).parse_string(text)