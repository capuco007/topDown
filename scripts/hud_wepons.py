
from ast import Break
import bge
from bge import logic

GD = bge.logic.globalDict

#GD['equiped'] = None
#GD['slots'] = None


def start(cont):
    obj = cont.owner
    scene = obj.scene

def update(cont):
    obj = cont.owner
    scene = obj.scene
    mouse = cont.sensors['Mouse']
    point = obj.childrenRecursive.get('point')
    ms = bge.logic.mouse.inputs
    msg = cont.sensors['Message']

    
            

    if mouse.positive:
        point.worldPosition = mouse.hitPosition
        point.worldPosition.z = mouse.hitPosition[2]
        wepon = mouse.hitObject
        groupWepon = mouse.hitObject.groupObject
        if wepon['wepon'] != 'vazio':
            if ms[bge.events.LEFTMOUSE].activated  and GD['equiped'] != None:
                GD['equiped'] = wepon['wepon']
                wepon['selected'] = True
        else:
            pass
       
        
       
