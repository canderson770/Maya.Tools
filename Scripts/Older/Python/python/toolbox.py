#toolbox
#2017-11-30
#============================================
import maya.cmds as cmds
import maya.mel as mel

import rename_functions
import joint_functions
import fk_systems
import simple_functions
import custom_outliner
import create_joints
import create_controls
import create_locator
import custom_outliner
import random_placement
import custom_animation_window

reload(rename_functions)
reload(joint_functions)
reload(fk_systems)
reload(simple_functions)
reload(custom_outliner)
reload(create_joints)
reload(create_controls)
reload(create_locator)
reload(custom_outliner)
reload(random_placement)
reload(custom_animation_window)

#my_toolbox_window()
def create_my_toolbox():
	my_window = 'myToolboxWindow'
    
	if cmds.window(my_window, q=True, exists=True):
	    cmds.deleteUI(my_window)

	my_window = cmds.window(my_window, width=160, height=570)    
    
	main_column = cmds.columnLayout(parent=my_window, adjustableColumn=True, columnAlign='center')
    
	image_row = cmds.rowLayout(parent=main_column, numberOfColumns=2, adjustableColumn=2, columnAlign=(2,'center'), backgroundColor=(1,1,1))
	my_image = cmds.picture(image='logo-32.png', parent=image_row)
	my_name = cmds.text(label='Cody Anderson', parent=image_row)
	
	my_tabs = cmds.tabLayout(parent=main_column)
	
	###tab 1
	tab_1_column = cmds.columnLayout(adjustableColumn=True, columnAlign='center', parent=my_tabs)
	
	#Simple tools
	cmds.separator(height=12, parent=tab_1_column)
	delete_history_button = cmds.button(parent=tab_1_column, label='Delete History', annotation='Delete history', command=lambda *args: simple_functions.delete_history())
	freeze_transform_button = cmds.button(parent=tab_1_column, label='Freeze Transformations', annotation='Freeze all transformations', command=lambda *args: simple_functions.freeze_transformations())
	center_pivot_button = cmds.button(parent=tab_1_column, label='Center Pivot', annotation='Center pivot', command=lambda *args: simple_functions.center_pivot())
	parent_scale_button = cmds.button(parent=tab_1_column, label='Parent and Scale Constrain', annotation='Parent and scale constrain', command=lambda *args: simple_functions.parent_scale_constrain())
	
    #Poly Count
	cmds.separator(height=12, parent=tab_1_column)
	poly_count_button = cmds.button(parent=tab_1_column, label='Poly Count', annotation='Toggle poly count', command=lambda *args: simple_functions.toggle_poly_count())
	
	#Orient Joint
	cmds.separator(height=12, parent=tab_1_column)
	orient_joint_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=2, columnWidth=(1, 125), adjustableColumn=2, columnAttach=(1, 'both', 0))
	orient_joint_button = cmds.button(parent=orient_joint_row, label='Orient Joint Options', annotation='Display orient joint options', command=lambda *args: joint_functions.display_orient_joint_options())
	display_axis_toggle = cmds.iconTextButton(style='iconOnly', image1='channelBoxUseManips.png', annotation='Toggle display axis for all joints', parent=orient_joint_row, command=lambda *args: joint_functions.display_local_axis())
	orient_channelbox_button = cmds.button(parent=tab_1_column, label='Joint Attributes', annotation='Unhide more joint attributes', command=lambda *args: joint_functions.show_joint_attr())
	
	#Scale Compensation
	cmds.separator(height=12, parent=tab_1_column)
	scale_comp_label = cmds.text(label='Scale Compensation', parent=tab_1_column)
	scale_comp_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=2, columnWidth=(1, 75), adjustableColumn=2, columnAttach=(1, "both", 0))
	scale_comp_on_button = cmds.button(parent=scale_comp_row, label='On', annotation='Turn scale compensation on', command=lambda *args: joint_functions.scale_compensate(1))
	scale_comp_off_button = cmds.button(parent=scale_comp_row, label='Off', annotation='Turn scale compensation off', command=lambda *args: joint_functions.scale_compensate(0))
	
	#Covert to Joints
	cmds.separator(height=12, parent=tab_1_column)
	create_joints_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=2, columnWidth=(1, 110), adjustableColumn=2, columnAttach = (1, 'left', 0))
	create_joints_button = cmds.button(parent=create_joints_row, label='Selection to Joints', annotation='Turn selection into joints', command=lambda *args: create_joints.convert_to_joints(create_joints_checkbox))
	create_joints_checkbox = cmds.checkBox(parent=create_joints_row, label='Del', annotation='Toggle to replace selection with joints', align='right')

    #Place Controls
	place_controls_button = cmds.button(parent=tab_1_column, label='Place Controls', annotation='Place controls at selection', command=lambda *args: create_controls.place_controls())
	
	#Locator
	cmds.separator(height=12, parent=tab_1_column)
	locator_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=3, columnWidth=(1, 62), adjustableColumn=2, columnAttach = (1, 'both', 0))
	create_locator_button = cmds.button(parent=locator_row, label='Locators', annotation='Create locator(s)', command=lambda *args: create_locator.center_locator(locator_buttons))
	locator_buttons = cmds.radioCollection(parent=locator_row)
	locator_button_1 = cmds.radioButton(label='Each', annotation='Create locator at each selection')
	locator_button_2 = cmds.radioButton(label='All', annotation='Create locator at center of entire selection')
	cmds.radioCollection(locator_buttons, edit=True, select=locator_button_1)
	
	#Rename Functions
	cmds.separator(height=12, parent=tab_1_column)
	rename_button = cmds.button(parent=tab_1_column, label='Rename', annotation='Sequential renamer', command=lambda *args: rename_functions.rename_prompt())
	search_and_replace_button = cmds.button(parent=tab_1_column, label='Search And Replace', annotation='Search and replace', command=lambda *args: rename_functions.search_and_replace())

	#Auto rigs
	cmds.separator(height=12, parent=tab_1_column)
	auto_rigs_row = cmds.rowLayout(parent=tab_1_column, numberOfColumns=4, columnAlign=(2, 'left'))
	fk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='FK', annotation='Creates an FK rig. Select first joint of chain then run', parent= auto_rigs_row, command=lambda *args: fk_systems.simple_fk())
	broken_fk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='Broken', annotation='Creates an broken FK rig. Select first joint of chain then run', parent= auto_rigs_row, command=lambda *args: fk_systems.broken_fk())
	#ik_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinHandle.png', label='IK', annotation='Creates an IK rig. Select first joint of chain then run', parent= auto_rigs_row, command='')
	#rk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='RK', annotation='Creates an RK rig. Select first joint of chain then run', parent= auto_rigs_row, command='')
	
	#Outliner
	cmds.separator(height=12, parent=tab_1_column)
	custom_outliner_button = cmds.button(parent=tab_1_column, label='Custom Outliner', annotation='Open custom outliner', command=lambda *args: custom_outliner.custom_outliner())
	
	#Animation Window
	cmds.separator(height=12, parent=tab_1_column)
	custom_outliner_button = cmds.button(parent=tab_1_column, label='Animator', annotation='Open animation master', command=lambda *args: custom_animation_window.custom_animation())
	
	#####tab 2
	tab_2_column = cmds.columnLayout(adjustableColumn=True, columnAlign='center', parent=my_tabs)
	
	cmds.separator(height=12, parent=tab_2_column)
	random_placement_button = cmds.button(parent=tab_2_column, label='Random Placement', annotation='Random placement options', command=lambda *args: random_placement.random_placement_prompt())
	
	cmds.separator(height=12, parent=tab_2_column)
	other_label = cmds.text(label='...', parent=tab_2_column)
	
	cmds.tabLayout(my_tabs, edit=True, tabLabel=[(tab_1_column, 'Main'), (tab_2_column, 'Other')])
	
	date = cmds.text(label='2017', parent=main_column, align='right')
	
	cmds.showWindow(my_window)
    
def my_toolbox_window():
    my_workspace  = 'My Workspace'
    
    if cmds.workspaceControl(my_workspace, exists=True):
        cmds.workspaceControl(my_workspace, e=True, close=True)
        
    my_workspace = cmds.workspaceControl(my_workspace, retain=False, floating=False, label='Cody', widthProperty='preferred', 
        initialWidth=160, initialHeight=570, resizeWidth=160, resizeHeight=560, uiScript='create_my_toolbox()')

#print(cmds.about(version=True))
#create_my_toolbox()
#my_toolbox_window()