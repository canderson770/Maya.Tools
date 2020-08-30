# rename_functions
# 2017-12-07
# EDITED: 2020-08-25
# ============================================
import maya.cmds as cmds
import maya.mel as mel
import re


def sequential_renamer(new_name):
    '''Renames selection sequentially'''
    # Get selection
    sels = cmds.ls(sl=True, tr=True)

    # if only one item selected, check of children
    if len(sels) == 1:
        cmds.select(hi=True)
        sels = cmds.ls(sl=True, tr=True)

    # loop and rename selection
    for index, sel in enumerate(sels):
        i = index + 1
        # if only one selected item, don't put number
        if len(sels) == 1: i = ''
        
        # rename
        if('#' in new_name):
            cmds.rename(sel, re.sub('#', str(i), new_name))
        else:
            cmds.rename(sel, new_name + str(i))


def search_and_replace():
    '''Opens Search and Replace window'''
    mel.eval('performSearchReplaceNames 1;')
    
    
def rename_prompt():
    '''Shows dialog prompt to enter name'''
    result = cmds.promptDialog(title='Rename', message='Enter Name:', button=('OK','Cancel'), defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        sequential_renamer(cmds.promptDialog(q=True, text=True))