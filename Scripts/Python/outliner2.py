#custom_outliner
#2017-12-05
#============================================
import maya.cmds as cmds

def custom_outliner():        
    custom_outliner_window =  'custom_outliner'

    if cmds.window(custom_outliner_window, exists=True):
        cmds.deleteUI(custom_outliner_window, window=True)

    custom_outliner_window = cmds.window(custom_outliner_window, title='Control Creator', minimizeButton=False, maximizeButton=False)
    
    custom_outliner_column = cmds.columnLayout(parent=custom_outliner_window, adjustableColumn=True)
    custom_outliner_row_buttons = cmds.rowLayout(parent=custom_outliner_column, numberOfColumns=6)
    custom_outliner_list = cmds.textScrollList(parent=custom_outliner_column, height=580, width=225, allowMultiSelection=True, deleteKeyCommand='outliner_remove(custom_outliner_list)', selectCommand='outliner_select(custom_outliner_list)')
    custom_outliner_add_button = cmds.button(parent=custom_outliner_row_buttons, label='Add', command='outliner_add(custom_outliner_list)')
    custom_outliner_remove_button =cmds.button(parent=custom_outliner_row_buttons, label='Remove', command='outliner_remove(custom_outliner_list)')
    custom_outliner_clear_button = cmds.button(parent=custom_outliner_row_buttons, label='Clear', command='outliner_clear(custom_outliner_list)')
    custom_outliner_sort_button = cmds.button(parent=custom_outliner_row_buttons, label='Sort', command='outliner_sort(custom_outliner_list)')
    custom_outliner_up_button = cmds.button(parent=custom_outliner_row_buttons, label='Up', command='outliner_up(custom_outliner_list)')
    custom_outliner_down_button = cmds.button(parent=custom_outliner_row_buttons, label='Down', command='outliner_down(custom_outliner_list)')
    cmds.window(custom_outliner_window, edit=True, widthHeight=(230, 610))
    cmds.showWindow(custom_outliner_window)

def outliner_select(custom_outliner_list):
    select_items = cmds.textScrollList(custom_outliner_list, q=True, selectItem=True)
    cmds.select(select_items)

def outliner_add(custom_outliner_list):
    sels = cmds.ls(sl=True)
    cmds.textScrollList(custom_outliner_list, e=True, removeAll=True)
    cmds.textScrollList(custom_outliner_list, e=True, append=sels)
    
def outliner_remove(custom_outliner_list):
    sels = cmds.ls(sl=True)
    cmds.textScrollList(custom_outliner_list, e=True, removeItem=sels)
    
def outliner_clear(custom_outliner_list):
    cmds.textScrollList(custom_outliner_list, e=True, removeAll=True)

def outliner_sort(custom_outliner_list):
    sorted_list = sorted(cmds.textScrollList(custom_outliner_list, q=True, allItems=True))
    cmds.textScrollList(custom_outliner_list, e=True, removeAll=True)
    cmds.textScrollList(custom_outliner_list, e=True, append=sorted_list)
    
def outliner_up(custom_outliner_list):
    sels = cmds.textScrollList(custom_outliner_list, q=True, selectItem=True)
    if len(sels) < 2:
        oldIndex = cmds.textScrollList(custom_outliner_list, q=True, selectIndexedItem=True)
        if oldIndex[0] > 1:
            newIndex = oldIndex[0] - 1
            cmds.textScrollList(custom_outliner_list, e=True, removeItem=sels)
            cmds.textScrollList(custom_outliner_list, e=True, appendPosition=(newIndex, sels[0]))
            cmds.textScrollList(custom_outliner_list, e=True, selectItem=sels)
    
def outliner_down(custom_outliner_list):
    sels = cmds.textScrollList(custom_outliner_list, q=True, selectItem=True)
    if len(sels) < 2:
        oldIndex = cmds.textScrollList(custom_outliner_list, q=True, selectIndexedItem=True)
        num_items = cmds.textScrollList(custom_outliner_list, q=True, numberOfItems=True)
        if oldIndex[0] < num_items:
            newIndex = oldIndex[0] + 1
            cmds.textScrollList(custom_outliner_list, e=True, removeItem=sels)
            cmds.textScrollList(custom_outliner_list, e=True, appendPosition=(newIndex, sels[0]))
            cmds.textScrollList(custom_outliner_list, e=True, selectItem=sels)