# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:38:06 2016

@author: josh
"""
import ImageCreator


# TEST 1
#frame1 = ImageCreator.Rectangle(100, 100, 50, 50)
#frame2 = ImageCreator.Rectangle(100, 90, 55, 50)
#frame3 = ImageCreator.Rectangle(100, 80, 65, 50)
#frame4 = ImageCreator.Rectangle(100, 70, 80, 50)
#frame5 = ImageCreator.Rectangle(100, 60, 100, 50)
#
#
#frame6 = ImageCreator.Rectangle(300, 100, 50, 50)
#frame7 = ImageCreator.Ellipse(300, 90, 55, 50)
#frame8 = ImageCreator.Rectangle(300, 80, 65, 50)
#
#
#
#elem1 = ImageCreator.Element([frame1, frame2, frame3, frame4, frame5])
#elem2 = ImageCreator.Element([frame6, frame7, frame8])



## TEST 2
#frame = ImageCreator.Rectangle(100, 100, 50, 50)
#anim = []
#for i in xrange(20):
#    anim.append(frame.withModifications(["changehue " + str(70 * i), "translate %d %d" % (20*i, 10*i)]))
#elem = ImageCreator.Element(anim)
#
#
#creator = ImageCreator.ImageCreator(512, 512, [elem], "nextanimationtest", 16)
#
#creator.renderAnimation()




## TEST 3
#
#frame = ImageCreator.Rectangle(100, 100, 50, 50)
#anim = []
#for i in xrange(3):
#    anim.append(frame.withModifications(["changehue " + str(70 * i), "scale %d" % (1 + .15*i)]))
#elem = ImageCreator.Element(anim)
#
#
#rule1 = ImageCreator.Rule("rule1", [[1, (elem, []), ("rule1", ["translate %d %d" % (7, 0)])], [1, (elem, []), ("rule1", ["translate %d %d" % (0, 7)])]])
##print rule1.executionRules
##rule2 = ImageCreator.Rule("rule2", [[1, (elem, []), ("rule1", ["translate %d %d" % (0, 7)])]])
#
#d = ImageCreator.RuleDict([rule1])
#
#
#creator = ImageCreator.ImageCreator(512, 512, d.chooseAndExecuteRule(), "thirdanimationtest", 16)
##print map(lambda k: k.frameList[0].y, d.chooseAndExecuteRule())
#creator.renderAnimation()



## TEST 4-5
#
#frame = ImageCreator.Rectangle(100, 100, 50, 50)
#anim = []
#for i in xrange(30):
#    anim.append(frame.withModifications(["changehue " + str(10 * i), "scale %f" % (1 + .15*i)]))
#elem = ImageCreator.Element(anim)
#
#
#rule1 = ImageCreator.Rule("rule1", [[1, (elem, []), ("rule1", ["translate %d %d" % (7, 0), "delay 1", "rotate -1"])], [1, (elem, []), ("rule1", ["translate %d %d" % (0, 7), "rotate 1", "delay 1"])]])
##rule2 = ImageCreator.Rule("rule2", [[1, (elem, []), ("rule1", ["translate %d %d" % (0, 7)])]])
#
#d = ImageCreator.RuleDict([rule1])
#
#
#creator = ImageCreator.ImageCreator(512, 512, d.chooseAndExecuteRule(), "rotationtest", 180)
##print map(lambda k: k.frameList[0].y, d.chooseAndExecuteRule())
#creator.renderAnimation()


## TEST 6
#
#frame = ImageCreator.Rectangle(25, 25, 30, 30)
##anim = []
##for i in xrange(1):
##    anim.append(frame.withModifications(["changehue " + str(10 * i), "scale %f" % (1 + .15*i)]))
#elem = ImageCreator.Element([frame, frame.withModifications(["changehue 180"])])
#
#
#rule1 = ImageCreator.Rule("rule1", [[1, (elem, []), ("rule1", ["translate %d %d" % (35, 0), "changehue 40"]), ("rule1", ["translate %d %d" % (0, 35), "rotate 15"])]])
##rule2 = ImageCreator.Rule("rule2", [[1, (elem, []), ("rule1", ["translate %d %d" % (0, 7)])]])
#
#d = ImageCreator.RuleDict([rule1])
#
#
#creator = ImageCreator.ImageCreator(512, 512, d.chooseAndExecuteRule(), "forktest", 2)
#
##print map(lambda k: k.frameList[0].y, d.chooseAndExecuteRule())
#creator.renderAnimation()



## TEST 7
#
#frame = ImageCreator.Rectangle(50, 256, 100, 100)
#anim = []
#for i in xrange(20):
#    anim.append(frame.withModifications(["rotate %f" % (18*i), "changehue 180"]))
#elem = ImageCreator.Element(anim)
#
#
#rule1 = ImageCreator.Rule("rule1", [[1, (elem, []), ("rule1", ["rtranslate %d %d" % (50, 0), "scale .9", "changehue 5", "delay 1"])]])
##rule2 = ImageCreator.Rule("rule2", [[1, (elem, []), ("rule1", ["translate %d %d" % (0, 7)])]])
#
#d = ImageCreator.RuleDict([rule1])
#
#
#creator = ImageCreator.ImageCreator(512, 512, d.chooseAndExecuteRule(), "rtranslatetest", 300)
##print map(lambda k: k.frameList[0], d.chooseAndExecuteRule())
#creator.renderAnimation()





## TEST 8-9 (change ellipse to rectangle and change width/height) and also 10 
#
#frame = ImageCreator.Ellipse(256, 256, 1, 2)
#anim = []
#for i in xrange(180):
#    anim.append(frame.withModifications(["rotate %d" % (-2 * i), "changehue %d" % (130 + 10*i), "setalpha .7"]))
#elem = ImageCreator.Element(anim)
#
#
#rule1 = ImageCreator.Rule("rule1", [[1, ("rule2", [])]])
#rule2 = ImageCreator.Rule("rule2", [[1, (elem, []), ("rule2", ["rtranslate %d %d" % (2, 0), "rotate 12", "scale 1.22"])]])
#
#d = ImageCreator.RuleDict([rule1, rule2])
#
#
#creator = ImageCreator.ImageCreator(512, 512, d.chooseAndExecuteRule(), "rtranslatetest2", 200)
##print map(lambda k: k.frameList[0], d.chooseAndExecuteRule())
#creator.renderAnimation()


# TEST 11 (improving on 10)

frame = ImageCreator.Ellipse(256, 256, 1, 2)
anim = []
for i in xrange(180):
    anim.append(frame.withModifications(["rotate %d" % (-2 * i), "changehue %d" % (130 + 10*i), "setalpha .7"]))
elem = ImageCreator.Element(anim)

rule0 = ImageCreator.Rule("rule0", [[1, ("rule1", []), ("rule1", ["scale .9", "changealpha .3", "changehue 120"])]])
rule1 = ImageCreator.Rule("rule1", [[1, ("rule2", []), ("rule2", ["rotate 60", "changehue 60"]), ("rule2", ["rotate 120", "changehue 120"]), ("rule2", ["rotate 180", "changehue 180"]), ("rule2", ["rotate 240", "changehue 240"]), ("rule2", ["rotate 300", "changehue 300"])]])
rule2 = ImageCreator.Rule("rule2", [[1, (elem, []), ("rule2", ["rtranslate %d %d" % (2, 0), "rotate 12", "scale 1.22", "changehue 5"])]])

d = ImageCreator.RuleDict([rule0, rule1, rule2])


creator = ImageCreator.ImageCreator(512, 512, d.chooseAndExecuteRule(), "rtranslatetest2", 200)
#print map(lambda k: k.frameList[0], d.chooseAndExecuteRule())
creator.renderAnimation()

