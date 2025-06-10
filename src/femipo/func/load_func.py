

import numpy as np

from femipo.fem.cards.bgrav import BGRAV
from ..fem.cards.beuslo import BEUSLO
from .load_surf import LoadSurf
from typing import Callable, Dict,Any

from typing import List,Union,Tuple
from ..fem.fem_base import FEM_BASE
from ..fem.element_parameters import  side_dic_20



from .func_template import FUNC_TEMPLATE


import math
import inspect
import logging
logger = logging.getLogger(__name__)


LoadFuncType = Callable[..., Union[float, Tuple[float, float, float]]] 
    
def contains_element(load_surfs: List['LoadSurf'], element: int) -> bool:
    """Check if the element is in any of the LoadSurf objects in the list."""
    return any(ls.element == element for ls in load_surfs)

   
def contains_element_and_side(load_surfs: List['LoadSurf'], element: int, side: int) -> bool:
    """Check if both the element and side are in any of the LoadSurf objects in the list."""
    return any(ls.element == element and ls.side == side for ls in load_surfs)
  





def extract_func_parameters(func: LoadFuncType) -> Dict[str, Any]:
    """
    Extracts the parameters of a given function, including their default values if present.
    
    - Required parameters (without a default) are set to `None`.
    - Parameters with default values are stored with their respective defaults.
    - `**kwargs` (variable keyword arguments) are labeled as `"Keyword Arguments"`.
    
    Args:
        func (Callable): The function to analyze.

    Returns:
        Dict[str, Any]: A dictionary mapping parameter names to their default values or `None` if no default exists.
    """
    if func is None:
        raise ValueError("The provided function is None.")
    signature = inspect.signature(func)
    params = signature.parameters
    args_dict: Dict[str, Any] = {}

    for name, param in params.items():
        if param.default != inspect.Parameter.empty:
            args_dict[name] = param.default  # Store default value
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            args_dict[name] = "Keyword Arguments"  # Label for **kwargs
        else:
            args_dict[name] = None  # Required parameter without a default

    return args_dict


class LOAD_FUNC(FEM_BASE,FUNC_TEMPLATE):

   
    Lrt1 = float   #Beusolo return type 1
    Lrt2 = tuple[float, float, float]  #Beusolo return type

   
    #LoadFuncType = Callable[[float, float, float],  Union[Lrt1,Lrt2]], 

 
    def create_beuslo(self,lc:int,loadtype:int,                        
                       load_surf:list[LoadSurf],
                       load_func:LoadFuncType,
                      lf:float=1.0,
                      **load_func_args:float)->None:
        if lc in self.beuslo:
            raise ValueError("The load case already exist")
        
        self.beuslo.setdefault(lc,{})

        for surf in load_surf:
            self.beuslo[lc].setdefault(surf.element, {})
            self.beuslo[lc][surf.element][surf.side] = self._create_beusol_obj(
            elno=surf.element,
            side=surf.side,
            load_type=loadtype,
            load_func=load_func,
            lf=lf,  # Ensure load factor is passed
            **load_func_args  # Correctly unpack additional arguments
        )
           
    def create_beuslo_given_nodes(self,lc:int,nodes:list[int],loadtype:int,load_func:LoadFuncType,lf:float=1.0,**load_func_args:float)->None:
    
        load_surf=self._create_load_surf_ojbects(nodes)
        self.create_beuslo(lc=lc,loadtype=loadtype,load_surf=load_surf,load_func=load_func,lf=lf,**load_func_args)
       
    def create_beuslo_given_elements(self,lc:int,elements:list[int],loadtype:int,load_func:LoadFuncType,lf:float=1.0,shell_z:int=0,**load_func_args:float)->None:
        load_surf:list[LoadSurf]=[]

        for element in elements:
            if element not in self.gelmnt1:
                raise ValueError(f"Element {element} not found in the model.")
            if self.gelmnt1[element].eltype == 28:
                load_surf.append(LoadSurf(element=element, side=shell_z))
        self.create_beuslo(lc=lc,loadtype=loadtype,load_surf=load_surf,load_func=load_func,lf=lf,**load_func_args)
        

    def delete_beuslo(self,lc:int)->None:
        if lc in self.beuslo.keys():
            del self.beuslo[lc]

    def create_beusol_based_on_lc(self,lc:int,base_lc:int,
                                load_surf_filter:list[LoadSurf]|None=None,                       
                                load_func:LoadFuncType|None=None,
                                load_type:int=2,
                                lf:float=1.0,
                                **load_func_args:float)->None:
        
        if base_lc not in self.beuslo:
            raise ValueError("The load case don't exist")
        if lc in self.beuslo:
            raise ValueError("The load case already exist")
        else:
            self.beuslo.setdefault(lc,{})

        for element,beusols in self.beuslo[base_lc].items():
            if self.gelmnt1[element].eltype not in [20,30]:
                continue
            
            if load_surf_filter  and contains_element(load_surf_filter,element):
                    continue
            
            
            self.beuslo[lc].setdefault(element, {})
            for side,beusol in beusols.items():
                if load_surf_filter  and contains_element_and_side(load_surf_filter,element,side):
                        continue
                if load_func is None:
                    beusol=self.beuslo[base_lc][element][side]
                    self.beuslo[lc][element][side]=BEUSLO(load_type,beusol.complx,beusol.layer,beusol.ndof,beusol.intno,side,beusol.rload)
                    continue
                obj=self._create_beusol_obj(elno=element,load_type=load_type,side=side,load_func=load_func,lf=lf,**load_func_args)
                if np.abs(sum(obj.rload)) < 1e-6:
                    
                    continue
                self.beuslo[lc][element][side]=obj
       
    def merge_beusol_into_lc(self,lc:int,lcs:list[int],                      
                                load_func:LoadFuncType|None=None,
                                load_type:int=2,
                                lf:float=1.0,
                                **load_func_args:float)->None:
        # ONGOING
        for _lc in lcs:
            for element,beusols in self.beuslo[_lc].items():
                    for side,beusol in beusols.items():
                        if (element or side) not in self.beuslo[lc]:
                            self.beuslo[lc][element][side]=self._create_beusol_obj(elno=element,side=side,load_type=load_type,
                                                                                   load_func=load_func,lf=lf,load_func_args=load_func_args)





    def _create_beusol_obj(self,elno:int,side:int,load_type:int,load_func:LoadFuncType,lf:float=1.0,**load_func_args:float)->BEUSLO:
        #TODO   add implementiation for complex 
        rload:list[float]=[]
        eltype=self.gelmnt1[elno].eltype
        # get all the nodes for the given side of the given element
       
        nodes=self.get_nodes_in_element_side(elno,side)
        
      
        args = extract_func_parameters(load_func)

        #calculate ndof
       
        if eltype not in [20,30,28]:
            raise ValueError("The current feature only works for 20-nodes solid element and 15-nodes solid element")
        
        #LOTYP = 1 number of nodes of the specified element side.
        #LOTYP = 2 number of translational degrees of freedom of the specified element side.
        loadtype_mult=1 if load_type==1 else 3    
        
        if eltype in [20, 28]:
            ndof = 8 * loadtype_mult
        elif eltype == 30:
            if side in [1,10]:
                ndof = 6 * loadtype_mult
            else:
                ndof = 8 * loadtype_mult

        else:
            raise ValueError("Unsupported element type")
       

        for node in nodes:
            x,y,z=self.get_node_coordinates(node)

            local_arg=locals()
            for arg in args:
                if arg in local_arg:
                    args[arg]=local_arg[arg]
                if arg in load_func_args:
                    args[arg]=load_func_args[arg]

            match load_type:
                case 1:
                    result=load_func(**args)
                    if not isinstance(result,(float,int)):
                        raise ValueError(" The return type of the load_func must be a float for loadtype 1")
                    rload.append(result*lf)
                case 2:
                    result=load_func(**args)
                    if not isinstance(result,tuple):
                        raise ValueError("The retrun type of the load_func must be a tuple (x-dir,y-dir,z-dir) for loadtype 2")
        
        return BEUSLO(loadtyp=load_type,complx=0,layer=0,ndof=ndof,intno=0,side=side,rload=rload)       
           
        
    def _create_load_surf_ojbects(self,nodes:list[int],shell_z:int=0)->list[LoadSurf]:
        """Create LoadSurf objects for the given element and side."""
        retun_load_surf_objects:list[LoadSurf]=[]
        for el in self.gelmnt1:
            nodes_in_element=self.gelmnt1[el].nodin
            if self.gelmnt1[el].eltype ==28:
                z_side={-1:1,0:2,1:3}
                if nodes_in_element in nodes:
                    retun_load_surf_objects.append(LoadSurf(element=el, side=z_side[shell_z]))
            elif self.gelmnt1[el].eltype ==20:
                node_idx:list[int]=[]
                for idx,node in enumerate(nodes_in_element):
                    if node in nodes:
                        node_idx.append(node)  
                    else:
                        continue
                node_idx=list(sorted(node_idx))
                for side,idxs in side_dic_20.items():
                    node_comp=list(sorted([self.gelmnt1[el].nodin[id-1] for id in idxs]))
                    if node_comp == node_idx:
                        retun_load_surf_objects.append(LoadSurf(element=el, side=side))
    
        return retun_load_surf_objects
    
    
           


   
    def create_grav(self,lc:int)->None:
        self.bgrav[lc]=BGRAV(modelnode=0,opt=0,gx=0,gy=0,gz=-9.8066501)
  
