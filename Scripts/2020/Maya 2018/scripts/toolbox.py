# TOOLBOX
# Created: 2017-11-30
# EDITED: 2020-08-27
#============================================
import maya.cmds as cmds
import maya.mel as mel
import rename_functions
import joint_functions
import auto_rigs
import simple_functions
import custom_outliner
import create_joints
import create_controls
import create_locator
import custom_outliner
import random_placement
import custom_animation_window


def create_my_toolbox(standalone=False):
	'''Create my toolbox dockable window'''
	# Reload scripts
	reload(rename_functions)
	reload(joint_functions)
	reload(auto_rigs)
	reload(simple_functions)
	reload(custom_outliner)
	reload(create_joints)
	reload(create_controls)
	reload(create_locator)
	reload(custom_outliner)
	reload(random_placement)
	reload(custom_animation_window)

	# Create window
	my_window = 'CSAToolboxWindow'
	if cmds.window(my_window, q=True, exists=True): cmds.deleteUI(my_window)
	my_window = cmds.window(my_window, width=160, height=570)

    # Create main column
	main_column = cmds.columnLayout(p=my_window, adjustableColumn=True, columnAlign='center')

	# Create header
	image_row = cmds.rowLayout(p=main_column, nc=2, adjustableColumn=2, columnAlign=(2,'center'), bgc=(1,1,1))
	my_image = cmds.picture(p=image_row, image='logo-32.png')
	my_name = cmds.text(p=image_row, label='Cody Anderson')

	# Create tab layout
	my_tabs = cmds.tabLayout(p=main_column)
	
	# Tab 1
	tab_1_column = cmds.columnLayout(p=my_tabs, adjustableColumn=True, columnAlign='center')
	
	# Simple modeling tools
	cmds.separator(p=tab_1_column, height=12)
	delete_history_button = cmds.button(p=tab_1_column, l='Delete History', ann='Delete history',
										command=lambda *args: simple_functions.delete_history())
	freeze_transform_button = cmds.button(p=tab_1_column, l='Freeze Transformations', ann='Freeze all transformations',
										command=lambda *args: simple_functions.freeze_transformations())
	center_pivot_button = cmds.button(p=tab_1_column, l='Center Pivot', ann='Center pivot',
										command=lambda *args: simple_functions.center_pivot())
	parent_scale_button = cmds.button(p=tab_1_column, l='Parent and Scale Constrain', ann='Parent and scale constrain',
										command=lambda *args: simple_functions.parent_scale_constrain())
	
    # Poly Count
	cmds.separator(p=tab_1_column, height=12)
	poly_count_button = cmds.button(p=tab_1_column, l='Poly Count', ann='Toggle poly count',
										command=lambda *args: simple_functions.toggle_poly_count())
	
	#Orient Joint
	cmds.separator(p=tab_1_column, height=12)
  	orient_joint_row = cmds.rowLayout(p=tab_1_column, nc=2, adj=2, columnWidth=(1, 125), columnAttach=(1, 'both', 0))
	orient_joint_button = cmds.button(p=orient_joint_row, l='Orient Joint Options', ann='Display orient joint options',
										command=lambda *args: joint_functions.display_orient_joint_options())
	display_axis_toggle = cmds.iconTextButton(p=orient_joint_row,  ann='Toggle display axis for all joints',
										style='iconOnly', image1='channelBoxUseManips.png',
										command=lambda *args: joint_functions.display_local_axis())
	orient_channelbox_button = cmds.button(p=tab_1_column, l='Toggle Joint Attributes', ann='Toggles joint attributes',
										command=lambda *args: joint_functions.show_joint_attr())
	
	#Scale Compensation
	cmds.separator(p=tab_1_column, height=12)
	scale_comp_label = cmds.text(p=tab_1_column, l='Scale Compensation')
	scale_comp_row = cmds.rowLayout(p=tab_1_column, nc=2, adj=2, columnWidth=(1, 75), columnAttach=(1, 'both', 0))
	scale_comp_on_button = cmds.button(parent=scale_comp_row, label='On', annotation='Turn scale compensation on',
										command=lambda *args: joint_functions.scale_compensate(1))
	scale_comp_off_button = cmds.button(parent=scale_comp_row, label='Off', annotation='Turn scale compensation off',
										command=lambda *args: joint_functions.scale_compensate(0))
	
	#Covert to Joints
	cmds.separator(p=tab_1_column, height=12)
	create_joints_row = cmds.rowLayout(p=tab_1_column, nc=2, adj=2, columnWidth=(1, 110), columnAttach=(1, 'left', 0))
	create_joints_button = cmds.button(p=create_joints_row, l='Selection to Joints', ann='Places joint at selection',
										command=lambda *args: create_joints.convert_to_joints(create_joints_checkbox))
	create_joints_checkbox = cmds.checkBox(p=create_joints_row, l='Del', ann='Delete selection?', align='right')

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
	fk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='FK', annotation='Creates an FK rig. Select first joint of chain then run', parent= auto_rigs_row, command=lambda *args: auto_rigs.simple_fk())
	broken_fk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='Broken', annotation='Creates an broken FK rig. Select first joint of chain then run', parent= auto_rigs_row, command=lambda *args: auto_rigs.broken_fk())
	ik_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinHandle.png', label='IK', annotation='Creates an IK rig. Select first joint of chain then run', parent= auto_rigs_row, command=lambda *args: auto_rigs.simple_ik())
	rk_button = cmds.iconTextButton(style='iconAndTextVertical', image1='kinJoint.png', label='RK', annotation='Creates an RK rig. Select first joint of chain then run', parent= auto_rigs_row, command=lambda *args: auto_rigs.simple_rk())

	# tab 2
	tab_2_column = cmds.columnLayout(adjustableColumn=True, columnAlign='center', parent=my_tabs)

	cmds.separator(height=24, parent=tab_1_column)
	other_label = cmds.text(label='BETA Functions Below!', parent=tab_1_column)
	cmds.separator(height=24, parent=tab_1_column)

	# Random Placement
	random_placement_button = cmds.button(parent=tab_1_column, label='Random Placement', annotation='Random placement options', command=lambda *args: random_placement.random_placement_prompt())

	# Custom Outliner
	custom_outliner_button = cmds.button(parent=tab_1_column, label='Custom Outliner', annotation='Open custom outliner', command=lambda *args: custom_outliner.custom_outliner())

	# Custom Animation window
	custom_outliner_button = cmds.button(parent=tab_1_column, label='Animator', annotation='Open animation master', command=lambda *args: custom_animation_window.custom_animation())

	# Add tabs
	cmds.tabLayout(my_tabs, edit=True, tabLabel=[(tab_1_column, 'Main'), (tab_2_column, '...')])

	# Show window
	# cmds.showWindow(my_window)

	# Check if dockable window exists
	if cmds.dockControl('CSA Toolbox', query=True, exists=True):
		cmds.deleteUI('CSA Toolbox', control=True)
	elif cmds.dockControl('MayaWindow|CSA_Toolbox', query=True, exists=True):
		cmds.deleteUI('MayaWindow|CSA_Toolbox')

	# Show as dockable window
	allowedAreas = ['right', 'left']
	my_dock_control = cmds.dockControl('CSA Toolbox', area='left', aa=allowedAreas, content=my_window)
	print(my_dock_control)
