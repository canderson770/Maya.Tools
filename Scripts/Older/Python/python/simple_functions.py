#simple_functions
#2017-11-30
#============================================
import maya.cmds as cmds
import maya.mel as mel


def delete_history():
    cmds.delete(ch=True)
    
def freeze_transformations():
    cmds.makeIdentity(apply=True)
    
def center_pivot():
    cmds.xform(centerPivots=True)
    
def parent_scale_constrain():
    cmds.parentConstraint()
    cmds.scaleConstraint()
    
def toggle_poly_count():
    mel.eval('TogglePolyCount')