import maya.cmds as cmds


def control_window():
    '''Builds an interface for control creation.'''

    # asssign object name for window UI object
    m_window =  'ctrlWindow'

    #delete the window if it already exists
    if cmds.window(m_window, exists=True):
        cmds.deleteUI(m_window, window=True)

    #create window and column
    m_window = cmds.window(m_window, title='Control Creator', sizeable=False)
    m_column = cmds.columnLayout(adjustableColumn=True, columnAttach=['both',2], parent=m_window)

    #create buttons and fields
    circle_btn = cmds.button(parent=m_column, label='Circle')
    square_btn = cmds.button(parent=m_column, label='Square')
    cube_btn = cmds.button(parent=m_column, label='Cube')

    txt_field = cmds.textFieldGrp(parent=m_column, label='Control Name', placeholderText='Enter name')
    float_field = cmds.floatSliderGrp(parent=m_column, label='Size', minValue=0, maxValue=10, field=1, value=1)

    #edit flag to add commands
    cmds.button(circle_btn, e=True, command="CreateControl('cirlce', %s, %s) % (txt_field, float_field)")
    cmds.button(square_btn, e=True, command="CreateControl('square', %s, %s) % (txt_field, float_field)")
    cmds.button(cube_btn, e=True, command="CreateControl('cube', %s, %s) % (txt_field, float_field)")

    cmds.window(m_window, e=True, width=400, height=125)
    cmds.showWindow(m_window)
    