from dataclasses import dataclass

from shapely import Point

from femipo import fem

from .fem import FEM
from .element_parameters import SOLID_20,SHELL_8,shell_solid_mpap_8_20
from .cards.gnode import GNODE
from .cards.gcoord import GCOORD
from .cards.gelmnt1 import GELMNT1
from .cards.gelref1 import GELREF1

from .cards.ident import IDENT
from ..func.func_geo import  calc_new_point

@dataclass
class Alfa():
    start:float
    stopp:float
 

@dataclass
class Revolve():
    base_fem_2d:FEM
    fem_3d:FEM
    revolve_point:Point



    def create_solid_from_shell(self,base_elements:list[int],alfas:list[Alfa],selnum:int)->None:
        
        self._creat_IDENT(selnum)
        #create Date
        self._create_DATE()
        
        
        node_num:int=len(self.fem_3d.gcoord)+1
      
        element_num:int=len(self.fem_3d.gelmnt1)+1
     
        for alfa in alfas:
            
            
         
           
            for element in base_elements:
                solid_nodes:dict[int,GCOORD]={}
                # get the element type
                typ=self.base_fem_2d.gelmnt1[element].eltype
                if typ==SHELL_8:
                    gcoords_base=self.base_fem_2d.get_elment_gcoord(element)

                    solid_nodes=self._create_solid_nodes(gcoords_base,alfa.start,alfa.stopp)
                    for s,v in solid_nodes.items():
                        print(f'{s=} {v.xcoord} {v.ycoord} {v.zcoord}')
                    nodin:list[int]=[]
                    for node in solid_nodes:
                                              
                        if self.fem_3d.get_org_node_num_if_duplicate(solid_nodes[node])<0:
                            self.fem_3d.gcoord[node_num]=solid_nodes[node]
                            nodin.append(node_num)
                            node_num+=1
                        else:
                            print(self.fem_3d.get_org_node_num_if_duplicate(solid_nodes[node]))
                            nodin.append(self.fem_3d.get_org_node_num_if_duplicate(solid_nodes[node]))
                           
                    self.fem_3d.gelmnt1[element_num]=GELMNT1(element_num,SOLID_20,0,nodin)
                    element_num+=1
          
                  
        self._create_GNODE()
        # create GELREF1
        matno=self.base_fem_2d.gelref1[base_elements[0]].matno
        self._create_GELREF1(matno)
    
        # create the material card
        self._create_MISOSEL(matno)
        # define the shell tickness
   
        

    def _create_sets(self,nodes:list[GCOORD],start_alfa:float,stopp_alfa:float)->dict[int,GCOORD]:
        return_nodes:dict[int,GCOORD]={}
        half_alfa=start_alfa+(stopp_alfa-start_alfa)/2
        if len(nodes)==8:
            pass
                   
                

    def _create_solid_nodes(self,nodes:list[GCOORD],start_alfa:float,stopp_alfa:float)->dict[int,GCOORD]:
        return_nodes:dict[int,GCOORD]={}
        half_alfa=start_alfa+(stopp_alfa-start_alfa)/2

      

        if len(nodes)==8:
            for n,node in enumerate(nodes):
                en=shell_solid_mpap_8_20[n+1]

                p0=calc_new_point(self.revolve_point,Point(node.xcoord,node.ycoord,node.zcoord),start_alfa)
                return_nodes[en[0]]=GCOORD(p0.x,p0.y,p0.z)
                if len(en)==3:       
                    p1=calc_new_point(self.revolve_point,Point(node.xcoord,node.ycoord,node.zcoord),half_alfa)
                    return_nodes[en[1]]=GCOORD(p1.x,p1.y,p1.z)
                    p2=calc_new_point(self.revolve_point,Point(node.xcoord,node.ycoord,node.zcoord),stopp_alfa)
                    return_nodes[en[2]]=GCOORD(p2.x,p2.y,p2.z)
                elif len(en)==2:
                    p1=calc_new_point(self.revolve_point,Point(node.xcoord,node.ycoord,node.zcoord),stopp_alfa)
                    return_nodes[en[1]]=GCOORD(p1.x,p1.y,p1.z)

        #return sorted by the key from low to high
        return_nodes=dict(sorted(return_nodes.items(),key=lambda x:x[0]))

        return  return_nodes
    
    
    def _create_GNODE(self)->None:
       
        for n in self.fem_3d.gcoord:
            self.fem_3d.gnode[n]=GNODE(n,6,123456)
    
    def _create_GELREF1(self,matno:int)->None:
        for element,v in self.fem_3d.gelmnt1.items():          
            self.fem_3d.gelref1[element]=GELREF1(matno=matno,addno=1,intno=0,mintno=0,strano=0,streno=0,strepono=0,geono=1,fixno=0,eccno=0,transno=0) 
    
    def _create_DATE(self)->None:   
        self.fem_3d.date= self.base_fem_2d.date 


    def _creat_IDENT(self,num)->None:
       
        self.fem_3d.ident[1]=IDENT(self.base_fem_2d.ident[1].slevel,self.base_fem_2d.ident[1].selmod)
        
   

    
    def _create_MISOSEL(self,matno):        
        self.fem_3d.misosel[matno]=self.base_fem_2d.misosel[matno] 
    
