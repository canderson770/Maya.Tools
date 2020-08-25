# START UP SCRIPT
# EDITED: 2020-08-25
# ============================================
import maya
import toolbox

maya.utils.executeDeferred(toolbox.dockable_toolbox, standalone=True)