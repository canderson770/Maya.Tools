#toolbox
#2017-11-30
#============================================
import maya.cmds as cmds
import maya.mel as mel
import rename_functions
import joint_functions
import fk_systems
import simple_functions

reload(rename_functions)
reload(joint_functions)


#my_toolbox_window()
def create_my_toolbox():
	#my_toolbox_window =  'my_toolbox_window'
    
	#if cmds.window(my_toolbox_window, exists=True):
		#cmds.deleteUI(my_toolbox_window, window=True)
        
	#my_toolbox_window = cmds.window(my_toolbox_window, title='My Toolbox', minimizeButton=False, maximizeButton=False)
    
	main_column = cmds.columnLayout(adjustableColumn=True, columnAlign='center')
    
	image_row = cmds.rowLayout(parent=main_column, numberOfColumns=2, adjustableColumn=2, columnAlign=(2,'center'), backgroundColor=(1,1,1))
	my_image = cmds.picture(image='logo-32.png', parent=image_row)
	my_name = cmds.text(label='Cody Anderson', parent=image_row)
	
	my_tabs = cmds.tabLayout(parent=main_column)
	
	###tab 1
	tab_1_column = cmds.columnLayout(adjustableColumn=True, columnAlign='center', parent=my_tabs)
	
	#Simple tools
	cmds.separator(height=12, parent=tab_1_column)
	delete_history_button = cmds.button(parent=tab_1_column, label='Delete History', command=lambda *args: simple_functions.delete_history())
	freeze_transform_button = cmds.button(parent=tab_1_column, label='Freeze Transformations', command=lambda *args: simple_functions.freeze_transformations())
	center_pivot_button = cmds.button(parent=tab_1_column, label='Center Pivot', command=lambda *args: simple_functions.center_pivot())
	parent_scale_button = cmds.button(parent=tab_1_column, label='Parent and Scale Constrain', command=lambda *args: simple_functions.parent_scale_constrain())
	
    #Poly Count
	cmds.separator(height=12, parent=tab_1_column)
	poly_count_button = cmds.button(parent=tab_1_column, label='Poly Count', command=lambda *args: simple_functions.toggle_poly_count())
	
	#Orient Joint
	cmds.separator(height=12, parent=tab_1_column)
	orient_joint_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=2, columnWidth=(1, 125), adjustableColumn=2, columnAttach=(1, 'both', 0))
	orient_joint_button = cmds.button(parent=orient_joint_row, label='Orient Joint Options', command='')
	display_axis_toggle = cmds.iconTextButton(style='iconOnly', image1='channelBoxUseManips.png', parent=orient_joint_row, command=lambda *args: joint_functions.display_local_axis())
	
	#Scale Compensation
	cmds.separator(height=12, parent=tab_1_column)
	scale_comp_label = cmds.text(label='Scale Compensation', parent=tab_1_column)
	scale_comp_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=2, columnWidth=(1, 75), adjustableColumn=2, columnAttach=(1, "both", 0))
	scale_comp_on_button = cmds.button(parent=scale_comp_row, label='On', command='')
	scale_comp_off_button = cmds.button(parent=scale_comp_row, label='Off', command='')
	
	
	cmds.separator(height=12, parent=tab_1_column)
	create_joints_button = cmds.button(parent=tab_1_column, label='Turn Selection into Joints', command='')
	place_controls_button = cmds.button(parent=tab_1_column, label='Place Controls', command='')
	
	#Locator
	cmds.separator(height=12, parent=tab_1_column)
	locator_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=3, columnWidth=(1, 62), adjustableColumn=2, columnAttach = (1, 'both', 0))
	create_locator_button = cmds.button(parent=locator_row, label='Locators', command='')
	locator_buttons = cmds.radioCollection(parent=locator_row)
	locator_button_1 = cmds.radioButton(label='Each', changeCommand='')
	locator_button_2 = cmds.radioButton(label='All', changeCommand='')
	cmds.radioCollection(locator_buttons, edit=True, select=locator_button_1)
	
	#Rename Functions
	cmds.separator(height=12, parent=tab_1_column)
	rename_button = cmds.button(parent=tab_1_column, label='Rename', command='')
	search_and_replace_button = cmds.button(parent=tab_1_column, label='Search And Replace', command=lambda *args: rename_functions.search_and_replace())

	#Auto rigs
	cmds.separator(height=12, parent=tab_1_column)
	auto_rigs_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=4, columnAlign=(2, 'left'))
	fk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='FK', parent= auto_rigs_row, command='')
	broken_fk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='Broken', parent= auto_rigs_row, command='')
	ik_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinHandle.png', label='IK', parent= auto_rigs_row, command='')
	rk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='RK', parent= auto_rigs_row, command='')
	
	#####tab 2
	tab_2_column = cmds.columnLayout(adjustableColumn=True, columnAlign='center', parent=my_tabs)
	
	cmds.separator(height=12, parent=tab_1_column)
	random_placement_button = cmds.button(parent=tab_2_column, label='Random Placement', command='')
	
	cmds.separator(height=12, parent=tab_1_column)
	other_label = cmds.text(label='...', parent=tab_2_column)
	
	cmds.tabLayout(my_tabs, edit=True, tabLabel=[(tab_1_column, 'Main'), (tab_2_column, 'Other')])
	
	date = cmds.text(label='2017', parent=main_column, align='right')
	
	#cmds.showWindow(my_toolbox_window)
    
def my_toolbox_window():
    my_workspace  = 'My Workspace'
    
    #if cmds.workspaceControl(my_workspace, exists=False)
    #if (cmds.workspaceControl(my_workspace, exists=True)):
    #    cmds.deleteUI(my_workspace)
        
    #if not cmds.objExists(my_workspace):
    my_workspace = cmds.workspaceControl(my_workspace, retain=False, floating=False, label='Cody', widthProperty='preferred', initialWidth=160, initialHeight=560, resizeWidth=160, resizeHeight=560, uiScript='create_my_toolbox()')

	#if cmds.workspaceControl(my_workspace, q=True, visible=False):
    #	cmds.workspaceControl(my_workspace, restore=True)
