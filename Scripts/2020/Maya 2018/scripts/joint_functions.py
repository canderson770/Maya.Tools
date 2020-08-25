#joint_functions
#2017-12-07
#============================================
import maya.cmds as cmds
import maya.mel as mel


def show_joint_attr():
    '''Unhides Joint Orients, Scale Compensate, and DisplayLocalAxis'''
    
    sels = cmds.ls(type='joint')
    
    for sel in sels:
        cmds.setAttr('%s.jointOrientX' % sel, lock=False, keyable=True)
        cmds.setAttr('%s.jointOrientY' % sel, lock=False, keyable=True)
        cmds.setAttr('%s.jointOrientZ' % sel, lock=False, keyable=True)
        #cmds.setAttr('%s.displayLocalAxis' % sel, lock=False, keyable=True)
        cmds.setAttr('%s.segmentScaleCompensate' % sel, keyable=True)
        
        
def scale_compensate(onOff):

    sels = cmds.ls(type='joint')
    
    for sel in sels:
        cmds.setAttr('%s.segmentScaleCompensate' % sel, onOff)

def display_orient_joint_options():
    mel.eval('OrientJointOptions')

def display_local_axis():
    
    sels = cmds.ls(type='joint')

    for sel in sels:
        value = cmds.getAttr('%s.displayLocalAxis' % sel)
        value = 1 - value
        cmds.setAttr('%s.displayLocalAxis' % sel, value)   
        
        
#Match Transforms     
        