#rename_functions
#2017-12-07
#============================================
import maya.cmds as cmds
import maya.mel as mel

#sequential_renamer('Test Ctrl')
def sequential_renamer(name):
    '''Renames selection sequentially'''

    #Get selection with hierarchy
    cmds.select(hi=True)
    sels = cmds.ls(sl=True)
    
    for index, sel in enumerate(sels):
        if '#' in name:
            new_name = name.replace('#', '%i')
            i = index + 1
            cmds.rename(sel, new_name % i)
        else:
            cmds.rename(sel, name)
        
def search_and_replace():
    mel.eval('performSearchReplaceNames 1;')
    
    
def rename_prompt():
    result = cmds.promptDialog(title='Rename', message='Enter Name:', button=('OK','Cancel'), defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    
    if result == 'OK':
        sequential_renamer(cmds.promptDialog(q=True, text=True))