from ast import Break
import bge
from bge import logic
from math import radians

def start(cont):
    obj = cont.owner
    group = obj.groupObject
    GD = bge.logic.globalDict
    icon = group.groupMembers.get('icon')
    always = cont.sensors[0]
    #meshs = cont.actuators['mesh']

    #icon.visible = False
    #iconRot = group.groupMembers.get()

    if always.positive:
        
        icon.applyRotation([0,0,radians(group.get('rotation'))], True)
        print(icon)
        
     



    if  GD['gunColected']:
        quant = len(GD['gunColected'])
        
        
        if obj['empt'] == 'livre' and obj['act'] == False and group['level'] < len(GD['gunColected']):
            obj['wepon'] =  GD['gunColected'][group['level']]
            obj['act'] = True
            icon.visible = True
            icon.replaceMesh(obj['wepon']) 
            
            
            
               

        if quant >= group['level']:
            obj['empt'] = 'livre'
            #icon.visible = False

        