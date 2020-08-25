#create_controls
#2017-11-06
#============================================
import maya.cmds as cmds


def place_controls():
    '''Creates controls at selection'''
    
    #Get selection with hierarchy
    cmds.select(hi=True)
    sels = cmds.ls(sl=True)
    
    #Loop through selection
    for sel in sels:
        #Set up control names
        ctrl_name = '%s__Ctrl' % sel
        grp_name = '%s__Grp' % sel
        
        #Create control and control group    
        ctrl = cmds.circle(c=(0,0,0), nr=(1,0,0), sw=360, r=1, d=3, ut=0, tol=0, s=8, ch=1, n=ctrl_name)  
        grp = cmds.group(ctrl, n=grp_name)
        
        #Match control group to joint transform
        pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
        rot = cmds.xform(sel, q=True, ro=True, ws=True)
        cmds.move(pos[0],pos[1],pos[2], grp, ws=True, a=True, rpr=True)
        cmds.rotate(rot[0],rot[1],rot[2], grp, a=True, ws=True)