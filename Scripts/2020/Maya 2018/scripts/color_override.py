import maya.cmds as cmds
import re


def change_color(index, enabled):
    '''Sets override color number and enable status'''
    if(index>32):
        index = 32
    index = index-1
    sels = cmds.ls(sl=True)
    for sel in sels:
        shapes = cmds.listRelatives(sel, shapes=True)
        for shape in shapes:
            cmds.setAttr("{0}.overrideEnabled".format(shape), enabled)
            cmds.setAttr("{0}.overrideColor".format(shape), index)


def default_color():
    '''Changes override color to 0 and disables override'''
    change_color(1, False)


def change_color_slider(slider):
    '''Sets override color from a colorIndexSliderGrp '''
    # fix name issue if using a dockControl instead of just a window
    if(cmds.colorIndexSliderGrp(slider, q=True, exists=True) == False):
        slider = re.sub('CSAToolboxWindow', 'MayaWindow', slider)

    # check for slider
    if(cmds.colorIndexSliderGrp(slider, q=True, exists=True)):
        # get value from slider
        value = cmds.colorIndexSliderGrp(slider, q=True, value=True)
        # set color
        change_color(value, True)
    else:
        print(slider+ ' not found')