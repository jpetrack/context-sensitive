# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:13:19 2016

@author: josh
"""

# This is the file for my intermediate representation. 
# It is a bunch of hierarchical classes that, together, are capable of
# storing and rendering animations.

from PIL import Image, ImageDraw
from copy import deepcopy
from random import random
import math
import tempfile
import os
import subprocess
import shutil
import sys
class ImageCreator:
    """
    An ImageCreator is essentially a list of all of the Elements in an image.
    It keeps track of what frame the animation is currently in, and is in
    charge of rendering each frame of the final animation.
    
    It is the top-level class in the hierarchy. It controls top-level actions.
    """
    def __init__(self, width = 512, height = 512, elems = [], outputpath = "", totalFrames = 20):
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
            
        
    def renderAnimation(self, outputType, framerate):
        print "Rendering %d total frames..." % self.totalFrames
        createVideo = outputType in ["mp4"]
        if (createVideo):
            path = tempfile.mkdtemp()
        else: 
            if not (os.path.exists(self.outputpath)):
                os.mkdir(self.outputpath)
            path = self.outputpath
        for i in xrange(self.totalFrames):
            print "Rendering frame %d." % i
            im = Image.new("RGBA", (self.width, self.height), "white")
            draw = ImageDraw.Draw(im)
            self.renderFrame(im, draw)
            im.save(path + '/' + self.outputpath + "%05d" % self.frame + ".png", "PNG")
            self.frame += 1
        if (createVideo):
            # The options used here:
            # -i is the input path. By adding "%05d", it looks for images with
            # 5 decimal digits after the name.
            # -b:v is the video bitrate.
            # -y says to overwrite files without asking.
            # -r is the framerate.
            subprocess.call(['./ffmpeg', '-i', path + '/' + self.outputpath + '%05d.png', 
                             '-b:v', '8000k', '-y', '-r', str(framerate),
                             self.outputpath + "." + outputType])
                             
            shutil.rmtree(path)
            
        

class RuleDict:
    """
    A RuleDict is a wrapper that knows all of the rules that the user has
    defined, so that it can run the initial rule and then make any other
    rule calls that the initial rule says it needs to make.
    """
    def __init__(self, rules):
        self.rules = {}
        self.ruleLimits = {}
        self.startFrames = {}
        for rule in rules:
            self.rules[rule.name] = rule.executionRules
            self.ruleLimits[rule.name] = rule.limit
            self.startFrames[rule.name] = rule.startFrame
        self.initialRule = rules[0].executionRules
        
    def chooseAndExecuteRule(self, executionRules = 0, existingModifications = 0, startFrame = 0):
        if 0 in self.ruleLimits.values():
            return []
        if executionRules == 0:
            # Placeholder value; this means we need to call the top-level rule.
            executionRules = self.initialRule
        if existingModifications == 0:
            # Placeholder value; make a new blank modifications object.
            existingModifications = Modifications()
            
        # Determine which version of our rule we need to call.
        choice = random()
        sumProb = 0
        chosenRule = None
        for rule in executionRules:
            sumProb += rule[0]
            if sumProb > choice:
                chosenRule = rule[1:]
                break
            
        # Handle possible floating point errors
        if chosenRule is None:
            chosenRule = executionRules[0][1:]
            
        resultElements = []
        for action in chosenRule:
            (thing, modifications) = action
            if type(thing) == type(""):
                # It's a rule name.
                # Make sure it's a valid rule name.
                try:
                    nextRule = self.rules[thing]
                except KeyError:
                    print "Invalid rule or primitive name: %s." % thing
                    sys.exit()
                self.ruleLimits[thing] -= 1
                resultElements += self.chooseAndExecuteRule(nextRule,
                                        existingModifications + modifications, self.startFrames[thing])
                self.ruleLimits[thing] += 1
            else:
                thing.framesUntilDrawn = startFrame
                newElem = (existingModifications + modifications).modifyElement(thing)
                resultElements.append(newElem)
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
    def __init__(self, name, executionRules, limit, startFrame = 0):
        self.name = name
        self.limit = limit
        self.startFrame = startFrame
        
        # Each execution rule is of the form:
        # [p, (r, m), (r, m) ..., (r, m)]
        # where p is a probability proportion (not actually a probability until we normalize), 
        # each r is either a Rule name or an Element, and each m is a modifications object.
        # executionRules is a list of these.
        self.executionRules = executionRules
        totalProbability = sum([x[0] for x in self.executionRules])
        self.executionRules = map(lambda k: [(k[0] / float(totalProbability))] + k[1:], self.executionRules)
    
class Modifications:
    """
    A Modifications object keeps track of a list of modifications. It knows
    how to apply those modifications to an Element, or to an individual Shape.
    
    It also has a number of static methods that can create modifications
    objects, and can combine two objects.
    
    A single modification in a list is a list of two functions. The first
    is a function that will be applied to the Element that's modified.
    The second is a function that will be applied to each shape.
    """
    def __init__(self, modifications = []):
        self.modifications = modifications
    
    def __add__(self, other):
        return Modifications(self.modifications + other.modifications)
        
    
    """
    This method will take an element and return a new copy of it, 
    with any modifications in the Modifications object applied to both
    it and any shapes in its frame list.
    """    
    def modifyElement(self, elem):
        elemcopy = deepcopy(elem)
        for modification in self.modifications:
            modification[0](elemcopy)
        for shape in elemcopy.frameList:
            self.modifyShape(shape)
        return elemcopy
        
    """
    This method is like the above, but for shapes. It also doesn't act on a
    copy, for efficiency reasons.
    """
    def modifyShape(self, shape):
        for modification in self.modifications:
            modification[1](shape)
        return shape
    
    """
    This function will be useful for many static methods where we are modifying
    either the element or the shapes in it, but not both.
    """
    @staticmethod
    def do_nothing(element_or_shape):
        pass
    
    
    """
    Translates a shape absolutely in space.
    """
    @staticmethod
    def AbsoluteTranslate(x, y):
        def translate(shape):
            shape.x += x
            shape.y += y
        return Modifications([(Modifications.do_nothing, translate)])
        
    """
    Translates a shape in space, relative to its current other properties,
    specifically rotation and scale.
    """
    @staticmethod
    def Translate(x, y):
        def translate(shape):
            shape.x += x * shape.xScale * math.cos((math.pi / 180) * shape.rotation)
            shape.y -= x * shape.yScale * math.sin((math.pi / 180) * shape.rotation)
            shape.x -= y * shape.xScale * math.sin((math.pi / 180) * shape.rotation)
            shape.y -= y * shape.yScale * math.cos((math.pi / 180) * shape.rotation)
        return Modifications([(Modifications.do_nothing, translate)])
    """
    Translates a shape in space, relative only to its scale and not rotation
    """
    @staticmethod
    def ScaleTranslate(x, y):
        def translate(shape):
            shape.x += x * shape.xScale
            shape.y -= x * shape.yScale
            shape.x -= y * shape.xScale
            shape.y -= y * shape.yScale
        return Modifications([(Modifications.do_nothing, translate)])
        
    """
    Rotates a shape by an amount specified in degrees.
    """
    @staticmethod
    def Rotate(theta):
        def rotate(shape):
            shape.rotation += theta
        return Modifications([(Modifications.do_nothing, rotate)])
    
    """
    Scales a shape by a specified factor.
    """
    @staticmethod
    def Scale(factor):
        def scale(shape):
            shape.xScale *= factor
            shape.yScale *= factor
        return Modifications([(Modifications.do_nothing, scale)])
        
    """
    Scales a shape horizontally by a specified factor.
    """
    @staticmethod
    def ScaleX(factor):
        def scale(shape):
            shape.xScale *= factor
        return Modifications([(Modifications.do_nothing, scale)])
        
    """
    Scales a shape vertically by a specified factor.
    """
    @staticmethod
    def ScaleY(factor):
        def scale(shape):
            shape.yScale *= factor
        return Modifications([(Modifications.do_nothing, scale)])
      
    """
    Rotates a shape's hue by a specified number of degrees.
    """
    @staticmethod
    def ChangeHue(theta):
        def changeHue(shape):
            shape.fill[0] += theta
            shape.fill[0] %= 360
        return Modifications([(Modifications.do_nothing, changeHue)])
     
    """
    Multiplies a shape's saturation by a specified factor.
    """
    @staticmethod
    def ChangeSaturation(f):
        def changeSaturation(shape):
            shape.fill[1] *= f
            shape.fill[1] = min(shape.fill[1], 100)
            shape.fill[1] = max(shape.fill[1], 0)
        return Modifications([(Modifications.do_nothing, changeSaturation)])
     
    """
    Multiplies a shape's brightness by a specified factor.
    """
    @staticmethod
    def ChangeBrightness(f):
        def changeBrightness(shape):
            shape.fill[2] *= f
            shape.fill[2] = min(shape.fill[2], 100)
            shape.fill[2] = max(shape.fill[2], 0)
        return Modifications([(Modifications.do_nothing, changeBrightness)])
     
    
    """
    Multiplies a shape's alpha (opacity) by a specified factor.
    """
    @staticmethod
    def ChangeAlpha(factor):
        def changeAlpha(shape):
            shape.alpha *= factor
            if shape.alpha > 1:
                shape.alpha = 1
        return Modifications([(Modifications.do_nothing, changeAlpha)])
        
    """
    Delays the animation of an element by a specified number of frames.
    So, if you modify with Delay(3), it will start on frame number 3 (indexing
    from zero).
    """
    @staticmethod
    def Delay(frames):
        def delay(elem):
            elem.currentFrame += frames
            elem.currentFrame %= elem.totalFrames
        return Modifications([(delay, Modifications.do_nothing)])
        
    """
    Delays the start of the animation of an element by a specified number of 
    frames.
    So, if you modify with DelayStart(3), it will begin rendering on the
    third frame of your animation.
    """
    @staticmethod
    def DelayStart(frames):
        def delayStart(elem):
            elem.framesUntilDrawn += frames
        return Modifications([(delayStart, Modifications.do_nothing)])
        
    

class Element:
    """
    An Element is a single shape or animation. It should know what frame it's
    on, how to display itself, and how to modify itself for the sake of
    recursively creating more copies of itself. It also knows when it should
    start being displayed.
    """
    
    def __init__(self, frameList, currentFrame = 0, firstFrame = 0):
        self.frameList = frameList
        self.currentFrame = 0
        self.totalFrames = len(frameList)
        self.framesUntilDrawn = firstFrame
        
        
    def incrementFrame(self):
        if self.framesUntilDrawn == 0:
            self.currentFrame = (self.currentFrame + 1) % self.totalFrames
        else:
            self.framesUntilDrawn -= 1
    def drawFrame(self, image, draw):
        if self.framesUntilDrawn == 0:
            self.frameList[self.currentFrame].render(image, draw)
            
        
    
class Shape(object):
    
    def __init__(self):
        self.fill = [0, 100, 50]
        self.x = 0
        self.y = 0
        self.xScale = 1
        self.yScale = 1
        self.width = 100
        self.height = 100
        self.rotation = 0
        self.alpha = 1

    
    def render(self, image, draw):
        """
        This function renders the shape, with all modifications stored in it.
        It relies on calling self.draw, which will be different depending on
        what kind of shape (rectangle, ellipse, etc) this is.
        """
        width = self.xScale * self.width
        height = self.yScale * self.height
        
        newImage = Image.new("RGB", (int(width), int(height)), 0)
        newdraw = ImageDraw.Draw(newImage)
        self.draw(newdraw, 'hsl(%d, %d%%, %d%%)' % tuple(self.fill), width, height)
        newImage = newImage.rotate(self.rotation, expand = 1)
        # Unfortunately we have to make this ugly mask to make the
        # pasting process work as we want it to. It handles rotation and alpha.      
        
        mask = Image.new("RGBA", (int(width), int(height)), 0)    
        alphamask = Image.new("L", (int(width), int(height)), 0)
        amdraw = ImageDraw.Draw(alphamask)
        self.draw(amdraw, int(255 * self.alpha), width, height)
        mask.putalpha(alphamask)
        
        mask = mask.rotate(self.rotation, expand = 1)
        image.paste(newImage, (int(self.x - mask.size[0]/2.0), int(self.y - mask.size[1]/2.0)), mask)
    

class Rectangle(Shape):
    """
    A Rectangle primitive. (x, y) is the rectangle's center.
    """
    def __init__(self, x=0, y=0, width=100, height=100):
        super(Rectangle, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, xdraw, fillvalue, width, height):
        xdraw.rectangle(((0, 0), (int(width), int(height))), fill=fillvalue)                    
    

class Ellipse(Shape):
    """
    An Ellipse primitive. (x, y) is the ellipse's center.
    """
    def __init__(self, x=0, y=0, width=100, height=100):
        super(Ellipse, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        

    def draw(self, xdraw, fillvalue, width, height):
        xdraw.ellipse(((0, 0), (int(width), int(height))), fill=fillvalue)
    
    
    
    
class Triangle(Shape):
    """
    An equliateral triangle primitive. (x, y) is the triangle's center.
    """
    def __init__(self, x=0, y=0, width=100, height=100):
        super(Triangle, self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        

    def draw(self, xdraw, fillvalue, width, height):
        # Some geometry goes into this to ensure that this triangle will
        # look correct when rotated.
        xdraw.polygon(((int(width/2), 0), (int(width * (.5 * (1 - math.sqrt(3) / 2.0))), int(.75 * height)), (int(width * (.5 * (1 + math.sqrt(3) / 2.0))), int(.75 * height))), fill=fillvalue)
    
    
    
    
    
    