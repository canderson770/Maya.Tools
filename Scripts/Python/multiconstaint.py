import maya.cmds as cmds

def multiconstraint(sel_method):
    ''''''
	sels = cmds.ls(sl=True)

	if len(sels) %2:
		cmds.error("Select an even number of nodes before running")

    targets, nodes = [],[]
    
	if(sel_method):
    	targets = sels[0::2] #[start:end:step]
    	nodes = sels[1::2]
    else:
        targets = sels[:0:len(sels)/2]
        nodes = sels[len(sels)/2::]
        
	for index, sel in enumerate(targets):
		cmds.parentConstraint(targets[index], nodes[index])

	cmds.select(targets, r=True)
	
#multiconstraint(0)