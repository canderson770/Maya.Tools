import maya.cmds as cmds


def create_fk():
    '''Creates a FK system along a single chain of joints'''

    last_ctrl = ''
    cmds.select(hi=True)
    sels = cmds.ls(sl=True)
    
    for sel in sels:
        cmds.select(clear=True)
        pos = cmds.xform(sel, q=True, rotatePivot=True, ws=True)
        rot = cmds.xform(sel, q=True, ro=True, ws=True)
        ctrl = cmds.circle( nr=rot, c=pos)

        if last_ctrl != '':
            cmds.parent(ctrl, last_ctrl)

        last_ctrl = ctrl
        
        
'''// MILESTONE
1
proc
CreateFKJoints(float $radius)
{
    string $sels[] = `ls - sl`;
string $mainJnt = $sels[0];
string $descendents[] = `listRelatives - ad`;
string $buffer[];
string $oldCtrl = "null";

if (size($sels) == 0)
error("Select something");

if (size($sels) < 2)
{
for ($i=0; $i < size($descendents); $i++)
{
string $children[] = `listRelatives -c`;
$sels[$i+1] = $children[0];
select -r $children[0];
}
}

for ($i=0; $i < size($sels); $i++)
{
string $temp = $sels[$i];
tokenize $temp "_" $buffer;

string $circle[] = `circle -c 0 0 0 -nr 1 0 0 -sw 360 -r $radius -d 3 -ut 0 -tol 0 -s 8 -ch 1`;
DeleteHistory;
string $newGrp = `group`;

float $pos[] = `xform -q -ws -rp $sels[$i]`;
float $rot[] = `xform -q -ws -ro $sels[$i]`;

move -rpr $pos[0] $pos[1] $pos[2] $newGrp;
rotate -a -ws $rot[0] $rot[1] $rot[2] $newGrp;

string $frontName;

for ($j=0; $j < (size($buffer)-1); $j++)
{
string $temp2 = $buffer[$j] + "_";
$frontName += $temp2;
}

if ($oldCtrl != "null")
{
select -r $newGrp;
select -add $oldCtrl;
parent;
}
else
{
if (`objExists "Controls"`)
{
select -r $newGrp;
select -add "Controls";
parent;
}
else
{
select -r $newGrp;
group -name "Controls";
}

if (`objExists "ControlsLayer"`)
{
editDisplayLayerMembers -noRecurse ControlsLayer $newGrp;
}
else
{
select -r $newGrp;
createDisplayLayer -name "ControlsLayer" -number 1 -nr;
}
}
select -r $circle[0];
select -add $sels[$i];

parentConstraint -mo -weight 1;
scaleConstraint -offset 1 1 1 -weight 1;

setAttr -lock true ($circle[0] + ".v");
rename $newGrp ($frontName + "Grp");
$oldCtrl = `rename $circle[0] ($frontName + "Ctrl")`;
}

if (`objExists "Skeleton"`)
{
select -r $mainJnt;
select -add "Skeleton";
parent;
}
else
{
select -r $mainJnt;
group -name "Skeleton";
createDisplayLayer -name "SkeletonLayer" -number 1 -nr;
}

if (`objExists "SkeletonLayer"`)
{
editDisplayLayerMembers -noRecurse SkeletonLayer $mainJnt;
}
else
{
select -r $mainJnt;
createDisplayLayer -name "SkeletonLayer" -number 1 -nr;
}
}

global proc
CreateFKPrompt()
{
    string $sels[] = `ls - sl`;
if (size($sels) > 0)
{
    string $text;
string $result = `promptDialog
                  - title
"Ctrl Radius"
- message
"Enter the size:"
- button
"OK" - button
"Cancel"
- defaultButton
"OK" - cancelButton
"Cancel"
- dismissString
"Cancel"
`;

if ($result == "OK")
{
$text = `promptDialog - query - text`;
CreateFKJoints((float)$text);
}
}
}
'''