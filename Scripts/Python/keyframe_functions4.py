#keyframe_functions
#2017-12-10
#=========================================
import maya.cmds as cmds
import maya.mel as mel

def custom_animation():        
    custom_animation_window =  'custom_animation'

    if cmds.window(custom_animation_window, exists=True):
        cmds.deleteUI(custom_animation_window, window=True)

    custom_animation_window = cmds.window(custom_animation_window, title='Animation Master', minimizeButton=False, maximizeButton=False)
    
    main_layout = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
        
    custom_animation_column = cmds.columnLayout(parent=main_layout)
    
    custom_animation_row_buttons = cmds.rowLayout(parent=custom_animation_column, numberOfColumns=6)
        
    add_clip_button = cmds.symbolButton(parent=custom_animation_row_buttons, image='addClip.png', h=20, w=30, 
        annotation='Add new animation clip', command=lambda *args: create_clip_row(custom_animation_column))
        
    cmds.symbolButton(parent=custom_animation_row_buttons, image='autoload.png', h=20, w=30, 
        annotation='Open the Graph Editor', command=lambda *args: mel.eval('GraphEditor'))
        
    cmds.button(parent=custom_animation_row_buttons, label='Dope Sheet', 
        annotation='Open the Dope Sheet', command=lambda *args: create_clip_row(custom_animation_column))
        
    cmds.symbolButton(parent=custom_animation_row_buttons, image='game_exporter.png', h=20, w=30, 
        annotation='Open Game Exporter', command=lambda *args: mel.eval('gameFbxExporter'))
         
    cmds.symbolButton(parent=custom_animation_row_buttons, image='gear.png', h=20, w=30, 
        annotation='Open Color Prefrences', command=lambda *args: mel.eval('ColorPreferencesWindow'))           
            
    cmds.window(custom_animation_window, edit=True, widthHeight=(277, 570))
    cmds.showWindow(custom_animation_window)
    

def change_color_settings():
    mel.eval('ColorPreferencesWindow;')

def change_key_color(onOff):
    current_time = cmds.currentTime(q=True)
    cmds.selectKey(clear=True)
    cmds.selectKey(add=True, keyframe=True, time=(current_time,current_time))
    cmds.keyframe(tds=onOff)
    if onOff:
        mel.eval('timeSliderEditKeys makeKey;')

def change_to_breakdown(onOff):
    if onOff:
        mel.eval('timeSliderEditKeys makeBreakdown;')
        cmds.keyframe(tds=False)
    else:
        mel.eval('timeSliderEditKeys makeKey;')
        cmds.keyframe(tds=False)
        
def change_range(clip_frame_list, start, end):
    if not start == '':
        cmds.playbackOptions(min=start, ast=start)

        if not end == '':  
            cmds.playbackOptions(max=end, aet=end)
            add_frames(clip_frame_list, start, end)
    
    
def play_clip(play_button, start, end):
    if not start == '':
        if not end == '':   
            cmds.playbackOptions(min=start, ast=start)
            cmds.playbackOptions(max=end, aet=end)
        
            if cmds.play(q=True, state=True):
                cmds.play(state=False)
                cmds.symbolButton(play_button, e=True, image='playClip.png')
            else:
                cmds.play()
                cmds.symbolButton(play_button, e=True, image='stopClip.png')


def create_clip_row(custom_animation_column):
    clip_layout = cmds.columnLayout(parent=custom_animation_column, bgc=(.2, .2, .2))
    cmds.rowLayout(parent=clip_layout, numberOfColumns=4, columnAlign4=('center','center','center','center'))
    cmds.text(label='', width = 20)
    cmds.text(label='Clip Name', width=110)
    cmds.text(label='Start', width = 40)
    cmds.text(label='End', width = 40)
    
    cmds.rowLayout(parent=clip_layout, numberOfColumns=5)
    play_button = cmds.symbolButton(image='playClip.png', h=20, w=20, c=lambda *args: play_clip(play_button, cmds.textField(start_field, q=True, tx=True), cmds.textField(end_field, q=True, tx=True)))
    cmds.textField(width=110)
    start_field = cmds.textField(width=40, cc=lambda *args: change_range(clip_frame_list, cmds.textField(start_field, q=True, tx=True), cmds.textField(end_field, q=True, tx=True)))
    end_field = cmds.textField(width=40, cc=lambda *args: change_range(clip_frame_list, cmds.textField(start_field, q=True, tx=True), cmds.textField(end_field, q=True, tx=True)))
    delete_button = cmds.symbolButton(image='deleteActive.png', h=20, w=20, c=lambda *args: delete_row(delete_button, False) )
    
    cmds.separator(parent=clip_layout)
    cmds.text(parent=clip_layout, label='Keyframes', width=250)
    
    clip_frame_list = cmds.textScrollList(parent=clip_layout, selectCommand=lambda *args: frame_select(clip_frame_list, 
        cmds.textField(start_field, q=True, tx=True), cmds.textField(end_field, q=True, tx=True)))
        
    right_click_menu = cmds.popupMenu(parent=clip_layout)
    cmds.menuItem(parent=right_click_menu, sh=True, label='Set Key', command=lambda *args: mel.eval('SetKey'))
    cmds.menuItem(parent=right_click_menu, label='Set Key on Animated', command=lambda *args: mel.eval('SetKeyAnimated'))
    cmds.menuItem(parent=right_click_menu, label='Set Breakdown', command=lambda *args: mel.eval('ColorPreferencesWindow'))  
    
    right_click_ctrl_menu = cmds.popupMenu(parent=clip_layout, sh=True)
    cmds.menuItem(parent=right_click_ctrl_menu, label='Normal Key', command=lambda *args: change_to_breakdown(False))
    cmds.menuItem(parent=right_click_ctrl_menu, label='Special Key', command=lambda *args: change_key_color(True))
    cmds.menuItem(parent=right_click_ctrl_menu, label='Breakdown Key', command=lambda *args: change_to_breakdown(True)) 
    
    right_click_shift_menu = cmds.popupMenu(parent=clip_layout, ctl=True)
    cmds.menuItem(parent=right_click_shift_menu, label='Key Translate', command=lambda *args: mel.eval('SetKeyTranslate'))
    cmds.menuItem(parent=right_click_shift_menu, label='Key Rotate', command=lambda *args: mel.eval('SetKeyRotate'))
    cmds.menuItem(parent=right_click_shift_menu, label='Key Scale', command=lambda *args: mel.eval('SetKeyScale'))     
    
def delete_row(delete_button, frame):
    if frame:
        cmds.deleteUI(cmds.symbolButton(delete_button, q=True, parent=True))
    else:
        row = cmds.symbolButton(delete_button, q=True, parent=True)
        cmds.deleteUI( cmds.rowLayout(row, q=True, parent=True))
    
    
def create_frame_row(clip_frame_list):
    current_time = int(cmds.currentTime(q=True))
    cmds.textScrollList(clip_frame_list, e=True, append=current_time)
    current_list = cmds.textScrollList(clip_frame_list, q=True, allItems=True)
        
    current_set = sorted(list(set(current_list)))
        
    cmds.textScrollList(clip_frame_list, e=True, removeAll=True)
    cmds.textScrollList(clip_frame_list, e=True, append=current_set)



def frame_select(clip_frame_list, start, end):
    select_item = cmds.textScrollList(clip_frame_list, q=True, selectItem=True)
    time = float(select_item[0])
    cmds.currentTime(time)
    
    if not start == '':
        if not end == '':   
            cmds.playbackOptions(min=start, ast=start)
            cmds.playbackOptions(max=end, aet=end)
    
def frame_remove(clip_frame_list):
    cmds.textScrollList(clip_frame_list, e=True, removeItem=cmds.textScrollList(clip_frame_list, q=True, selectItem=True))
    
    
def add_frames(clip_frame_list, start, end):
    frame_range = int(end) - int(start) + 1
    start_frame = int(start)
    
    cmds.textScrollList(clip_frame_list, e=True, removeAll=True)
    for i in range(frame_range):
        cmds.textScrollList(clip_frame_list, e=True, append=start_frame)
        start_frame = start_frame + 1
        
    num_items = cmds.textScrollList(clip_frame_list, q=True, numberOfItems=True)
    new_height = 12 * int(num_items) + (int(num_items)) + 5
    cmds.textScrollList(clip_frame_list, e=True, height=new_height)
    
    

custom_animation()

#keys = cmds.selectKey(add=True, keyframe=True, time=(0,24))
#print(keys)
        