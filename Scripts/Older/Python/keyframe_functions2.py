#keyframe_functions
#2017-12-10
#=========================================
import maya.cmds as cmds
import maya.mel as mel

def custom_animation():        
    custom_animation_window =  'custom_animation'

    if cmds.window(custom_animation_window, exists=True):
        cmds.deleteUI(custom_animation_window, window=True)

    custom_animation_window = cmds.window(custom_animation_window, title='Keyframes', minimizeButton=False, maximizeButton=False)
    
    main_layout = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
        
    custom_animation_column = cmds.columnLayout(parent=main_layout)
    
    custom_animation_row_buttons = cmds.rowLayout(parent=custom_animation_column, numberOfColumns=6)
        
    add_clip_button = cmds.button(parent=custom_animation_row_buttons, label='New Clip', 
        annotation='Add new animation clip', command=lambda *args: create_clip_row(custom_animation_column))
                    
    
    cmds.window(custom_animation_window, edit=True, widthHeight=(292, 570))
    cmds.showWindow(custom_animation_window)
    

def change_color_settings():
    mel.eval('ColorPreferencesWindow;')

def change_key_color(onOff):
    current_time = cmds.currentTime(q=True)
    cmds.selectKey(clear=True)
    cmds.selectKey(add=True, keyframe=True, time=(current_time,current_time))
    cmds.keyframe(tds=onOff)

def change_to_breakdown(onOff):
    if onOff:
        mel.eval('timeSliderEditKeys makeBreakdown;')
    else:
        mel.eval('timeSliderEditKeys makeKey;')
        
def change_range_start(start):
    cmds.playbackOptions(min=start, ast=start)
    
def change_range_end(end):
    cmds.playbackOptions(max=end, aet=end)
    
def play_clip(play_button, start, end):
    if not start == '':
        if not end == '':   
            change_range_start(start) 
            change_range_end(end)
        
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
    
    cmds.rowLayout(parent=clip_layout, numberOfColumns=6)
    delete_button = cmds.symbolButton(image='deleteActive.png', h=20, w=20, c=lambda *args: delete_row(delete_button, False) )
    cmds.textField(width=110)
    start_field = cmds.textField(width=40, cc=lambda *args: change_range_start(cmds.textField(start_field, q=True, tx=True)))
    end_field = cmds.textField(width=40, cc=lambda *args: change_range_end(cmds.textField(end_field, q=True, tx=True)))
    play_button = cmds.symbolButton(image='playClip.png', h=20, w=20, c=lambda *args: play_clip(play_button, cmds.textField(start_field, q=True, tx=True), cmds.textField(end_field, q=True, tx=True)))
    add_frame_button = cmds.symbolButton(image='addClip.png', h=20, w=30, c=lambda *args: create_frame_row(clip_frame_list))
    
    cmds.separator(parent=clip_layout)
    cmds.rowLayout(parent=clip_layout, numberOfColumns=3, columnAlign3=('center','center','center'))
    cmds.text(label='S', width=13)
    cmds.text(label='B', width=13)
    cmds.text(label='Keyframe', width = 220)
    
    clip_frame_list = cmds.textScrollList(parent=clip_layout, height=400, selectCommand=lambda *args: frame_select(clip_frame_list), 
        deleteKeyCommand=lambda *args: outliner_remove(clip_frame_list))
    
    
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



def frame_select(clip_frame_list):
    select_item = cmds.textScrollList(clip_frame_list, q=True, selectItem=True)
    time = float(select_item[0])
    cmds.currentTime(time)
    
def outliner_remove(clip_frame_list):
    cmds.textScrollList(clip_frame_list, e=True, removeItem=cmds.textScrollList(clip_frame_list, q=True, selectItem=True))
    

custom_animation()

#keys = cmds.selectKey(add=True, keyframe=True, time=(0,24))
#print(keys)
        