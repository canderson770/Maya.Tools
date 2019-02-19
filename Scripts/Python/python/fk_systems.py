#fk_systems
#2017-11-06
#============================================
import maya.cmds as cmds


def simple_fk():
    '''Creates a FK system along a single chain of joints'''
    #Variables
    last_ctrl = ''
    replace = "Jnt"
    
    #Get selection with hierarchy
    cmds.select(hi=True)
    sels = cmds.ls(sl=True)
    
    #Loop through selection
    for sel in sels:
        #Set up control names
        if replace in sel:
            ctrl_name = sel.replace(replace, "FK_Ctrl")
            grp_name = sel.replace(replace, "FK_Grp")
        else:
            ctrl_name = '%s_FK_Ctrl' % sel
            grp_name = '%s_FK_Grp' % sel
        
        #Create control and control group    
        ctrl = cmds.circle(c=(0,0,0), nr=(1,0,0), sw=360, r=1, d=3, ut=0, tol=0, s=8, ch=1, n=ctrl_name)  
        grp = cmds.group(ctrl, n=grp_name)
        
        #Match control group to joint transform
        pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
        rot = cmds.xform(sel, q=True, ro=True, ws=True)
        cmds.move(pos[0],pos[1],pos[2], grp, ws=True, a=True, rpr=True)
        cmds.rotate(rot[0],rot[1],rot[2], grp, a=True, ws=True)
        
        #Constrain joint to control         
        cmds.parentConstraint(ctrl, sel)
        cmds.scaleConstraint(ctrl, sel)
        
        #If it's not the first control parent to last control    
        if last_ctrl != '':
            cmds.parent(grp, last_ctrl, a=True)
            
        #If it's  the first control
        else:
            #Create 'Controls' group if it doesn't exist
            if cmds.objExists('Controls'):
                cmds.parent(grp, 'Controls')
            else:
                controls_grp = cmds.group(grp, n='Controls')
                if cmds.listRelatives(controls_grp, p=True):
                    cmds.parent(controls_grp, world=True)
                
            #Create 'Skeleton' group if it doesn't exist    
            if cmds.objExists('Skeleton'):
                if cmds.listRelatives(sel, p=True):
                    cmds.parent(sel, world=True)
                cmds.parent(sel, 'Skeleton')
            else:
                skeleton_grp = cmds.group(sel, n='Skeleton')
                if cmds.listRelatives(skeleton_grp, p=True):
                    cmds.parent(skeleton_grp, world=True)

        #Save last ctrl
        last_ctrl = ctrl
        
        #Freeze Transformations and delete history
        cmds.makeIdentity(ctrl, apply=True)
        cmds.delete(ctrl, ch=True)
        
        #Lock and hide  visibility
        cmds.setAttr('%s.v' % ctrl[0], lock=True, keyable=False, channelBox=False)
    
    #Clear selection     
    cmds.select(clear=True)
    
    
def broken_fk():
    '''Creates a broken fk system along a single chain of joints'''
    
    #Variables
    master_control_grp = ''
    last_ctrl = ''
    first_pass = 'true'
    replace = "Jnt"
    
    #Get selection with hierarchy
    cmds.select(hi=True)
    sels = cmds.ls(sl=True)
    
    #Loop through selection
    for sel in sels:
        #Set up control names
        if replace in sel:
            ctrl_name = sel.replace(replace, "FK_Ctrl")
            grp_name = sel.replace(replace, "FK_Grp")
        else:
            ctrl_name = '%s_FK_Ctrl' % sel
            grp_name = '%s_FK_Grp' % sel
        
        #Create control and control group   
        ctrl = cmds.circle(c=(0,0,0), nr=(1,0,0), sw=360, r=1, d=3, ut=0, tol=0, s=8, ch=0, n=ctrl_name)  
        grp = cmds.group(ctrl, n=grp_name)
        
        #Match control group to joint transform
        pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
        rot = cmds.xform(sel, q=True, ro=True, ws=True)
        cmds.move(pos[0],pos[1],pos[2], grp, ws=True, a=True, rpr=True)
        cmds.rotate(rot[0],rot[1],rot[2], grp, a=True, ws=True)
        
        #Constrain joint to control        
        cmds.parentConstraint(ctrl, sel)
        cmds.scaleConstraint(ctrl, sel)
        
        #Add Follow Transform and Follow Rotate       
        cmds.addAttr(ctrl[0], ln='FollowTransform', at='double', min=0, max=1, dv=True, keyable=True)
        cmds.addAttr(ctrl[0], ln='FollowRotate', at='double', min=0, max=1, dv=True, keyable=True)
        
        #If its the first control
        if first_pass == 'true':
            first_pass = 'false'
            
            #Create master control, move, rotate, and freeze transformations
            master_ctrl = cmds.spaceLocator(n='%s_Master_Ctrl' % sel)
            cmds.move(pos[0],pos[1],pos[2], master_ctrl, ws=True, a=True, rpr=True)
            cmds.rotate(rot[0],rot[1],rot[2], master_ctrl, a=True, ws=True)
            cmds.makeIdentity(master_ctrl, apply=True)

            #Create master ctrl group and constain it to master ctrl
            master_ctrl_grp = cmds.group(empty=True, n='%s_Master_Grp' % sel)
            cmds.scaleConstraint(master_ctrl, master_ctrl_grp)
            cmds.parent(grp, master_ctrl_grp)
            
            #Constrain first control to master control
            transform_constraint = cmds.parentConstraint(master_ctrl, grp, mo=True, skipTranslate=('x','y','z'), n='%s_parentTransformConstaint' % grp)
            rotate_constraint = cmds.parentConstraint(master_ctrl, grp, mo=True, skipRotate=('x','y','z'), n='%s_parentRotateConstaint' % grp)
            
            #Create main control croup
            main_ctrl_grp = cmds.group(master_ctrl, n='%s_Ctrl_Grp' % sel)
            cmds.parent(master_ctrl_grp, main_ctrl_grp)
            
            #Connect Follow Transform and Follow Rotate
            cmds.connectAttr('%s.FollowTransform' % ctrl[0], transform_constraint[0] + '.%sW0' % master_ctrl[0], f=True)
            cmds.connectAttr('%s.FollowRotate' % ctrl[0], rotate_constraint[0] + '.%sW0' % master_ctrl[0], f=True)
            
            
            #Create 'Controls' group if it doesn't exist
            if cmds.objExists('Controls'):
                cmds.parent(main_ctrl_grp, 'Controls')
            else:
                controls_grp = cmds.group(main_ctrl_grp, n='Controls')
                if cmds.listRelatives(controls_grp, p=True):
                    cmds.parent(controls_grp, world=True)
                
            #Create 'Skeleton' group if it doesn't exist
            if cmds.objExists('Skeleton'):
                if cmds.listRelatives(sel, p=True):
                    cmds.parent(sel, world=True)
                cmds.parent(sel, 'Skeleton')
            else:
                skeleton_grp = cmds.group(sel, n='Skeleton')
                if cmds.listRelatives(skeleton_grp, p=True):
                    cmds.parent(skeleton_grp, world=True)
                
        #If it's not the first control
        else:
            #Move to master control group
            cmds.parent(grp, master_ctrl_grp)
            
            #Contrain to previous control
            transform_constraint = cmds.parentConstraint(last_ctrl, grp, mo=True, skipRotate=('x','y','z'), n='%s_parentTransformConstaint' % grp)
            rotate_constraint = cmds.parentConstraint(last_ctrl, grp, mo=True, skipTranslate=('x','y','z'), n='%s_parentRotateConstaint' % grp)
            
            #Connect Follow Transform and Follow Rotate
            cmds.connectAttr('%s.FollowTransform' % ctrl[0], transform_constraint[0] + '.%sW0' % last_ctrl[0], f=True)
            cmds.connectAttr('%s.FollowRotate' % ctrl[0], rotate_constraint[0] + '.%sW0' % last_ctrl[0], f=True)
        
        #Save last ctrl     
        last_ctrl = ctrl
        
        #Freeze Transformations and delete history
        cmds.makeIdentity(ctrl, apply=True)
        #cmds.delete(ctrl, ch=True)
        
        #Lock and/or hide scale and visibility
        cmds.setAttr('%s.v' % ctrl[0], lock=True, keyable=False, channelBox=False)
        cmds.setAttr('%s.sx' % ctrl[0], lock=True, keyable=False)
        cmds.setAttr('%s.sy' % ctrl[0], lock=True, keyable=False)
        cmds.setAttr('%s.sz' % ctrl[0], lock=True, keyable=False)
        
    #Clear selection    
    cmds.select(clear=True)