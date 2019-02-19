import maya.cmds as cmds


def make_joints_at():
    sels = cmds.ls(sl=True)
    last_jnt = ''

    for sel in sels:
        cmds.select(clear=True)
        pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
        jnt = cmds.joint(position=pos, absolute=True)

        if last_jnt != '':
            cmds.parent(jnt, last_jnt)

        last_jnt = jnt

make_joints_at()