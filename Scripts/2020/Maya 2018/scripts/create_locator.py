#create_locator
#2017-11-06
#============================================
import maya.cmds as cmds

def center_locator(locator_buttons):
    '''Creates locator at each selection or center of all selections'''
    
    sels = cmds.ls(sl=True)
    saved_sel = []
    radio_button = cmds.radioCollection(locator_buttons, q=True, select=True)
    type =  cmds.radioButton(radio_button, q=True, label=True)
    
    if type == 'Each':
        for sel in sels:
            #make locator
            locator = cmds.spaceLocator(n='%s_Locator' % sel)
            
            #move/rotate locator to match sel        
            pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
            rot = cmds.xform(sel, q=True, ro=True, ws=True)
            cmds.move(pos[0],pos[1],pos[2], locator, ws=True, a=True, rpr=True)
            cmds.rotate(rot[0],rot[1],rot[2], locator, a=True, ws=True)
            
            #freeze transforms
            cmds.makeIdentity(locator, apply=True)
            
            saved_sel.append(locator)
            
        cmds.select(clear=True)
        for sel in saved_sel:
            cmds.select(sel, add=True)
            
    elif type == 'All':
		bbox = cmds.exactWorldBoundingBox()

		pos = [0,0,0]
		pos[0] = ((bbox[0] + bbox[3]) / 2) #X cord =(X min - X max)/2
		pos[1] = ((bbox[1] + bbox[4]) / 2) #Y cord =(Y min - Y max)/2
		pos[2] = ((bbox[2] + bbox[5]) / 2) #Z cord =(Z min - Z max)/2

		main_locator = cmds.spaceLocator()
		cmds.move(pos[0],pos[1],pos[2], main_locator, ws=True, a=True, rpr=True)
		cmds.select(main_locator, r=True)
