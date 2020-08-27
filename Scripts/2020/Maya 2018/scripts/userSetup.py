# START UP SCRIPT
# EDITED: 2020-08-25
# ============================================
import maya
import my_menu

maya.utils.executeDeferred(my_menu.create_my_menu, standalone=True)
