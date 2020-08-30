# joint_functions
# 2017-12-07
# EDITED: 2020-08-25
# ============================================
import maya.cmds as cmds
import maya.mel as mel

local_axis_on = False


def show_joint_attr():
    '''Toggles Joint Orients, Scale Compensate, and DisplayLocalAxis for all joints'''
    sels = cmds.ls(type='joint')
    for sel in sels:
        value = 1 - cmds.getAttr('%s.jointOrientX' % sel, k=True)
        cmds.setAttr('%s.jointOrientX' % sel, lock=False, keyable=value)
        cmds.setAttr('%s.jointOrientY' % sel, lock=False, keyable=value)
        cmds.setAttr('%s.jointOrientZ' % sel, lock=False, keyable=value)
        cmds.setAttr('%s.segmentScaleCompensate' % sel, keyable=value)

def scale_compensate(onOff):
    '''Toggles scale compensate for all joints'''
    sels = cmds.ls(type='joint')
    for sel in sels:
        cmds.setAttr('%s.segmentScaleCompensate' % sel, onOff)


def display_orient_joint_options():
    '''Opens Orient Joint options window'''
    mel.eval('OrientJointOptions')


def display_local_axis():
    '''Toggles local axis for all joints'''
    # toggle bool
    global local_axis_on
    local_axis_on = 1 - local_axis_on

    # loop through joints
    sels = cmds.ls(type='joint')
    for sel in sels:
        cmds.setAttr('%s.displayLocalAxis' % sel, local_axis_on)
