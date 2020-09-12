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
import color_override


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
	reload(color_override)

	w_width = 160
	w_width = 160
	sep_height = 12

	my_window = 'CSAToolboxWindow'
	my_dock_control='CSAToolbox'
	two_button_row = (1, 'both', 0)

	# Create window
	if cmds.window(my_window, q=True, exists=True): cmds.deleteUI(my_window)
	my_window = cmds.window(my_window, width=w_width)

    # Create main column
	main_column = cmds.columnLayout('ColumnLayout', p=my_window, adjustableColumn=True, columnAlign='center')

	# Create header
	image_row = cmds.rowLayout(p=main_column, nc=2, adj=2, columnAlign=(2,'center'), bgc=(1,1,1))
	my_image = cmds.picture(p=image_row, image='logo-32.png')
	my_name = cmds.text(p=image_row, label='Cody Anderson')

	# Create tab layout
	my_tabs = cmds.tabLayout('TabLayout', p=main_column)

	# Tab 1
	t1_column = cmds.columnLayout('TabColumn1',p=my_tabs, adj=1, columnAlign='center')

	# MODELING TOOLS
	cmds.separator(p=t1_column, height=sep_height)
	other_label = cmds.text(p=t1_column, l='Modeling')
	cmds.separator(p=t1_column, height=sep_height)

	# Poly Count
	poly_count_button = cmds.button(p=t1_column, l='Poly Count', ann='Toggle poly count',
				command=lambda *args: simple_functions.toggle_poly_count())

	cmds.separator(p=t1_column, height=sep_height)

	# Simple modeling tools
	delete_history_button = cmds.button(p=t1_column, l='Delete History', ann='Delete history',
				command=lambda *args: simple_functions.delete_history())
	freeze_transform_button = cmds.button(p=t1_column, l='Freeze Transformations', ann='Freeze all transformations',
				command=lambda *args: simple_functions.freeze_transformations())
	center_pivot_button = cmds.button(p=t1_column, l='Center Pivot', ann='Center pivot',
				command=lambda *args: simple_functions.center_pivot())

	cmds.separator(p=t1_column, height=sep_height)

	# Rename Functions
	rename_button = cmds.button(p=t1_column, l='Rename', ann='Sequential renamer',
				command=lambda *args: rename_functions.rename_prompt())
	search_and_replace_button = cmds.button(p=t1_column, l='Search And Replace', ann='Search and replace',
				command=lambda *args: rename_functions.search_and_replace())

	# RIGGING TOOLS
	cmds.separator(p=t1_column, height=sep_height)
	other_label = cmds.text(p=t1_column, l='Rigging')
	cmds.separator(p=t1_column, height=sep_height)

	# Locator
	locator_row = cmds.rowLayout(p=t1_column, nc=3, adj=3, columnWidth=(1, 60))
	create_locator_button = cmds.button(p=locator_row, l='Locators', ann='Create locator(s)',
				command=lambda *args: create_locator.center_locator(locator_buttons))
	locator_buttons = cmds.radioCollection(p=locator_row)
	locator_button_1 = cmds.radioButton(l='Each', ann='Create locator at each selection')
	locator_button_2 = cmds.radioButton(l='All', ann='Create locator at center of entire selection')
	cmds.radioCollection(locator_buttons, edit=True, select=locator_button_1)

	# Covert to Joints
	create_joints_row = cmds.rowLayout(p=t1_column, nc=2, adj=2, columnWidth=(1, 110), columnAttach=(1, 'left', 0))
	create_joints_button = cmds.button(p=create_joints_row, l='Selection to Joints', ann='Places joint at selection',
				command=lambda *args: create_joints.convert_to_joints(create_joints_checkbox))
	create_joints_checkbox = cmds.checkBox(p=create_joints_row, l='Del', ann='Delete selection?', align='right')

	# Place Controls
	place_controls_button = cmds.button(p=t1_column, l='Place Controls', ann='Place controls at selection',
				command=lambda *args: create_controls.place_controls())

	cmds.separator(p=t1_column, height=sep_height)

	# Change color
	color_slider = cmds.colorIndexSliderGrp(p=t1_column, w=w_width/2, cw=(1, 60), adj=2, min=1, max=32, v=1)
	color_buttons_row = cmds.rowLayout(p=t1_column, nc=2, adj=2, columnWidth=(1, 75), columnAttach=two_button_row)
	color_set_button = cmds.button(p=color_buttons_row, l='Set Color', ann='Changes color to slider color',
				command=lambda *args: color_override.change_color_slider(color_slider))
	color_default_button = cmds.button(p=color_buttons_row, l='Default Color', ann='Changes color back to default',
				command=lambda *args: color_override.default_color())

	cmds.separator(p=t1_column, height=sep_height)

	# Contstraints
	parent_constrain_button = cmds.button(p=t1_column, l='Parent Constrain', ann='Parent constrain',
				command=lambda *args: cmds.parentConstraint())
	scale_constrain_button = cmds.button(p=t1_column, l='Scale Constrain', ann='Scale constrain',
				command=lambda *args: cmds.scaleConstraint())
	point_constrain_button = cmds.button(p=t1_column, l='Point Constrain', ann='Point constrain',
				command=lambda *args: cmds.pointConstraint())
	orient_constrain_button = cmds.button(p=t1_column, l='Orient Constrain', ann='Orient constrain',
				command=lambda *args: cmds.orientConstraint())
	pole_vector_constrain_button = cmds.button(p=t1_column, l='Pole Vector Constrain', ann='Pole vector constrain',
				command=lambda *args: cmds.poleVectorConstraint())

	cmds.separator(p=t1_column, height=sep_height)

	#Orient Joint
  	orient_joint_row = cmds.rowLayout(p=t1_column, nc=2, adj=2, columnWidth=(1, 125), columnAttach=two_button_row)
	orient_joint_button = cmds.button(p=orient_joint_row, l='Orient Joint Options', ann='Display orient joint options',
				command=lambda *args: joint_functions.display_orient_joint_options())
	display_axis_toggle = cmds.iconTextButton(p=orient_joint_row,  ann='Toggle display axis for all joints',
				style='iconOnly', image1='channelBoxUseManips.png',
				command=lambda *args: joint_functions.display_local_axis())
	orient_channelbox_button = cmds.button(p=t1_column, l='Toggle Joint Attributes', ann='Toggles joint attributes',
				command=lambda *args: joint_functions.show_joint_attr())

	cmds.separator(p=t1_column, height=sep_height)

	#Scale Compensation
	scale_comp_label = cmds.text(p=t1_column, l='Scale Compensation')
	scale_comp_row = cmds.rowLayout(p=t1_column, nc=2, adj=2, columnWidth=(1, 75), columnAttach=two_button_row)
	scale_comp_on_button = cmds.button(parent=scale_comp_row, label='On', annotation='Turn scale compensation on',
				command=lambda *args: joint_functions.scale_compensate(1))
	scale_comp_off_button = cmds.button(parent=scale_comp_row, label='Off', annotation='Turn scale compensation off',
				command=lambda *args: joint_functions.scale_compensate(0))

	cmds.separator(p=t1_column, height=sep_height)

	#Auto rigs
	auto_rigs_row = cmds.rowLayout(p=t1_column, nc=4, columnAlign=(2, 'left'))
	fk_button = cmds.iconTextButton(p=auto_rigs_row, l='FK', ann='Creates a FK rig. Select first joint',
				style='iconAndTextVertical', image1='kinJoint.png',
				command=lambda *args: auto_rigs.simple_fk())
	broken_fk_button = cmds.iconTextButton(p=auto_rigs_row, l='Broken', ann='Creates a broken FK rig. Select first joint',
				style='iconAndTextVertical', image1='kinJoint.png',
				command=lambda *args: auto_rigs.broken_fk())
	ik_button = cmds.iconTextButton(p=auto_rigs_row, l='IK', ann='Creates an IK rig. Select first joint',
				style='iconAndTextVertical', image1='kinHandle.png',
				command=lambda *args: auto_rigs.simple_ik())
	rk_button = cmds.iconTextButton(p=auto_rigs_row, l='RK', ann='Creates a RK rig. Select first joint',
				style='iconAndTextVertical', image1='kinJoint.png',
				command=lambda *args: auto_rigs.simple_rk())

	cmds.separator(p=t1_column, height=sep_height)

	# Skinning
	bind_skin_button = cmds.button(p=t1_column, l='Bind Skin', ann='Binds skin to joint(s)',
				command=lambda *args: cmds.bindSkin())
	paint_weights_button = cmds.button(p=t1_column, l='Paint Weights', ann='Opens paint weight options',
				command=lambda *args: mel.eval('ArtPaintSkinWeightsToolOptions'))

	# tab 2
	t2_column = cmds.columnLayout(p=my_tabs, adj=True, columnAlign='center')

	cmds.separator(p=t1_column, height=sep_height)
	other_label = cmds.text(p=t1_column, l='BETA Functions Below!')
	cmds.separator(p=t1_column, height=sep_height)

	# Random Placement
	random_placement_button = cmds.button(p=t1_column, l='Random Placement', ann='Random placement options',
				command=lambda *args: random_placement.random_placement_prompt())

	# Custom Outliner
	custom_outliner_button = cmds.button(p=t1_column, l='Custom Outliner', ann='Open custom outliner',
				command=lambda *args: custom_outliner.custom_outliner())

	# Custom Animation window
	custom_outliner_button = cmds.button(p=t1_column, l='Animator', ann='Open animation master',
				command=lambda *args: custom_animation_window.custom_animation())

	# Add tabs
	cmds.tabLayout(my_tabs, edit=True, tabLabel=[(t1_column, 'Main'), (t2_column, '...')])

	# Show window
	# cmds.showWindow(my_window)

	# Check if dockable window exists
	if cmds.dockControl(my_dock_control, q=True, e=True): cmds.deleteUI(my_dock_control, control=True)

	# Create dockable window
	my_dock_control = cmds.dockControl(my_dock_control, area='left', width=w_width, fixedWidth=True,
				aa=['right', 'left'], content=my_window)
