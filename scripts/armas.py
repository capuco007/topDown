import bge

from bge import logic

def start(cont):
    own = cont.owner
    own['mesh'] = [obj for obj in own.childrenRecursive if 'arma' in obj]

def update(cont):
    own = cont.owner
    scn =own.scene
    mesh = own['mesh'][0]
    group = own.groupObject

    if 'gun' in group:
      
  
        mesh.replaceMesh(group['gun'])
