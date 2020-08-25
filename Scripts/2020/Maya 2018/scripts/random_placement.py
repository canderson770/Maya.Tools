#random_placement
#2017-11-06
#============================================
import maya.cmds as cmds
import random as rand


def random_place(x_minF, x_maxF, y_minF, y_maxF, z_minF, z_maxF, amountF, checkboxesF, rand_window, close):
    '''Copy and randomly place selected objects'''
    
    sels = cmds.ls(sl=True)
    saved_sel = []
    
    x_min = cmds.floatField(x_minF, q=True, v=True)
    x_max = cmds.floatField(x_maxF, q=True, v=True)
    y_min = cmds.floatField(y_minF, q=True, v=True)
    y_max = cmds.floatField(y_maxF, q=True, v=True)
    z_min = cmds.floatField(z_minF, q=True, v=True)
    z_max = cmds.floatField(z_maxF, q=True, v=True)
    
    amount = cmds.intSliderGrp(amountF, q=True, v=True)
    
    tran = cmds.checkBoxGrp(checkboxesF, q=True, v1=True)
    rot = cmds.checkBoxGrp(checkboxesF, q=True, v2=True)
    scal = cmds.checkBoxGrp(checkboxesF, q=True, v3=True)
	
    for sel in sels:
        for i in range(amount-1):
            copy = cmds.duplicate(sel, rr=True)
			
            if tran == True:
                x = rand.uniform(x_min,x_max)
                y = rand.uniform(y_min,y_max)
                z = rand.uniform(z_min,z_max)
                cmds.move(x, y, z, copy, ws=True, a=True, rpr=True)
                
            if rot == True:
                x = rand.uniform(0,360)
                y = rand.uniform(0,360)
                z = rand.uniform(0,360)
                cmds.rotate(x, y, z, copy)
                
            if scal == True:
                x = rand.uniform(.5,2)
                y = rand.uniform(.5,2)
                z = rand.uniform(.5,2)
                cmds.scale(x, y, z, copy)
                
            saved_sel.append(copy)
	
	cmds.select(clear=True)
    for sel in saved_sel:
        cmds.select(sel, add=True)
        
    if close == True:
        if cmds.window(rand_window, q=True, exists=True):
            cmds.deleteUI(rand_window)
        

def random_placement_prompt():
    random_place_window = 'RandomPlacementWindow'
    
    if cmds.window(random_place_window, q=True, exists=True):
        cmds.deleteUI(random_place_window)
        
    random_place_window = cmds.window(random_place_window, title='Random Placement', minimizeButton=False, maximizeButton=False)
    
    random_place_column = cmds.columnLayout(parent=random_place_window, adjustableColumn=True, columnAlign='center')
    
    #Min Fields
    cmds.separator(height=12, parent=random_place_column)
    random_place_min_row = cmds.rowLayout(parent=random_place_column, numberOfColumns=7, columnWidth=(1, 30))
    cmds.text(label="Min | ")
    
    cmds.text(label="X:")
    x_min_field = cmds.floatField(precision=2, v=-10)
    
    cmds.text(label="Y:")
    y_min_field = cmds.floatField(precision=2, v=-10)
    
    cmds.text(label="Z:")
    z_min_field = cmds.floatField(precision=2, v=-10)
    
    #Max Fields
    cmds.separator(height=12, parent=random_place_column)
    random_place_max_row = cmds.rowLayout(parent=random_place_column, numberOfColumns=7, columnWidth=(1, 30))
    cmds.text(label="Max | ")
    
    cmds.text(label="X:")
    x_max_field = cmds.floatField(precision=2, v=10)
    
    cmds.text(label="Y:")
    y_max_field = cmds.floatField(precision=2, v=10)
    
    cmds.text(label="Z:")
    z_max_field = cmds.floatField(precision=2, v=10)
    
    #Amount Slider
    cmds.separator(height=12, parent=random_place_column)
    amount_slider_grp = cmds.intSliderGrp(parent=random_place_column, columnAlign3=("left", "left", "left"), cw3=(50, 50, 50), adjustableColumn=3, label="Amount:", field=True,
            minValue=0, maxValue=100, fieldMinValue=0, fieldMaxValue=100, value=10)
    
    #Checkboxes        
    cmds.separator(height=12, parent=random_place_column)
    rand_place_checkBoxes = cmds.checkBoxGrp(parent=random_place_column, numberOfCheckBoxes=3, columnWidth3=(80, 80, 80), va3=(True, True, True), 
            labelArray3=("Translate", "Rotate", "Scale"))
            
    #Apply Buttons        
    cmds.separator(height=12, parent=random_place_column)
    rand_place_apply_row = cmds.rowLayout(parent=random_place_column, numberOfColumns=2, columnAttach2=("both", "both"), columnWidth2=(126, 126))
    rand_place_random_btn = cmds.button(parent=rand_place_apply_row, label="Randomize", command=lambda *args:
        random_place(x_min_field, x_max_field, y_min_field, y_max_field, z_min_field, z_max_field, amount_slider_grp, rand_place_checkBoxes, random_place_window, True))
    rand_place_apply_btn = cmds.button(parent=rand_place_apply_row, label="Apply", command=lambda *args:
        random_place(x_min_field, x_max_field, y_min_field, y_max_field, z_min_field, z_max_field, amount_slider_grp, rand_place_checkBoxes, random_place_window, False))
    
    cmds.showWindow(random_place_window)
    cmds.window(random_place_window, edit=True, widthHeight=(252, 175), sizeable=False)