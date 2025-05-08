from dataclasses import dataclass
import copy
from multiprocessing.reduction import duplicate
from typing import Callable, OrderedDict

from shapely import Point
from vectormath import Vector3
from femipo import fem
from femipo.fem.cards import gelmnt1,gcoord,gelref1
from femipo.fem.cards.gnode import GNODE
from ..func.func_geo import mirror_point,rotate_point_origin_euler

from .fem import FEM

@dataclass
class ASSEMBLY():
    base_fem: FEM

    def rotate(self,seq:str,angles:list[float],make_copy:bool=False)->None:
        """
        Rotates the base FEM object around the origin (0,0,0) using a sequence of Euler angles.

        Args:
            seq (str): Sequence of rotations using 'x', 'y', 'z' characters.
                      The rotations are applied in the order specified.
                      Examples: 'xyz', 'zyx', 'x', 'zy'
            angles (list[float]): List of rotation angles in degrees.
                               Must match the length of seq.
                               Positive angles follow the right-hand rule.
            make_copy (bool): If True, creates a new rotated copy instead of
                             modifying the original. Defaults to False.
        
        Examples:
            # Rotate 90 degrees around z-axis
            >>> assembly.rotate('z', [90])
            
            # Rotate 45 degrees around x, then 30 around y
            >>> assembly.rotate('xy', [45,30])
            
            # Make a rotated copy 180 degrees around z
            >>> assembly.rotate('z', [180], make_copy=True)
        """
        other:FEM=copy.deepcopy(self.base_fem) 
        for node in other.gcoord:
            p=rotate_point_origin_euler(Point(other.gcoord[node].xcoord, other.gcoord[node].ycoord, other.gcoord[node].zcoord), seq, angles,degrees=True)
            other.gcoord[node].xcoord, other.gcoord[node].ycoord, other.gcoord[node].zcoord = p.x, p.y, p.z 
        if not make_copy:
            self.base_fem = other   
            
        else:
            self.add(other)  
            

        
    def mirror(self,po:Point,vector:Vector3,make_copy:bool=False)->None:
        """
        Mirror the base FEM object across a plane defined by a point and a vector.
        Args:
            po (Point): A point on the plane of reflection.
            vector (Vector3): A vector normal to the plane of reflection.
            make_copy (bool): If True, create a copy of the base FEM object. Default is False.
        """
        other:FEM=copy.deepcopy(self.base_fem) 
        for node in other.gcoord:
            p=mirror_point(Point(other.gcoord[node].xcoord, other.gcoord[node].ycoord, other.gcoord[node].zcoord), po, vector)
            other.gcoord[node].xcoord, other.gcoord[node].ycoord, other.gcoord[node].zcoord = p.x, p.y, p.z
        if not make_copy:
            self.base_fem = other
        else:
            self.add(other)


    def translate(self,dx:float,dy:float,dz:float,make_copy:bool=False)->None:
        """
        Translate the base FEM object by the given distances in x, y, and z directions.
        Args:
            dx (float): Distance to translate in x direction.
            dy (float): Distance to translate in y direction.
            dz (float): Distance to translate in z direction.
        """
        other:FEM=copy.deepcopy(self.base_fem) 

        for node in other.gcoord:
            other.gcoord[node].xcoord += dx
            other.gcoord[node].ycoord += dy
            other.gcoord[node].zcoord += dz
        if not make_copy:
            self.base_fem = other
        else:
            self.add(other)
    
    

    def add(self,fem_obj:FEM)->None:
        """
        Add a 3D FEM object to the assembly.
        Args:
            fem_obj (FEM): The 3D FEM object to be added.
        """
        # join gcoord ,remove duplicatet nodes base on tolerance of 1e-4,update node numbers
        dupicate_nodes:dict[int,int]=self._get_duplicate_nodes(fem_obj)
        next_node_num:int=max(self.base_fem.gcoord)+1
        next_element_num:int=max(self.base_fem.gelmnt1)+1
        node_num_conv_dict:dict[int,int]={}
        for node in self.base_fem.gcoord:
            node_num_conv_dict[node] = node
        for node,coord in fem_obj.gcoord.items():
            if node in dupicate_nodes:
                continue
            self.base_fem.gcoord[next_node_num]=coord
            node_num_conv_dict[node] = next_node_num

            next_node_num += 1

        #update gnodes
        #get the first item in self.base_fem.gnode
        first_gnode = next(iter(self.base_fem.gnode.values())) 
        ndof=first_gnode.ndof
        odof=first_gnode.odof

        self.base_fem.gnode=OrderedDict()
        for node in self.base_fem.gcoord:
            self.base_fem.gnode[node] = GNODE(node,ndof,odof)


        
        for elnum,gelmnt in fem_obj.gelmnt1.items():
            nodin=[node_num_conv_dict[node] for node in gelmnt.nodin]
            self.base_fem.gelmnt1[next_element_num]=gelmnt1.GELMNT1(next_element_num,gelmnt.eltype,gelmnt.eltyad,nodin)
            self.base_fem.gelref1[next_element_num] = fem_obj.gelref1[elnum]
            next_element_num += 1

        
    def _get_duplicate_nodes(self,other:FEM)->dict[int,int]:
      """get the duplicate nodes between two FEM objects"""
      duplicate_nodes={}
      for key,value in other.gcoord.items():
         if self.base_fem.duplicate_nodes(value):
            duplicate_nodes[key]=other.get_org_node_num_if_duplicate(value)
      return duplicate_nodes
