#create_joints
#2017-11-06
#============================================
import maya.cmds as cmds

#convert_to_joints(False)
def convert_to_joints(checkbox):
    '''Creates joints at selection. Will replace selection if the parameter is True'''
    sels = cmds.ls(sl=True)
    last_jnt = ''
    replace = cmds.checkBox(checkbox, q=True, value=True)

    for sel in sels:
        cmds.select(clear=True)
        pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
        jnt = cmds.joint(position=pos, absolute=True)
        
        if replace == True:
            cmds.delete(sel)
        
        if last_jnt != '':
            cmds.parent(jnt, last_jnt)

        last_jnt = jnt