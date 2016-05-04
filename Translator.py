# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 21:07:39 2016

@author: josh
"""

import ImageCreator
from ImageCreator import Modifications
from copy import deepcopy
import sys

def makeShape(shapeType, modificationsList):
    if shapeType == "Rectangle":
        shape = ImageCreator.Rectangle()
    elif shapeType == "Ellipse":
        shape = ImageCreator.Ellipse()
    elif shapeType == "Triangle":
        shape = ImageCreator.Triangle()
    else:
        print "Invalid shape type: %s" % shapeType
        sys.exit()
    
    
    modDict = dict(modificationsList)
    keys = modDict.keys()
    for key in keys:
        if key not in ["x", "y", "width", "height", "size", "s", "rotation", \
        "r", "alpha", "a", "hue", "h", "saturation", "sat", "brightness", "b"]:
            print "Invalid shape attribute: %s" % key
            sys.exit()
    if "x" in keys:
        shape.x = float(modDict['x'])
    if "y" in keys:
        shape.y = float(modDict['y'])
    if "width" in keys:
        shape.width = float(modDict['width'])
    if "height" in keys:
        shape.height = float(modDict['height'])
    if "s" in keys:
        # Allows things like equilateral triangles to be preserved.
        shape.width *= float(modDict['s'])
        shape.height *= float(modDict['s'])
    if "size" in keys:
        # Allows things like equilateral triangles to be preserved.
        shape.width *= float(modDict['size'])
        shape.height *= float(modDict['size'])
    if "r" in keys:
        shape.rotation = float(modDict['r'])
    if "rotation" in keys:
        shape.rotation = float(modDict['rotation'])
    if "a" in keys:
        shape.alpha = float(modDict['a'])
    if "alpha" in keys:
        shape.alpha = float(modDict['alpha'])
    if "h" in keys:
        shape.fill[0] = float(modDict['h'])
    if "hue" in keys:
        shape.fill[0] = float(modDict['hue'])
    if "sat" in keys:
        shape.fill[1] = float(modDict['sat'])
    if "saturation" in keys:
        shape.fill[1] = float(modDict['saturation'])
    if "b" in keys:
        shape.fill[2] = float(modDict['b'])
    if "brightness" in keys:
        shape.fill[2] = float(modDict['brightness'])
    
    return shape


def translateModifications(modificationsList):
    result = Modifications()
    #translate, rotate, scale, scalex, scaley, changehue,
    #changesaturation, changebrightness, changealpha, delay
    for modification in modificationsList:
        # We essentially need to do a big case-switch here for what kind it is.
        # We don't want to do this as a dict because order can matter.
        if modification[0] in ["translate", "t"]:
            result = result + Modifications.Translate(float(modification[1]), float(modification[2]))
        elif modification[0] in ["absoluteTranslate", "at"]:
            result = result + Modifications.AbsoluteTranslate(float(modification[1]), float(modification[2]))  
        elif modification[0] in ["scaleTranslate", "st"]:
            result = result + Modifications.ScaleTranslate(float(modification[1]), float(modification[2]))
        elif modification[0] in ["rotate", "r"]:
            result = result + Modifications.Rotate(float(modification[1]))
        elif modification[0] in ["scale", "s"]:
            result = result + Modifications.Scale(float(modification[1]))
        elif modification[0] == "scaleX":
            result = result + Modifications.ScaleX(float(modification[1]))
        elif modification[0] == "scaleY":
            result = result + Modifications.ScaleY(float(modification[1]))
        elif modification[0] in ["hue", "h"]:
            result = result + Modifications.ChangeHue(int(modification[1]))
        elif modification[0] in ["saturation", "sat"]:
            result = result + Modifications.ChangeSaturation(float(modification[1]))
        elif modification[0] in ["brightness", "b"]:
            result = result + Modifications.ChangeBrightness(float(modification[1]))
        elif modification[0] in ["alpha", "a"]:
            result = result + Modifications.ChangeAlpha(float(modification[1]))
        elif modification[0] in ["delay", "d"]:
            result = result + Modifications.Delay(int(modification[1]))   
        elif modification[0] in ["delayStart", "ds"]:
            result = result + Modifications.DelayStart(int(modification[1]))   
        else:
            print "Invalid modification: %s." % modification[0]
            sys.exit()
    return result

"""
Takes a syntax tree generated by Parser and translates it into the
language of ImageCreator.
"""
def translate(AST):
    animationName, canvasWidth, canvasHeight, filetype, duration, framerate, defaultLimit, shapes, primitives, rules, limits, startTimes = AST
    
    # Create shapes.
    shapeDict = {}
    for shape in shapes:
        name, shapeType, modifications = shape
        shapeDict[name] = makeShape(shapeType, modifications)
        
    # Create animation primitives (Elements).
    elemDict = {}
    for primitive in primitives:
        exp = False
        if len(primitive) == 3:
            exp = True
            primitive = primitive[:-1]
        name, frames = primitive
        frameList = []
        for frameSpecification in frames:
            firstFrame, firstFrameModifications = frameSpecification[:2]
            firstFrame = deepcopy(shapeDict[firstFrame])
            firstFrameShape = translateModifications(
                    firstFrameModifications).modifyShape(firstFrame)
            frameList.append(firstFrameShape)
            if len(frameSpecification) > 2:
                nextFrameShape = firstFrameShape
                loops, newModifications = frameSpecification[2:4]
                translatedModifications = translateModifications(newModifications)
                for i in xrange(int(loops)):
                    nextFrameShape = deepcopy(nextFrameShape)
                    translatedModifications.modifyShape(nextFrameShape)
                    frameList.append(nextFrameShape)
        elemDict[name] = ImageCreator.Element(frameList, expires = exp)
    
    # Make a quick limit dictionary and start time dictionary.
    limitsByName = {}
    for limit in limits:
        limitsByName[limit[0]] = int(limit[1])
        
    startTimesByName = {}
    for time in startTimes:
        startTimesByName[time[0]] = int(time[1])
    
    # Create a rule dictionary. 
    rulesByName = {}
    for rule in rules:
        if len(rule) == 2:
            prob = 1
            name, executionRules = rule
            #put in defaults for these two dictionaries.
            if not limitsByName.has_key(name):
                limitsByName[name] = int(defaultLimit)
            if not startTimesByName.has_key(name):
                startTimesByName[name] = 0
        else:
            prob, name, executionRules = rule
        for i in xrange(len(executionRules)):
            step = executionRules[i]
            # We need to change any element names to elements.
            # we can leave rule names alone.
            if step[0] in elemDict.keys():
                executionRules[i] = (elemDict[step[0]], translateModifications(step[1]))
            else:
                executionRules[i] = (step[0], translateModifications(step[1]))
        if rulesByName.has_key(name):
            rulesByName[name].append([float(prob)] + executionRules)
        else:
            rulesByName[name] = [[float(prob)] + executionRules]
            
            
    ruleMaker = lambda (name, execrules): ImageCreator.Rule(
            name, execrules, limitsByName[name], startTimesByName[name])
    ruleDict = ImageCreator.RuleDict(map (ruleMaker, rulesByName.items()))
    ruleDict.initialRule = ruleDict.rules[rules[0][0]]
    print "Executing rules."
    creator = ImageCreator.ImageCreator(int(canvasWidth), int(canvasHeight), ruleDict.chooseAndExecuteRule(startFrame = startTimesByName[rules[0][0]]), animationName, int(duration))


    
    creator.renderAnimation(filetype, framerate)
        
                    
                    
        