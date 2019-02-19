#ToolBox_Script
#        _________   
#       / _______ \
#      / /       \ \
#   ===================
#   =       ___       =
#   =     _|   |_     =
#   =====/_| + |_\=====
#   =    | |___| |    =
#   =    |_______|    =
#   =                 =
#   ===================
import maya.cmds as cmds
import maya.mel as mel
#_________________HotKey_________________#
#HotKey
version = mel.eval('getApplicationVersionAsFloat')
def runtimeCommand():
    if not cmds.runTimeCommand('switchRTC', exists = True):
        cmds.runTimeCommand('switchRTC',
                            default = True,
                            category = 'User',
                            ann = "switches wieght unlocked influences",
                            c = 'switchInfluence()')
    
    cmds.nameCommand('switchNC',
                     ann = "Create a Sphere",
                     default = True,
                     command = 'switchRTC')
    if version >= 2016:
        clHotkeySet = "slHotKeySet"
        if not cmds.hotkeySet (clHotkeySet, exists = True):
            cmds.hotkeySet(clHotkeySet, source = 'Maya_Default', current = True)
        else:
            cmds.hotkeySet (clHotkeySet, e = True, current = True)
    cmds.hotkey(k = ';', n = 'switchNC')
runtimeCommand()
#------------------------------------------------------------------------------
def switchInfluence():    
    sel = cmds.ls(sl = True)
    influenceList = cmds.skinCluster(sel, query = True, influence = True)
    unlockedList = []
    for num in influenceList:
        lockValue = cmds.getAttr('%s.liw'%num)
        if lockValue == False:
            unlockedList.append(num)
    #find selected influence
    currentCtx1 = cmds.currentCtx()
    currentInf = cmds.artAttrSkinPaintCtx(currentCtx1, query = True, inf = True)
    #Check for thing in index
    if currentInf in unlockedList:
        #find index
        index = unlockedList.index(currentInf)
    
        myJoint = unlockedList[(index -1)]
        mel.eval('artSkinSelectInfluence("artAttrSkinPaintCtx", "%s")'% myJoint)
    else:
        error("HappyBirthday Claytor")
#______________________RIGGING____________________________
#new AutoFK Script
skeleton = []
fk_Grp =[]
def createFKSystem(color, shape, size):
    sel = cmds.ls(sl = True)
    if sel:
        sel = sel[0]
        FKChain(color, shape, size, sel)
        ctrlGrp = cmds.group(fk_Grp, n = 'FK_Ctrl_Grp')
        cmds.group(skeleton, n = 'FK_Joints')
        del fk_Grp[:], skeleton[:]
        return ctrlGrp
    else:
        ctrl = createControl(color,shape,size,"empty")
        grp = groupControl(ctrl)
    
#________________________________________________________      
def FKChain(color, shape, size, sel):
    grpList = []
    backgroundCheck(sel)
    children = cmds.listRelatives(sel, c = True)
    if children:
        numberChildren = len(children)
        if numberChildren > 1:
            for child in children:
                nextGrp = FKChain(color,shape,size,child)
                grpList.append(nextGrp)
        else:
            nextGrp = FKChain(color,shape,size,children[0])
            grpList.append(nextGrp)
    ctrl = createControl(color,shape,size,sel)
    grp = groupControl(ctrl)
    orientConstrain(grp, ctrl, sel)
    followRotate(ctrl)
    if children:
        for num in grpList:
            fkParenting(num,ctrl)
    if (cmds.listRelatives(sel, p = True)):
        cmds.parent(sel, world = True)
    fk_Grp.append(grp)
    skeleton.append(sel)
    return [grp, ctrl]
#________________________________________________________             
def orientConstrain(grp, ctrl, jnt): 
    cmds.matchTransform(grp,jnt)
    cmds.parentConstraint(ctrl,jnt, mo = True)
def groupControl(ctrl):
    grp = cmds.group(ctrl, name = "%s_Grp"%ctrl)
    return grp


    
def fkParenting(num,ctrl):
    grp = num[0]
    nextCtrl = num[1]
    cmds.parentConstraint(ctrl, grp, mo = True, skipRotate = ['x','y','z'])
    rotateParent = cmds.parentConstraint(ctrl ,grp, mo = True, skipTranslate = ['x', 'y','z'], name = "rotateParent")[0]
    cmds.connectAttr ('%s.Follow_Rotate'%nextCtrl, '%s.w0'%rotateParent)
def followRotate(ctrl):
    cmds.addAttr(ctrl, maxValue = 1, minValue = 0, longName = 'Follow_Rotate', dv = 1)
    cmds.setAttr("%s.Follow_Rotate"%ctrl, e = True, keyable = True)
#________________________________________________________  
def createControl(color,shape,size,sel):#builds a control and orients the control with a group
    if shape == "circle":
        ctrl = circle(sel,size)
    if shape == "square":
        ctrl = square(sel,size)
    if shape == "diamond":
        ctrl = diamond(sel,size)
    if shape == "arrow":
        ctrl = arrow(sel,size)
    changeColor(ctrl,color)
    cmds.setAttr("%s.rz"%ctrl, 90)
    cmds.makeIdentity (ctrl, apply = True)
    return ctrl
def changeColor(ctrl,color):
   cmds.setAttr ('%s.overrideEnabled' %ctrl, 1)
   cmds.setAttr ('%s.overrideColor' %ctrl, color)
#______________________________________________________________
def square(sel, size):
    name = '%s_ctrl' %sel
    ctrl = cmds.curve(name = name,
                      d = 1, 
                      p = [(-size, 0, size),(-size, 0, -size), (size, 0, -size), (size, 0, size), (-size, 0, size)], 
                      k = [0,1,2,3,4])
    return ctrl
def diamond(sel, size):
    name = '%s_ctrl' %sel
    ctrl = cmds.curve(name = name,
                      d = 1,
                      p = [(-size,0,0),(0,0,size),(size,0,0),(0,0,-size),(-size,0,0)],
                      k = [0,1,2,3,4])
    return ctrl  
 
def arrow(sel, size):
    name = '%s_ctrl' %sel
    ctrl = cmds.curve(name = name,
                      d = 1,
                      p = [(0,0,-size),(-size,0,0),((-0.5*size),0,0),((-0.5*size),0,size),((0.5*size),0,size),((0.5*size),0,0),(size,0,0),(0,0,-size)],
                      k = [0,1,2,3,4,5,6,7])
    return ctrl
def circle(sel, size):   
    name = '%s_ctrl' %sel
    ctrl = cmds.circle(name = name,
                       c = [0, 0, 0], 
                       nr = [0,1,0],
                       sw =  360, 
                       r  = size, 
                       d =  3, 
                       ut = 0, 
                       tol = 0.01,
                       s = 8, 
                       ch = 1)[0]
    return ctrl
#________________________________________________________ 
def backgroundCheck(sel):
    family = cmds.listRelatives(sel, ad = True) or []
    for member in family:
        isJoint = cmds.objectType(member, isType = "joint")
        if isJoint == False:
            cmds.error("You must only have Joints")
#________________________________________________________ 
def createIK(color, shape, size,solver, orientation):
    sel = cmds.ls(sl = True, type = "joint")
    if sel:
        selLength = len(sel)
        if selLength == 2:
            myIK = cmds.ikHandle(sel[0], sel[1], name = "%s_IK_Handle"%sel[0])[0]
            ctrl = createControl(color,shape,size,sel[0])
            grp = groupControl(ctrl)
            cmds.matchTransform(grp,myIK)
            cmds.parent(myIK,ctrl) 
            if solver == True:
                pole = poleVector(color,size,sel[0], orientation)
                cmds.poleVectorConstraint(pole[0], myIK)
                grp = cmds.group(pole[1],grp, name = "IK_Ctrl_Grp" )
        else:
            cmds.error("only select two joints")
    else:
        cmds.error("No Object Selected.")
    return grp
def poleVector(color,size,sel, orientation):
    chain = cmds.listRelatives(sel, ad = True)
    jointPosition = int((len(chain))/2) + 1
    poleVector = createControl(color,"arrow",size,("%s_poleVector"%sel))
    grp = groupControl(poleVector)
    cmds.matchTransform(grp, chain[jointPosition])
    cmds.parent(grp, chain[jointPosition])
    if orientation[0] == "z":
        cmds.xform(grp,r = True, t=(0, 0, (orientation[1])))
    if orientation[0] == 'x':
        cmds.xform(grp,r = True, t=(0, (orientation[1]),0))
    if orientation[0] == "y":
        cmds.xform(grp,r = True, t=((orientation[1]),0,0))
    cmds.parent(grp, world = True)
    return poleVector, grp
#_________________________________________________________
def branchRK(rkGrp,prefix,parameters):
    grp = cmds.duplicate(rkGrp, name = ("%s_Joints"%prefix), rc = True)
    rkList = cmds.listRelatives(rkGrp, ad = True, type = "joint")
    branchList = cmds.listRelatives(grp, ad = True, type = "joint")
    length = len(rkList)
    for num in range(0,length):
        branchList[num] = cmds.rename(branchList[num], "%s_%s"%(prefix,rkList[num]))
    if prefix == "IK":
        cmds.select(branchList[-1], branchList[0])
        ctrlGrp = createIK(parameters[0], parameters[1],parameters[2], parameters[3], parameters[4])
    if prefix == "FK":
        cmds.select(branchList[-1])
        ctrlGrp = createFKSystem(parameters[0], parameters[1],parameters[2])
    return [grp,branchList,rkList, ctrlGrp]
#RK script
def createRK(color,shape, size,solver,orientation):
    parameters = [color,shape,size,solver,orientation]
    sel = cmds.ls(sl = True)   
    for num in sel:
        rkGrp = cmds.group(num, name = "RK_Joints")
        fkGrp = branchRK(rkGrp, "FK", parameters)
        ikGrp = branchRK(rkGrp, "IK", parameters)
        rkList, ikList, fkList = fkGrp[2], ikGrp[1], fkGrp[1]
        switchCtrl = cmds.circle(name = 'IKFK_Switch')[0]
        cmds.addAttr(switchCtrl, maxValue = 1, minValue = 0, longName = 'IKFK_Switch', dv = 1)
        cmds.setAttr("%s.IKFK_Switch"%switchCtrl, e = True, keyable = True)
        reverseNode = cmds.shadingNode('reverse',au = True)
        cmds.connectAttr('%s.IKFK_Switch'%switchCtrl, '%s.inputX'%reverseNode)
        length = len(rkList)
        for num in range(0,length):
            fk = fkList[num]
            ik = ikList[num]
            rk = rkList[num]
            FK_Constrain = cmds.parentConstraint(fk, rk, name = 'FK_Constrain')[0]
            RK_Constrain = cmds.parentConstraint(ik,rk, name = 'IK_Constrain')[0]
            cmds.connectAttr('%s.IKFK_Switch'%switchCtrl, '%s.w0'%RK_Constrain)
            cmds.connectAttr('%s.outputX'%reverseNode, '%s.w1'%RK_Constrain)
        cmds.connectAttr('%s.IKFK_Switch'%switchCtrl, '%s.visibility'%fkGrp[3])
        cmds.connectAttr('%s.outputX'%reverseNode, '%s.visibility'%ikGrp[3])
        
#______________________SKELETON__________________________________#
def createJointChain(pValue, sValue, cValue):
    skeleton = []
    sels = cmds.ls(sl = True)
    for num in range(0,(len(sels))):
        newJoint = cmds.joint((sels[num]),n = "%s_jnt"%sels[num])
        cmds.matchTransform(newJoint, sels[num])
        skeleton.append(newJoint)
    if cValue == True:    
        for num in range(0,(len(skeleton))):
            if skeleton[num] == skeleton[-1]:
                cmds.parent(skeleton[num], world = True)
            else:
                cmds.parent(skeleton[num], skeleton[(num + 1)])
    if pValue == True:
        for num in range(0,(len(skeleton))):
            cmds.parentConstraint(skeleton[num],sels[num])
    if sValue == True:
        for num in range(0,(len(skeleton))):
            cmds.scaleConstraint(skeleton[num],sels[num])       
     
#---------------------------------------------------------------------
def toggleAxisDisplay():
    sel = cmds.ls(sl= True)[0]        
    toggleList = cmds.listRelatives(sel, ad = True, typ = "joint")
    if toggleList:
        toggleList.append(sel)
    else:
        toggleList = sel 
    query = cmds.toggle(sel, query = True, localAxis = True)
    if query == False:
        for item in toggleList:
            cmds.setAttr('%s.jointOrientX'%item, lock = False, keyable = True)
            cmds.setAttr('%s.jointOrientY'%item, lock = False, keyable = True)
            cmds.setAttr('%s.jointOrientZ'%item, lock = False, keyable = True)
            cmds.toggle(item, localAxis = True, state = True)
    else:
        for item in toggleList:
            cmds.setAttr('%s.jointOrientX'%item, keyable = False)
            cmds.setAttr('%s.jointOrientY'%item, keyable = False)
            cmds.setAttr('%s.jointOrientZ'%item, keyable = False)
            cmds.toggle(item, localAxis = True, state = False)
    




#______________________GENERAL_______________________________#
def parentScale():
    sel = cmds.ls(sl = True)
    parent = sel[0]
    length = len(sel)
    for num in range(1, length):
        child = sel[num]
        cmds.parentConstraint(parent, child, mo = True)
        cmds.scaleConstraint(parent, child, mo = True)
#---------------------------------------------------------
def separate():
    sel = cmds.ls(sl = True)
    name = "query"
    split = cmds.polySeparate(sel,n = name)
    cmds.parent(split, world = True)
    deleteHistory(split)
#---------------------------------------------------------
def combine():
    sels = cmds.ls(sl = True)
    if sels:
        length = len(sels)
        if length > 1:
            for num in range(1,length):
                p1, p2 = sels[0], sels[(num)]
                sels[0] = cmds.polyUnite(p1, p2, name = "query")[0]
                deleteHistory(cmds.ls(sl = True))
    else:
        cmds.error("buddy, you need to select at least two items.")
#---------------------------------------------------------
def grpParent():
    sels = cmds.ls(sl = True)
    if sels:
        length = len(sels)
        for num in range(0, length):
            aParent = cmds.listRelatives(sels[num], p = True)
            name = "%s_Grp"%sels[0]
            grp = cmds.group(n = name, empty =True)
            cmds.matchTransform(grp, sels[num])
            if aParent:
                cmds.parent(grp, aParent)
            cmds.parent(sels[num], grp)
            
    else:
        cmds.error("Stop that. It has yet to work, but you keep doing it.")
#---------------------------------------------------------
def populateMesh():
    selList = cmds.ls(sl = True)
    mesh = selList[0]
    length = len(selList)
    if length > 1:
        for num in range(1, length):
            mesh = cmds.duplicate(mesh)
            sel = selList[num]
            cmds.matchTransform(mesh, sel)
    else:
        cmds.error("You gonna have to select more than that")   








#---------------------------------------------------------
def freezeAttr(tbox, rbox, sbox):
    tQ = cmds.checkBox(tbox, q= True, value = True)
    rQ = cmds.checkBox(rbox, q= True, value = True)
    sQ = cmds.checkBox(sbox, q= True, value = True) 
    
    object = cmds.ls(sl = True)
    if object:
        for sel in object:
            cmds.makeIdentity(sel, 
                              apply = True, 
                              normal = 1,
                              translate = tQ,
                              rotate = rQ,
                              scale = sQ)
    else:
         cmds.error("You can't freeze something if you don't select it, Stupid!")    
#---------------------------------------------------------
def deleteHistory(object):
    if object:
        for sel in object:
            cmds.delete(sel, constructionHistory = True)
            
    else:
        cmds.error("Maya would like to inform you that you suck.",
                   " And that you should probably select something next time.")
#---------------------------------------------------------
def renameHierarchy(myText):
    textQuery = cmds.textField(myText, query = True, text = True)
    sels = cmds.ls(sl = True)
    length = len(sels)
    for num in range(0, length):
        newName = "%s"%textQuery + "_" + str(num).zfill(2)
        sel = sels[num]
        cmds.rename(sel,newName, ignoreShape = True )    
#_____________________WINDOW_FORMAT______________________________#
#Function_Callers
def callJointChain(parentBox, scaleBox, chainBox):
    pQuery  = cmds.checkBox(parentBox, query = True, value  = True)
    sQuery  = cmds.checkBox(scaleBox, query = True, value  = True)
    cQuery = cmds.checkBox(chainBox, query = True, value = True)
    createJointChain(pQuery,sQuery, cQuery)
def rigCall(cIndex, zIndex, sIndex, sbIndex, system, oIndex):
    color = cmds.intSliderGrp(cIndex, query  = True, value = True)
    size = cmds.floatField(zIndex, query = True, value = True)
    shape = cmds.radioCollection(sIndex, query = True, select = True)   
    solver = cmds.checkBox(sbIndex, query = True, value = True)


    if cmds.radioCollection(oIndex[1], query = True, select = True) == "Positive":
        pvOrient = cmds.floatField(oIndex[2], query = True, v = True)
    if cmds.radioCollection(oIndex[1], query = True, select = True) == "Negative":
        pvOrient = -(cmds.floatField(oIndex[2], query = True, v = True))
    orientation = [cmds.radioCollection(oIndex[0], query = True, select = True), pvOrient]
    if system == "IK":             
        createIK(color, shape, size, solver, orientation)
    if system == "FK":
        createFKSystem(color, shape, size)
    if system == "RK":
        createRK(color, shape, size, solver, orientation)


    
#------------------------------------------------------------
#Window_Maker
def attrWindow():
    winName = 'myWindow'
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)    
    mainWindow = cmds.window(winName, title = "Dave's Toolbox",)
    form = cmds.formLayout()
    tabs = cmds.tabLayout()
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
#Generaltab
    general = cmds.rowColumnLayout(numberOfColumns=1)
    outlinerBtn = cmds.button(l = "Launch Outliner", c = lambda x: myOutliner.create())   
    freezeBtn = cmds.button(l='FreezeTransforms', c=lambda x:freezeAttr(tbox, rbox, sbox))
    tbox = cmds.checkBox(l = 'Translate',v=True)
    rbox = cmds.checkBox(l = 'Rotate',v=True)
    sbox = cmds.checkBox(l = 'Scale',v=True)  
    combineBtn = cmds.button(l = "Combine", c = lambda x: combine())
    separateBtn = cmds.button(l = "Separate", c = lambda x: separate())
    deleteBtn = cmds.button(l='DeleteHistory', c=lambda x:deleteHistory(cmds.ls(sl = True)))
    myText = cmds.textField()  
    cmds.textField(myText, e=True, text = "Enter new name")
    renameBtn = cmds.button(l= "Rename Hierarchy",c = lambda x: renameHierarchy(myText))
    grpBtn = cmds.button(l = "Group Items", c = lambda x: grpParent())
    parentScaleBtn = cmds.button(l = "Parent and Scale Constrain", c = lambda x: parentScale())
    populateObjBtn = cmds.button(l = "Populate with first selected Object",c=lambda x:populateMesh())
    cmds.setParent( '..' )
#RiggingCtrls
    rigging = cmds.rowColumnLayout(numberOfColumns=1)
    cmds.text("Control Shape")
    shapeRdCol = cmds.radioCollection("Shapes")
    circleRd = cmds.radioButton("circle",l = "Circle", select = True)
    squareRd = cmds.radioButton("square",l = "Square")
    diamondRd = cmds.radioButton("diamond",l = "Diamond")
    arrowRd = cmds.radioButton("arrow",l = "Arrow")


    cmds.text("Color Index")
    colorValue = cmds.intSliderGrp(min=0, max=16, value=0, step=1, field = True)
    cmds.text("Control Size")
    sizeField = cmds.floatField(min = 0, v =1)
    
    AutoFKbtn = cmds.button(l = "Auto FK System", c = lambda x: rigCall(colorValue,sizeField,shapeRdCol, solverBox, "FK", orientation))
    solverBox = cmds.checkBox(l = "IK Solver", v = True)
    
    cmds.text("Solver Orientation") 
    solverOrientRdCol = cmds.radioCollection("Solver Orientation")
    orientXRd = cmds.radioButton('x',l = 'X')
    orientYRd = cmds.radioButton('y',l = 'Y')
    orientZRd = cmds.radioButton('z',l = 'Z', select = True)
    
    cmds.text("Axis Value")
    orientValueCol = cmds.radioCollection("Axis Value")
    positiveRd = cmds.radioButton('Positive', l = "+", select = True)
    negativeRd = cmds.radioButton('Negative', l = "-")
    
    cmds.text("PoleVector Distance")
    distanceField = cmds.floatField(min = 0, v = 1)
    orientation = [solverOrientRdCol, orientValueCol, distanceField]
    
    AutoIKbtn = cmds.button(p = rigging, l = "Auto IK Solver", c = lambda x: rigCall(colorValue,sizeField,shapeRdCol, solverBox, "IK", orientation))
    AutoRKbtn = cmds.button(p = rigging, l = "Auto RK System", c = lambda x: rigCall(colorValue,sizeField,shapeRdCol, solverBox, "RK", orientation))
    
    cmds.setParent( '..' )
#Rigging/Joints 
    skeleton = cmds.rowColumnLayout()
    scaleBox = cmds.checkBox(l = 'Add Scale Constraint', v=False)
    parentBox = cmds.checkBox(l = 'Add Parent Constraint',v=False)
    chainBox = cmds.checkBox(l = 'Create Chain From Joints', v = True)
    jointChainBtn = cmds.button(l = "Create Joint Chain", c = lambda x: callJointChain(parentBox, scaleBox, chainBox))
    toggleBtn = cmds.button(l = "Toggle Axis Display", c = lambda x: toggleAxisDisplay())
    cmds.setParent( '..' )
#TabLayout
    cmds.tabLayout( tabs, edit=True, tabLabel=((general, 'General'),(rigging, 'Rigging'), (skeleton, 'Joints')) )
#-------------------------------------------------------   
    cmds.showWindow(winName)
#---------------------------------------------------------
attrWindow()
#_________________OUTLINER__________________________
#OutLiner
class Outliner():
    def __init__(self):
        self.control_name = 'myOutliner'
        self.nodeTypes = ['joint',
                          'clusterHandle',
                          'mesh',
                          'nurbsCurve',
                          'parentConstraint',
                          'scaleConstraint',
                          'locator',
                          'lattice',
                          'camera']  
        self.filterItems = [] 
    def clearList(self):
        cmds.textScrollList(self.filterList, edit = True, removeAll = True)
    def addSelectedItem(self):
        sel = cmds.ls(sl = True)
        self.filterItems.extend(sel)
        self.clearList
        cmds.textScrollList(self.filterList, edit = True, append = self.filterItems)
    def removeSelectedItem(self):
        sel = cmds.ls(sl = True)
        for item in sel:
            self.filterItems.remove(item)
        self.clearList()
        cmds.textScrollList(self.filterList, edit = True, append = self.filterItems)
    def selectItem(self):
        itemQuery = cmds.textScrollList(self.filterList, query = True, selectItem = True)
        cmds.select(itemQuery)         
    def displayList(self):
        self.filterItems = []
        filterNodes = []
        nodeQuery = cmds.textScrollList(self.nodeList, query = True, selectItem = True)
        for num in nodeQuery:
            filterNodes = cmds.ls(type = "%s"%num)
            self.filterItems.extend(filterNodes)
        self.filterItems = self.sortList(self.filterItems)
        cmds.textScrollList(self.filterList, edit = True, removeAll = True)
        cmds.textScrollList(self.filterList, edit = True, append = self.filterItems)
    def selectAll(self):
        query = cmds.textScrollList(self.filterList, q = True, allItems = True)
        cmds.textScrollList(self.filterList, e = True, selectItem=query)
        self.selectItem()
    def moveItem(self, num):
        sel = cmds.ls(sl = True)[0]
        index = self.filterItems.index(sel)
        index = index + num
        self.filterItems.remove(sel)
        self.filterItems.insert(index, sel)
        cmds.textScrollList(self.filterList, edit = True, removeAll = True)
        cmds.textScrollList(self.filterList, edit = True, append = self.filterItems, selectItem = sel)
        
    def create(self):
        self.delete()
        self.myWindow= cmds.window(self.control_name)
        self.Main_Column = cmds.columnLayout()
        addBtn = cmds.button(l = "Add", c = lambda X: self.addSelectedItem()) 
        removeBtn = cmds.button(l = "Remove", c= lambda X: self.removeSelectedItem())
        clearBtn = cmds.button("ClearList", c = lambda X: self.clearList())
        upBtn = cmds.button("Move Item Up", c = lambda X: self.moveItem(-1))
        downBtn = cmds.button("Move Item Down", c = lambda X: self.moveItem(1))
        self.pane = cmds.paneLayout('Scroll Lists', configuration='vertical2',
                                    staticWidthPane = 1,
                                    p = self.myWindow)     
        self.nodeList = cmds.textScrollList(parent = self.pane,
                                            append = self.nodeTypes,
                                            allowMultiSelection = True,
                                            selectCommand = lambda: self.displayList())
        self.filterList = cmds.textScrollList(parent = self.pane,
                                              allowMultiSelection = True,
                                              selectCommand = lambda: self.selectItem(),
                                              doubleClickCommand = lambda: self.selectAll(),
                                              deleteKeyCommand = lambda: self.removeSelectedItem())    
        self.topRow = cmds.rowLayout(parent = self.myWindow)
        
        cmds.showWindow()
    def delete(self):
        if cmds.window(self.control_name, exists = True):
            cmds.deleteUI(self.control_name)
    def sortList(self, list):
        sortedList = sorted(list)
        return sortedList
myOutliner = Outliner()