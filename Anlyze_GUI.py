import os
from functools import wraps

medium = '=>'
List_GUI = []
List_PY = []
List_CNAME = []

def readConfig(filename):
    #global  Dtn_Cfg
    Dtn_Cfg = {} #analyze conf, back a dictionary
    f = open(filename, 'r')
    aline = f.readlines()
    #print aline
    maximium = len(aline)
    for index in range(0, maximium):
        if '#' in aline[index]:
            continue
        else:
            key = aline[index].split('=')[0]
            value = aline[index].split('=')[1].strip()
            Dtn_Cfg[key] = value
    return Dtn_Cfg

def getConfig(filename):
    dic = readConfig(filename)
    return dic

def readGUI(filename):
    Dtn_Cfg = {} #analyze GUI, back two Lists or a dictionary
    f = open(filename, 'r')
    aline = f.readlines()
    maximium = len(aline)

    for index in range(0, maximium):
        someline = aline[index]
        #print someline
        if '#' in someline:
            continue
        elif 'Corner' in someline:
            try:
                List_GUI.append(aCorner_GUI)
                List_PY.append(aCorner_PY)
            except:
                pass
                #print 'to avoid the unknown except'
            aCorner_GUI = []
            aCorner_PY = []
            valued = someline.strip().split('=>')#.strip()
            a = valued[1]#.split(medium)[1]
            b = valued[2]#.split(medium)[2]
            c = valued[0]#.split(medium)[0]
            aCorner_GUI.append(a)
            aCorner_PY.append(b)
            List_CNAME.append(c)
        elif 'LOOP' in someline:
            valued = someline.strip().split('=>')#.strip()
            a = valued[1]#.split(medium)[1]
            b = valued[2]#.split(medium)[2]
            aCorner_GUI.append(a)
            aCorner_PY.append(b)
        else:
            print "This line is unknown!"
            continue
    List_GUI.append(aCorner_GUI)
    List_PY.append(aCorner_PY)

    Dtn_Cfg['GUI'] = List_GUI
    Dtn_Cfg['PY'] = List_PY
    Dtn_Cfg['CNAME'] = List_CNAME
    #print Dtn_Cfg
    return Dtn_Cfg

def seqGUI(Dtn_Cfg):
    List_seqGUI = []
    List_seqPY = []
    List_seqCNAME = []
    seq_Dtn = {}

    cornList = Dtn_Cfg['CNAME']
    corn_Len = len(cornList)
    #prepare the list
    for id in range(0, corn_Len):
        List_seqGUI.append('')
        List_seqPY.append('')
        List_seqCNAME.append('')
    #print List_seqCNAME
    #sequential the list
    for id in range(0, corn_Len):
        keyvalue = cornList[id]
        rightKEY = int(keyvalue.split('Corner')[1]) - 1
        #print keyvalue
        #print rightKEY

        List_seqCNAME[rightKEY] = keyvalue
        List_seqGUI[rightKEY] = Dtn_Cfg['GUI'][id]
        List_seqPY[rightKEY] = Dtn_Cfg['PY'][id]

    seq_Dtn['GUI'] = List_seqGUI
    seq_Dtn['PY'] = List_seqPY
    seq_Dtn['CNAME'] = List_seqCNAME
    #print seq_Dtn
    return seq_Dtn


def ctn_corners(part_str):
    # part_str looks like "1-4"
    a1 = int(part_str.split('-')[0])
    a2 = int(part_str.split('-')[1])
    rtList = []
    if a1 < a2:
        for id in range(a1, a2+1):
            rtList.append(id)
    else:
        a_list = range(a2, a1+1)
        a_list.reverse()
        #print 'a_list'
        #print a_list
        for id in a_list:
            rtList.append(id)
    #print 'Yuna8'
    #print rtList
    return rtList

def part_corners(part_str):
    # part_str looks like "1-4" or "3" or "4-2"
    pcornerList = []
    if '-' in part_str:
        subc = ctn_corners(part_str)
        pcornerList.extend(subc)
    else:
        #print 'this is a single corner'
        subc = int(part_str)
        pcornerList.append(subc)
    #print 'below is pcornerList'
    #print pcornerList
    return pcornerList

def total_corners(target_str):
    #target_str looks like "1-4,3,4-2"
    cornerList = []
    parts = target_str.split(',')
    lpart = len(parts)
    for id in range(0, lpart):
        pcr = part_corners(parts[id])
        cornerList.extend(pcr)
    #print 'Yuna7'
    #print cornerList
    return cornerList

def logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print "function    = {0}".format(fn.__name__)
        print "arguments   = {0} {1}".format(args, kwargs)
        print "return      = {0}".format(result)
    return wrapper

def gtemplate(a, c):
    filename = a
    flag1 = 'Case:' + c + ' Start'
    flag2 = 'Case:' + c + ' Start'
    atemplateList = []
    f = open(filename, 'r')
    aline = f.readlines()
    maximium = len(aline)
    for index in range(0, maximium):
        if flag1 in aline[index]:
            startindex = index
        elif flag2 in aline[index]:
            endindex = index
            break
        else:
            continue
    atemplateList = aline[startindex+1:endindex]
    return atemplateList

def pconvert(a):
    #a looks like '/home/reg.GUI'
    #it return a new path '/home/reg_temporary.GUI'
    gfname = a.split('.GUI')[0]
    newPath = gfname + '_temporary.GUI'
    return newPath

def wGUIfile(nfPath, tcornerL, atL):
    file = nfPath
    cornerList = tcornerL
    atemplateList = atL
    fList = []

    alength = len(cornerList)
    blength = len(atemplateList)
    for id_a in range(0, alength):
        tobject = 'Corner' + str(id) + '=>Corner' + str(id) + '_'
        robject = 'Corner=>'
        for id_b in range(0, blength):
            oneline = atemplateList[id_b]
            if robject in oneline:
                temp = oneline.replace(robject, tobject)
                fList.append(temp)
            else:
                fList.append(oneline)
    #write list to new gui file
    if os.path.exists(file):
        os.remove(dfile)
    handle = open(dfile, 'w')
    for id_c in range(0, alength):
        thisline = fList[id_c]
        handle.write(thisline)

@logger
def transformer(a, b, c):
    #guifile, dic['Std_Corner_Run'], dic['Std_Gui_Case']
    #a is guifile '/home/gaom/git/client/lib/reg.GUI'
    #b is corner to run like 1-4,3,4-2
    #c is Case Number like 1, 2 or any
    #ruturn the new guifile full path
    tcornerL = total_corners(b)
    print tcornerL
    atL = gtemplate(a, c)
    print atL
    nfPath = pconvert(a)
    print nfPath
    wGUIfile(nfPath, tcornerL, atL)
    return nfPath

def xxx():
    pass