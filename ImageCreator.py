# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:13:19 2016

@author: josh
"""
from PIL import Image, ImageDraw
from copy import deepcopy
from random import random
class ImageCreator:
    """
    An ImageCreator is essentially a list of all of the Elements in an image.
    It keeps track of what frame the animation is currently in, and is in
    charge of rendering each frame of the final animation.
    """
    def __init__(self, width = 800, height = 600, elems = [], outputpath = "", totalFrames = 20):
        self.width = width
        self.height = height
        self.elements = elems
        self.frame = 0
        self.outputpath = outputpath
        self.totalFrames = totalFrames
        
        
    def renderFrame(self, image, draw):
        """Renders a single frame of animation"""
        for elem in self.elements:
            elem.drawFrame(image, draw)
            elem.incrementFrame()
            
        
    def renderAnimation(self):
        for i in xrange(self.totalFrames):
            im = Image.new("RGBA", (self.width, self.height), "white")
            draw = ImageDraw.Draw(im)
            self.renderFrame(im, draw)
            im.save(self.outputpath + "%05d" % self.frame + ".png", "PNG")
            self.frame += 1
        

class RuleDict:
    """
    A RuleDict is a wrapper that knows all of the rules that the user has
    defined, so that it can run the initial rule and then make any other
    rule calls that the initial rule says it needs to make.
    """
    def __init__(self, rules):
        self.rules = {}
        for rule in rules:
            self.rules[rule.name] = rule.executionRules
        self.initialRule = rules[0].executionRules
        
    def chooseAndExecuteRule(self, executionRules = 0, existingModifications = [], remainingDepthLimit = 20):
        if remainingDepthLimit == 0:
            return []
        if executionRules == 0:
            executionRules = self.initialRule
        choice = random()
        sumProb = 0
        chosenRule = None
        for rule in executionRules:
            sumProb += rule[0]
            if sumProb > choice:
                chosenRule = rule[1:]
                break
        #handles possible floating point errors
        if chosenRule is None:
            chosenRule = executionRules[0][1:]
        resultElements = []
        for action in chosenRule:
            (thing, modifications) = action
            if type(thing) == type(""):
                # it's a rule name
                nextRule = self.rules[thing]
                resultElements += self.chooseAndExecuteRule(nextRule,
                                                       existingModifications + modifications, 
                                                       remainingDepthLimit - 1)
            else:
                resultElements.append(thing.modify(existingModifications))
        return resultElements

    
class Rule:
    """
    A rule tells us to create an element or set of elements, and then execute
    another rule or rules, all potentially with modifications. 
    A rule may be nondeterministic, i.e., have several possible
    sub-rules one of which is randomly chosen at runtime when the rule is
    executed. A rule might correspond to someone writing a program saying 
    "to make a caterpillar, make a circle and then make another caterpillar
    shifted to the right by 10 and scaled by .9".
    """
    def __init__(self, name, executionRules):
        self.name = name
        
        # Each execution rule is of the form:
        # [p, (r, m), (r, m) ..., (r, m)]
        # where p is a probability proportion (not actually a probability until we normalize), 
        # each r is either a Rule or an Element, and each m is a modification
        # list.
        # executionRules is a list of these.
        self.executionRules = executionRules
        totalProbability = sum([x[0] for x in self.executionRules])
        self.executionRules = map(lambda k: [(k[0] / float(totalProbability))] + k[1:], self.executionRules)
    


class Element:
    """
    An Element is a single shape or animation. It should know what frame it's
    on, how to display itself, and how to modify itself for the sake of
    recursively creating more copies of itself.
    """
    
    def __init__(self, frameList, currentFrame = 0):
        self.frameList = frameList
        self.currentFrame = 0
        self.totalFrames = len(frameList)
        
    def incrementFrame(self):
        self.currentFrame = (self.currentFrame + 1) % self.totalFrames
    def drawFrame(self, image, draw):
        self.frameList[self.currentFrame].render(image, draw)
        
        
    def modify(self, modifications):
        """
        Applies some modification (like scaling, changing hue, etc) to all
        frames of the animation.
        """
        newElem = Element(map(lambda k: k.withModifications(modifications), self.frameList), 0)
        newElem.currentFrame = (self.currentFrame + sum(map(lambda k: int(k.split(' ')[-1]), 
                          filter(lambda k: k[0:5] == "delay", modifications)))) % self.totalFrames
        return newElem
        
    
class Shape(object):
    
    def __init__(self):
        self.fill = [0, 100, 50]
        self.scale = 1
        self.x = 0
        self.y = 0
        self.rotation = 0

    
    def render(self, image, draw):    
        pass
    
    def withModifications(self, modifications):
        """
        Modifications should be an ordered list of modifications to apply.
        Those modifications can take the following forms:
        "changehue x" increases the hue by x
        "sethue x" sets the hue to x
        "scale x" multiplies the scale by x
        "translate x y" translates by the tuple (x, y)
        "rotate x" rotates by x degrees
        "delay x" delays the animation by x frames
        """
        newShape = deepcopy(self)
        for modification in modifications:
            desc = modification.split(" ")
            if desc[0] == "changehue":
                newShape.fill[0] += int(desc[1])
            if desc[0] == "sethue":
                newShape.fill[0] = int(desc[1])
            if desc[0] == "scale":
                newShape.scale *= float(desc[1])
            if desc[0] == "translate":
                newShape.x += float(desc[1])
                newShape.y += float(desc[2])
            if desc[0] == "rtranslate":
                # Relative translate. Translate relative to scale.
                newShape.x += float(desc[1]) * newShape.scale
                newShape.y += float(desc[2]) * newShape.scale
            if desc[0] == "rotate":
                newShape.rotation += float(desc[1])
            if desc[0] == "delay":
                # Handled at the element level.
                pass
        return newShape

class Rectangle(Shape):
    """
    A Rectangle primitive. (x, y) is the rectangle's center.
    """
    def __init__(self, x, y, width, height):
        super(Rectangle, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def render(self, image, draw):
        
        width = self.width * self.scale
        height = self.height * self.scale
        
        newRect = Image.new("RGB", (int(width), int(height)), 'hsl(%d, %d%%, %d%%)' % tuple(self.fill))
        newRect = newRect.rotate(self.rotation, expand = 1)
        # Unfortunately we have to make this ugly mask to make the
        # pasting process work as we want it to.        
        
        mask = Image.new("1", (int(width), int(height)), 255)
        mask = mask.rotate(self.rotation, expand = 1)
        image.paste(newRect, (int(self.x - mask.size[0]/2.0), int(self.y - mask.size[1]/2.0)), mask)
        #draw.rectangle(((self.x - width/2.0, self.y - width/2.0), 
        #                (self.x + width/2.0, self.y + height/2.0)), 
        #                fill='hsl(%d, %d%%, %d%%)' % tuple(self.fill))
                        
    

class Ellipse(Shape):
    """
    An Ellipse primitive. (x, y) is the ellipse's center.
    """
    def __init__(self, x, y, width, height):
        super(Ellipse, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def render(self, image, draw):
        width = self.width * self.scale
        height = self.height * self.scale
        draw.ellipse(((self.x - width/2.0, self.y - width/2.0), 
                        (self.x + width/2.0, self.y + height/2.0)), 
                        fill='hsl(%d, %d%%, %d%%)' % tuple(self.fill))
    

    
    
    
    
    
    
    