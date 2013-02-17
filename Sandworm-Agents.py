####                Sandworm Movment	                           ####
##   Below is a model of Sandworm behavior based on the novel Dune   ##
##   By Frank Herbert. According to the novel, sandworms do some     ##
##   easily modeled behavior, such as move around. They are also     ##
##   attracted to sound. They occasionally eat smaller worms. Here   ##
##   a tool used to attracted sandworms, called a thumper, is rep-   ##
##   resented by a green dot, made by clicking on the scene. Sand-   ##
##   are positions are represented by the moving red dots. Their     ##
##   past 4 positions by the yellow dots. Stationary red and blue    ##
##   dots represent sandworm corpses.
##
##  Update :: No more corpses, replaced by maturation mechanic
##         :: Sometimes a thumper kills a worm (Water of Life?)
##
## Things to add ::
##
##  1) Starving < ------- DONE
##  2) Middle after outskirts
##  3) Length increases on feed
##  4) Ignore thumper for close food
##  5) Teamworks / Teams <---- DONE
##  6) Every so often thumber adds size <--- DONE
##  7) Every so often they make a bad movie based on it (Approx 20 years) < --- Dan Higgs
##  8) Thumpers Randomly kill sandworms (Jaws, Oxygen tanks?) (Sandworms would be water) <--- DONE
##     Red Kills, Green Rewards
##  9) Worms reach certian size, they explode into sandfish and mature <--- DONE
## 10) Fatigue
##
## Download - April 5th, 9:30pm, 6:30, 5pm, etc
##
##
##
from visual.graph import * # import graphing features
import random
#from math import *

def InitGrid(N,Prob):
    Distribution = []
    count = 0
    for j in range(0,N,1):
        for k in range(0,N,1):
            d = random.random()
            if d < Prob:
                c = random.random()
                if c > .9:
                    #Distribution.append([j,k,d*(1/Prob),2,1])
                    Distribution.append([j,k,1,2,1])
                else:
                    Distribution.append([j,k,d*(1/Prob),1,1])
    return Distribution

def Move():
    return ([0,1],[1,0],[1,1],[0,-1],[-1,-1],[1,-1],[-1,1],[-1,0])

def MakeGreat(loc):
    if loc != 0:
        return loc
    else:
        return 0

def IsGreatAttractor(Distribution,Detector,loc):
    A = Distribution
    Test = []
    if loc == 0:
        return 0
    else:
##        print loc
##        print A
        Test = (((A[0] - loc[0])*(A[0] - loc[0])) + ((A[1] - loc[1])*(A[1] - loc[1])))**.5
        if Test < Detector*10*A[2]:## DETECTION THRESHOLD (Bigger worms can hear farther)
            return 1

def AttractedToGreatness(Distribution,j,loc,locpoint,LiveOrDie):
    A = Distribution
    NoChange = A[j][:]
    Moves = Move()
    RR = []
    for k in range(0,len(Moves)-1):
        NoChange[0] = (A[j][0]+Moves[k][0])
        NoChange[1] = (A[j][1]+Moves[k][1])
        Test = ((NoChange[0] - loc[0])**2 + (NoChange[1] - loc[1])**2)**.5
        if k == 1:
            RR = Test
            OhNoes.append(NoChange)
            count +=1
        else:
                if Test < RR:
                    OhNoes = []
                    OhNoes.append(NoChange[:])
                    count = 0
                    RR = Test;
                else:
                        if Test == RR:
                            OhNoes.append(NoChange[:])
                            count += 1
    i = random.randint(0,(len(OhNoes)-1))
    A[j] = OhNoes[i]
    if Test < 2:
        if LiveOrDie > .2:
            A[j][2] = A[j][2] + 1##+ random.random()*5 ## Reward Amount
            A[j][4] = 0
        else:
            A[j][2] = 0
        loc = 0
        locpoint.visible = False
        del locpoint
    return A,loc

def Walks(Distribution,Detector,count,loc,locpoint,Size,LiveOrDie):
    A = Distribution
    loc = MakeGreat(loc)
    ### Movement Modifiers ###
    a = 1   ## X
    b = 1   ## Y
    Moves = Move()
    for j in range(0,len(A),1):
        FS = len(A)
        DangerIndex = DangerCalc(Distribution,j,Detector)
        GreatAttractor = IsGreatAttractor(A[j],Detector,loc)
        if GreatAttractor == 1:
            A,loc = AttractedToGreatness(A,j,loc,locpoint,LiveOrDie)
        elif DangerIndex == 1:
            A = Actions(A,j,Detector,Size)
        else:
            k = random.randint(0,len(Moves)-1)
            A[j][0] = A[j][0] + Moves[k][0]
            A[j][1] = A[j][1] + Moves[k][1]
        if FS != len(A):
            print ' what?!'
            break
    return A, loc

def Torusify(A,Size):
    for j in range(0,len(A)):
        if A[j][0] > Size:
            A[j][0] = 0
        else:
            if A[j][0] < 0:
                A[j][0] = Size
            else:
                A[j][0] = A[j][0]
        if A[j][1] > Size:
            A[j][1] = 0
        else:
            if A[j][1] < 0:
                A[j][1] = Size
            else:
                A[j][1] = A[j][1]
        if (A[j][2] < .5 and A[j][2] != 0): #Grow Up Counter, max 'grow' size, grow larger by eating
            A[j][2] = A[j][2] + .01
        if A[j][4] >= 10000000:
            A[j][2] = 0
        if A[j][4] < 10000000: # Starve to Death Counter
            A[j][4] = A[j][4] + 1
    return A

def TorusifyHF(A,Size):
    if A[0] > Size:
        A[0] = 0
    else:
        if A[0] < 0:
            A[0] = Size
        else:
            A[0] = A[0]
    if A[1] > Size:
        A[1] = 0
    else:
        if A[1] < 0:
            A[1] = Size
        else:
            A[1] = A[1]
    if A[2] < .5:
        A[2] = A[2] + .01
    if A[4] == 1000:
        A[2] = 0
    if A[4] < 1000: # Starve to Death Counter
        A[4] = A[4] + 1
    return A

def DangerCalc(Distribution,j,Detector):
    A = Distribution
    Test = []
    if j == 0:
        for k in range(1,len(A),1):
            if A[j][3] != A[k][3]:
                Test.append(((A[j][0] - A[k][0])**2 + (A[j][1] - A[k][1])**2)**.5)
##            print ''
##            print 'j == 0'
##            print ''
##            print Test
    else:
        for k in range(0,j):
            if A[j][3] != A[k][3]:
                Test.append(((A[j][0] - A[k][0])**2 + (A[j][1] - A[k][1])**2)**.5)
##            print ''
##            print 'j-1'
##            print ''
        for k in range(j+1,len(A)):
            if A[j][3] != A[k][3]:
                Test.append(((A[j][0] - A[k][0])**2 + (A[j][1] - A[k][1])**2)**.5)
####            print ''
##            print 'j+1'
##            print ''
    for k in range(0,len(Test),1):
        if Test[k] < Detector*A[j][2]:## DETECTION THRESHOLD (Bigger worms can hear farther[More surface area or something])
##            print 'Pass'
##            print j
##            print '----------------------'
            return 1

def Rotate(A,B):
    del B[0]
    B.append(A)
    return B



##def PlotMover5(Distribution,Detector):
##    A = Distribution
##    point = []
##    loops = len(A)
##    for j in range(0,(loops),1):
##        if DangerCalc(A,j,Detector) == 1:
##            point[5]((points(pos=[A[j][0],A[j][1]],color=color.red)))
##        else:
##            point[5]((points(pos=[A[j][0],A[j][1]],size=6,color=color.blue)))
##    return point

def Actions(A,j,Detector,Size):
    Placehold = []
    Sk = 0
    if j > -1:
        ReVal = 10000000
        PlaceHold = 0
        for k in range(0,len(A)):
            if k == j:
                None
##                print 'Pass'
            else:
               # print 'Not Passed'
                if (DangerCalc(A,k,Detector) == 1 and A[j][3] != A[k][3]):
##                    print '======'
##                    print A[j][3],A[k][3]
                    PlaceHold = (((A[j][0] - A[k][0])**2 + (A[j][1] - A[k][1])**2)**.5)
                    if PlaceHold < ReVal:
                        ReVal = PlaceHold
                        Sk = k
##                        print A[j][3],A[Sk][3], ReVal
##        print Sk,ReVal
##        print '----------------'
        if A[j][2] < A[Sk][2]: ## Flee
            A = Flee(A,j,Sk,Size)
        if A[j][2] >= A[Sk][2]: ## Hunt
            A = Hunt(A,j,Sk,Size)
    return A

def Hunt(A,j,Sk,Size):
    c = random.randint(1,2)   ## Hunt X Multiplier
    d = random.randint(1,2)   ## Hunt Y Multiplier
    Moves = Move()
    RR = 0
    count = 0
    OhNoes = []
    Test = 0
    NoChange = A[j][:]
    for k in range(0,len(Moves)-1):
        NoChange[0] = (A[j][0]+c*Moves[k][0])
        NoChange[1] = (A[j][1]+d*Moves[k][1])
        Test = ((NoChange[0] - A[Sk][0])**2 + (NoChange[1] - A[Sk][1])**2)**.5
        if k == 1:
            RR = Test;
            OhNoes.append(NoChange)
            count +=1
        else:
            if Test < RR:
                OhNoes = []
                OhNoes.append(NoChange[:])
                count = 0
                RR = Test;
            else:
                if Test == RR:
                    OhNoes.append(NoChange[:])
                    count += 1
    i = random.randint(0,(len(OhNoes)-1))
    A[j] = OhNoes[i]
    return A

def Flee(A,j,Sk,Size):
    a = random.randint(0,2)   ## Flee X Multiplier
    b = random.randint(0,2)   ## Flee Y Multiplier
    Moves = Move()
    count = 0
    RR = 0
    OhNoes = []
    Test = 0
    NoChange = A[j][:]
    for k in range(0,len(Moves)-1):
        NoChange[0] = (A[j][0]+a*Moves[k][0])
        NoChange[1] = (A[j][1]+b*Moves[k][1])
##        NoChange = TorusifyHF(NoChange,Size)
        Test = ((NoChange[0] - A[Sk][0])**2 + (NoChange[1] - A[Sk][1])**2)**.5
        if k == 1:
            RR = Test;
            OhNoes.append(NoChange)
            count +=1
        else:
            if Test > RR:
                OhNoes = []
                OhNoes.append(NoChange[:])
                count = 0
                RR = Test;
            else:
                if Test == RR:
                    OhNoes.append(NoChange[:])
                    count += 1
    i = random.randint(0,(len(OhNoes)-1))
    A[j] = OhNoes[i][:]
    return A

def Uniquify(seq): 
    # not order preserving 
    set = {} 
    map(set.__setitem__, seq, []) 
    return set.keys()

def Eat(Distribution):
    A = Distribution
    Del = []
    DelThis = []
    Ugly = 0
    for j in range(0,len(A)):
        for k in range(0,len(A)):
            if j == k:
                None
            elif (A[j][0] == A[k][0] and A[j][3] != A[k][3]):
                if A[j][1] == A[k][1]:
                    if A[j][2] >= A[k][2]:
                        A[j][2] = (A[j][2] + A[k][2])
                        Del.append(k)
                        A[j][4] = 1
                    else:
                        A[k][2] = (A[k][2] + A[j][2])
                        Del.append(j)
                        A[k][4] = 1
                if A[j][2] == 0:
                    Del.append(j)
##    print '--------------'
##    print array(A)
##    print 'Length of A is ', len(A)
##    print Del
    Del = Uniquify(Del)
    k = 0
    for j in Del:
        A[j][2] = 0
    for j in range(0,len(A)):
        if A[j][2] == 0:
            k += 1
    while k != 0:
        j = len(A)
        for i in range(0,j):
            if A[i][2] == 0:
                del A[i]
                k -= 1
                break
##    print Del
##    print array(A)
##    print 'Length of A is ', len(A)
##    print '--------------

def ColorChange(pointz,B):
##    print pointz
    point = []
##    print B
    for k in range(0,len(pointz[2])):
##        print len(B[3])
##        print len(pointz[2])
##        print '----'
        pointz[2][k].visible = False
##                print '-----------------------'
##                print len(pointz[j])
    for k in range(0,len(pointz[2])):
        del pointz[2][0]
##                print len(pointz[j])
##                print pointz[j]
    for k in range(0,len(B[0])):
        point.append((points(pos=[B[3][k][0],B[3][k][1]],color=color.yellow)))
    temp = pointz[3]
    del pointz[3]
    del pointz[2]
    pointz.append(point)
    pointz.append(temp)
    return pointz

def PlotElements(point,A):
    loops = len(point[0])
##    for j in range(0,4):
##        for k in range(len(point[0])):
##            point[j][k] = color.white
##    for j in range(0,len(A)):
##        points(pos=[A[j][0],A[j][1]],color=color.white)
    for j in range(0,(loops),1):
        point[0][j].visible = False
    del point[0]
    return point
                  
def PlotMover(Distribution,Detector):
    A = Distribution
    point = []
    loops = len(A)
    for j in range(0,(loops),1):
        if (DangerCalc(A,j,Detector) == 1 and A[j][3] == 1):
            point.append((points(pos=[A[j][0],A[j][1]],size=(13 - log(A[j][4])),color=color.red)))
        if (DangerCalc(A,j,Detector) == 1 and A[j][3] == 2):
            point.append((points(pos=[A[j][0],A[j][1]],size=(13 - log(A[j][4])),color=color.cyan)))
        if (DangerCalc(A,j,Detector) != 1 and A[j][3] == 1):
            point.append((points(pos=[A[j][0],A[j][1]],size=(13 - log(A[j][4])),color=color.magenta)))
        if (DangerCalc(A,j,Detector) != 1 and A[j][3] == 2):
            point.append((points(pos=[A[j][0],A[j][1]],size=(13 - log(A[j][4])),color=color.blue)))
    return point  

def Explode(A,B,countmulti):
    temp = []
    Del = []
    for j in range(0,len(A)):
        if A[j][2] > 3: ## Size to Explode At
            temp.append(j)
            if countmulti != 0:
                None
            else:
                countmulti = 1
    for k in range(0,len(temp)):
        for i in range(0,5):
            B.append([A[temp[k]][0],A[temp[k]][1],0,A[temp[k]][3],1])
    Del = Uniquify(temp)
    for j in range(0,len(Del)):
        A[(Del[j])] = [0,0,0]
    k = len(Del)
    while k != 0:
        j = len(A)
        for i in range(0,j):
            if A[i] == [0,0,0]:
                del A[i]
                k -= 1
                break
    return A,B,countmulti

def GoForth(A,C,B,countmulti,pointz):
    Moves = Move()
    temp = []
    temp2 = []
    if countmulti < 50: ## Maturation Rate ##
        for j in range(0,len(B)):
            k = random.randint(0,len(Moves)-1)
            C[j][0] = C[j][0] + Moves[k][0]
            C[j][1] = C[j][1] + Moves[k][1]
            d = random.random()
            if d > .7:
                C[j][2] = C[j][2] + .01
    else:
        for j in range(0,len(C)):
            A.append(C[j])
        for j in range(0,4):
            for k in range(0,len(C)):
                pointz[j].append(points(pos=[C[k][0],C[k][1]],size=6,color=color.blue))
##                B[j].append(C[k][:])
##            print pointz[0]
        C = []
        countmulti = 0
    countmulti += 1
    return A,C,B,countmulti,pointz









###                   ###
# Begin Executing Stuff #
###                   ###

N=500
Prob = .0001
R = 50
A = InitGrid(N,Prob)  ##Populate Grid
point =[]
pointz = []
loc = 0
locpoint = []
scalefix =[]
Size = N
#A = [[0,0,.25],[5,5,.5]]
Detector = 100#Set modifier for detection range
print Detector
print '---------Start----------'
print array(A)
print 'Length of A:', len(A)
count = 0
print '----------End-----------'
scene = display(title='Movement of Agents',autocenter=true,autoscale=true)
scalefix.append(points(pos=[Size,Size],color=color.white))
scalefix.append(points(pos=[0,0],color=color.white))
scalefix.append(points(pos=[0,Size],color=color.white))
scalefix.append(points(pos=[Size,0],color=color.white))
B = []
C = []
countmulti = 0
LiveOrDie = 0
locpoint = points(pos=[0,0,0])
locpoint.visible = False
while (len(A) or len(B)) > 0:
    size = len(A)
    if count < 5:
        pointz.append(point[:])
##        print pointz
        B.append(A)
    else:
        Rotate(A,B)
        pointz = PlotElements(pointz,A)
        pointz = ColorChange(pointz,B)
    A,loc = Walks(A,Detector,count,loc,locpoint,Size,LiveOrDie)
    A = Torusify(A,Size)
    Eat(A)
    count += 1
    if count < 5:
        point = PlotMover(A,Detector)
    if count > 5:
        pointz.append(PlotMover(A,Detector))
    if scene.mouse.clicked:
        m = scene.mouse.getclick()
        locpoint.visible = False
        del locpoint
        loc = m.pos
        LiveOrDie = random.random() ## Chance Thumper will Kill
        if LiveOrDie > 0:#Change to change chance
            locpoint = points(pos=loc,color=color.green,size=10)
        else:
            locpoint = points(pos=loc,color=color.red,size=10)
        print locpoint
        print '-------------------------------------------'
        print array(A)
        print 'Current size of A ',len(A)
        print 'Current Count is', count
        print '-------------------------------------------'
##        print loc[0], '', loc[1]
    rate(R)
    A,C,countmulti = Explode(A,C,countmulti)
    if len(C) != 0:
        A,C,B,countmulti,pointz = GoForth(A,C,B,countmulti,pointz)
    size1 = len(A)
    if size != size1:
        print '---------Size Change-----------'
        print array(A)
        print 'Current count is',count
        print 'Size of A is',size1
        print '-------------------------------'
##    print 'Space'
print array(A)
print 'Count is ', count
print 'Number of worms:',len(A)
print 'There can be only Zer0.'
print '------------------------'
##print A##print A[0][0]
##print A[0][1]
##print A[0][2]

##    if scene.mouse.clicked:
##        m = scene.mouse.getclick()
##        loc = m.pos
##        print loc
##        points(pos=[loc],size=50,color=color.green)
