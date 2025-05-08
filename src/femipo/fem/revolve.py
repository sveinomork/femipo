from dataclasses import dataclass


from shapely import Point
from vectormath import Vector3



from .fem import FEM
from .element_parameters import BEAM_3, SOLID_20,SHELL_8,shell_solid_mpap_8_20,shell_solid_map_6_15,beam_shell_map_3_8
from .cards.gnode import GNODE
from .cards.gcoord import GCOORD
from .cards.gelmnt1 import GELMNT1
from .cards.gelref1 import GELREF1

from .cards.ident import IDENT
from ..func.func_geo import  calc_new_point


@dataclass
class Alfa():
    start:float
    stop:float
 

@dataclass
class Revolve():
    base_fem_2d:FEM
    fem_3d:FEM
    revolve_point:Point

    def extrude(self,base_elements:list[int],vector:Vector3,nof:int,selnum:int,set_num:int=1,set_name="default_set",create_set:bool=True)->None:
        
        pass

    def create_solid_from_shell(self,base_elements:list[int],alfas:list[Alfa],selnum:int,set_num:int=1,set_name="default_set",create_set:bool=True)->None:
        
        self._creat_IDENT(selnum)
        #create Date
        self._create_DATE()
        
        nodes,elements=self._create_fem_3d(alfas=alfas,base_elements=base_elements)

        if create_set:
            self.fem_3d.create_set(set_num,fem_List=elements,type=2,tx1=f'{set_name}_elments',tx2=None)
            self.fem_3d.create_set(set_num,fem_List=nodes,type=1,tx1=f'{set_name}_nodes',tx2=None)
 
          
                  
        self._create_GNODE()
        # create GELREF1
        matno=self.base_fem_2d.gelref1[base_elements[0]].matno
        self._create_GELREF1(matno,elements)
    
        # create the material card
        self._create_MISOSEL(matno)
        # define the shell tickness
   
        
    def _create_fem_3d(self,alfas:list[Alfa],base_elements:list[int])->tuple[list[int],list[int]]:
        node_num:int=len(self.fem_3d.gcoord)+1
      
        element_num:int=len(self.fem_3d.gelmnt1)+1
        return_nodes:list[int]=[]
        return_elements:list[int]=[]
        for alfa in alfas:
                     
            for element in base_elements:
                solid_nodes:dict[int,GCOORD]={}
                # get the element type
                typ=self.base_fem_2d.gelmnt1[element].eltype
                if typ==SHELL_8:
                    gcoords_base=self.base_fem_2d.get_elment_gcoord(element)

                    solid_nodes=self._create_solid_nodes(gcoords_base,alfa,mapping_dict=shell_solid_mpap_8_20)
                    

                    nodin:list[int]=[]
                    for node in solid_nodes:
                                              
                        if self.fem_3d.get_org_node_num_if_duplicate(solid_nodes[node])<0:
                            return_nodes.append(node_num)
                            self.fem_3d.gcoord[node_num]=solid_nodes[node]
                            nodin.append(node_num)
                            node_num+=1
                        else:
                            
                            nodin.append(self.fem_3d.get_org_node_num_if_duplicate(solid_nodes[node]))
                           
                    self.fem_3d.gelmnt1[element_num]=GELMNT1(element_num,SOLID_20,0,nodin)
                    return_elements.append(element_num)
                    element_num+=1
        
        return list(set(return_nodes)),return_elements
    
    def _create_node_set(self,alfas:list[Alfa],base_elements:list[int],num:int,description="")->None:
        nodes=self._find_sets_nodes(alfas=alfas,base_elements=base_elements)
        self.fem_3d.create_set(num,fem_List=nodes,type=1,tx1=description,tx2=None)

    
    def _find_sets_nodes(self,alfas:list[Alfa],base_elements:list[int])->list[int]:
        set_nodes:list[int]=[]
        for alfa in alfas:
            for element in base_elements:
                typ=self.base_fem_2d.gelmnt1[element].eltype
                if typ==BEAM_3:

                    gcoords_base=self.base_fem_2d.get_elment_gcoord(element)
                    nodes=self._create_solid_nodes(gcoords_base,alfa,mapping_dict=beam_shell_map_3_8)
                    for s,v in nodes.items():
                        node=self.fem_3d.get_node_given_coordinates(Point(v.xcoord,v.ycoord,v.zcoord))
                        if node>0:
                            set_nodes.append(node)
                        else:
                            raise ValueError(f"Node not found node for coordinates: {v.xcoord}, {v.ycoord}, {v.zcoord}")
        return sorted(list(set(set_nodes)))
                        
    
    def _create_boundary_condition(self,alfas:list[Alfa],base_elements:list[int],fixed_dofs:list[int])->None:
        nodes=self._find_sets_nodes(alfas=alfas,base_elements=base_elements)
        self.fem_3d.add_bnbc(nodes,fixed_dofs)
                
    def _create_loads(self,alfas:list[Alfa],base_elements:list[int],lc,load_func,lf=1.0)->None:  
        nodes=self._find_sets_nodes(alfas=alfas,base_elements=base_elements) 
        self.fem_3d.create_beuslo_given_nodes(lc=lc,nodes=nodes,loadtype=1,load_func=load_func,lf=lf)
        
    def _extrude_to_solid_nodes(self,nodes:list[GCOORD],vector:Vector3,elength:list[float],
                            mapping_dict:dict[int, list[int]])->dict[int, GCOORD]:
        
        pass

    def _create_solid_nodes(self, base_nodes: list[GCOORD], alfa:Alfa, 
                        mapping_dict: dict) -> dict[int, GCOORD]:
        """
        Create 3D nodes for a solid by revolving input nodes around a point.
        
        Args:
            base_nodes: List of input nodes to revolve
            start_alfa: Starting angle for revolution (in radians)
            stop_alfa: Stopping angle for revolution (in radians)
            mapping_dict: Dictionary mapping source node indices to target node indices
                        
        Returns:
            Dictionary of new nodes indexed by their element node number
        """
        return_nodes: dict[int, GCOORD] = {}
        half_alfa = alfa.start + (alfa.stop - alfa.start) / 2
        
        # Process each node according to mapping
        for n, node in enumerate(base_nodes):
            node_index = n + 1  # 1-based indexing
            if node_index not in mapping_dict:
                continue
                
            target_indices = mapping_dict[node_index]
            point = Point(node.xcoord, node.ycoord, node.zcoord)
            
            # Create first point at start angle
            p0 = calc_new_point(self.revolve_point, point, alfa.start)
            return_nodes[target_indices[0]] = GCOORD(p0.x, p0.y, p0.z)
            
            if len(target_indices) == 3:
                # Create middle point at half angle
                p1 = calc_new_point(self.revolve_point, point, half_alfa)
                return_nodes[target_indices[1]] = GCOORD(p1.x, p1.y, p1.z)
                
                # Create end point at stop angle
                p2 = calc_new_point(self.revolve_point, point, alfa.stop)
                return_nodes[target_indices[2]] = GCOORD(p2.x, p2.y, p2.z)
                
            elif len(target_indices) == 2:
                # Create end point at stop angle
                p1 = calc_new_point(self.revolve_point, point, alfa.stop)
                return_nodes[target_indices[1]] = GCOORD(p1.x, p1.y, p1.z)
        
        # Return sorted by the key from low to high
        return_nodes = dict(sorted(return_nodes.items(), key=lambda x: x[0]))
        
        return return_nodes

    
    def _create_GNODE(self)->None:
       
        for n in self.fem_3d.gcoord:
            self.fem_3d.gnode[n]=GNODE(n,6,123456)
    
    def _create_GELREF1(self,matno:int,elments:list[int])->None:
        for element in elments:
            if element not in self.fem_3d.gelref1:          
                self.fem_3d.gelref1[element]=GELREF1(matno=matno,addno=1,intno=0,mintno=0,strano=0,streno=0,strepono=0,geono=1,fixno=0,eccno=0,transno=0) 
            else:
                raise ValueError(f"Element {element} already exists in GELREF1")

    def _create_DATE(self)->None:   
        self.fem_3d.date= self.base_fem_2d.date 


    def _creat_IDENT(self,num)->None:
       
        self.fem_3d.ident[1]=IDENT(self.base_fem_2d.ident[1].slevel,self.base_fem_2d.ident[1].selmod)
        
   

    
    def _create_MISOSEL(self,matno):        
        self.fem_3d.misosel[matno]=self.base_fem_2d.misosel[matno] 
    
