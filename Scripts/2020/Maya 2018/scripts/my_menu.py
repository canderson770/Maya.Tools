# Creates new option in main menu bar
# EDITED: 2020-08-25
# ============================================
import pymel.core as pm
import toolbox

def create_my_menu(standalone=False):
    '''Creates a CSA menu with my scripts'''
    reload(toolbox)

    # find main maya window
    main_maya_window = pm.language.melGlobals['gMainWindow']

    # check of menu exists
    if pm.menu('CSA', exists=True): pm.deleteUI('CSA')

    # create a new menu and parent to main maya window
    custom_menu = pm.menu('CSA', parent=main_maya_window)

    # Build a menu item and parent under the 'customMenu'
    pm.menuItem(label='Open Toolbox', parent=custom_menu, command=lambda *args: toolbox.create_my_toolbox())

    toolbox.create_my_toolbox()