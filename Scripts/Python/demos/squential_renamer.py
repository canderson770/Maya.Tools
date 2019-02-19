import maya.cmds as cmds


def sequential_renamer(name):
    '''Renames selection sequentially'''

    #get selection
    sels = cmds.ls(sl=True)

    if not sels:
        cmds.error("No Selection")

    if len(sels) < 2:
        for i in range(len(cmds.listRelatives(sels, ad=True))):
            sels[i+1] = cmds.listRelatives(sels, c=True)[0]
            cmds.select(sels[i+1])

    numTokens = name.split('#', 1)

    for i in range(len(sels)):
        name.replace('#', i, 1)

    #cmds.select(clear=True)

'''
int $numTokens = `tokenize $name "#" $buffer`;

if ($numTokens == 1)
{
for ($i=0; $i < size($sels); $i++)
{
stringArrayInsertAtIndex(size($returnNames), $returnNames, `rename $sels[$i] $buffer[0]`);
}
}
else if ($numTokens > 2)
{
error("Too many #");
}
else
{
for ($i=0; $i < size($sels); $i++)
{
string $newName;
$newName = $buffer[0] + ($i+1) + $buffer[1];
stringArrayInsertAtIndex(size($returnNames), $returnNames, `rename $sels[$i] $newName`);
}
}
select -cl;
//
return $returnNames;
}

global proc
RenamePrompt()
{
string $sels[] = `ls - sl`;
if (size($sels) > 0)
{
    string $text;
string $result = `promptDialog
                  - title
"Rename"
- message
"Example: Name_#_Jnt"
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
Rename($text);
}
}
}
'''