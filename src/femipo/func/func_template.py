from vectormath import Vector3
from shapely.geometry import Point
import numpy as np


from ..fem.cards.gcoord import GCOORD

from .load_surf import LoadSurf
from typing import Callable, Tuple, Union
from typing import Protocol
class FUNC_TEMPLATE(Protocol):
    
    def translate_nodes(self,trans_vector:Vector3)->None:
        ...
    def get_nodes_given_exnodes(self,nodes_exe:list[int])->list[int]:
        ...
    def get_node_given_coordinates(self,point:Point)->int:
        ...
    def get_nodes_inBox(self,p1:Point,p2:Point)->list[int]:
        ...
    def get_node_coordinates(self,node:int)->tuple[float,float,float]:
        ...
    def get_max_min_coor(self)->dict[str,float]:
        ...
    def get_nodes_between_z_coor(self,z1:float,z2:float)->list[int]:
        ...
    def get_nodes_in_elements(self,elements:list[int])->list[int]:
        ...
    def get_nodes_in_plane(self,plane:np.ndarray,tolerance=1e-4)->list[int]:
        ...
    def select_nodes_to_be_removed(self,remove_el)->list[int]:
        ...
    def select_nodes_not_to_be_removed(self,elements_not_to_be_removed:list[int])->list[int]:
        ...
    def get_nodes_in_lc(self,lc:int)->list[int]:
        ...
  
    def get_exe_nodes_inBox_vector(self,p1:Point,vec:Vector3)->list[int]:
        ...
    #def add_bnbc(self,nodes:list[int],fix:list[int])->None:
    #    ...
    def get_elements_inBox(self,p1:Point,p2:Point)->list[int]:
        ...
    def get_elements_containg_nodes(self,nodes:list[int])->list[int]:
        ...
    def get_element_sides(self,nodes:list[int],element)->list[int]:
        ...
    def get_elment_gcoord(self,element:int)->list[GCOORD]:
        ...
    def get_nodes_in_element_side(self,elnum:int,side:int)->list[int]:
        ...

    def find_nex_unused_set_num(self)->int:
        ...

    def create_set(self,num,fem_List,type,tx1=None,tx2=None)->None:
        ...
    Lrt1 = float   #Beusolo return type 1
    Lrt2 = tuple[float, float, float]  #Beusolo return type

    LoadFuncType = Callable[..., Union[float, Tuple[float, float, float]]]  

    

    #def add_beuslo_plane(self,pp1:Point,pp2:Point,pp3:Point,lc:int,beusol_obj:BEUSLO,load_func:LoadFuncType|None=None,lf:float=1.0,constant_load:float|None=None)->None:
    #    ...

       
    def create_beuslo(self,lc:int,loadtype:int,load_surf:list[LoadSurf],load_func:LoadFuncType,lf:float=1.0,**load_func_args:float)->None:
        ...
    def create_beuslo_given_nodes(self,lc:int,nodes:list[int],loadtype:int,load_func:LoadFuncType,lf:float=1.0,**load_func_args:float)->None:
        ...
    def merge_beusol_into_lc(self,lc:int,lcs:list[int])->None:  
        ...
    def move_beusol_to_lc(self,lc_old:int,lc_new:int)->None:
        ...
   

    def get_surf_element_side(self,pp1:Point,pp2:Point,pp3:Point)->list[LoadSurf]:
        ...
    
    def duplicate_nodes(self,gcoord:GCOORD)->bool:
        ...
    def get_org_node_num_if_duplicate(self,gcoord:GCOORD)->int:
        ...
    def add_bnbc(self,nodes:list[int],fix:list[int])->None:
        ...
    def create_grav(self,lc:int)->None:
        ...
