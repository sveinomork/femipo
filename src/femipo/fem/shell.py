from dataclasses import dataclass
from operator import le
from shapely import Point
from vectormath import Vector3
from .fem import FEM
from .element_parameters import side_d,SOLID_20,solid20_shell,SHELL_8,SOLID_15,solid15_shell,SHELL_6,shell_solid_mpap_8_20,sh|
from .cards.gnode import GNODE
from .cards.gcoord import GCOORD
from .cards.gelmnt1 import GELMNT1
from .cards.gelref1 import GELREF1
from .cards.beuslo import BEUSLO
from .cards.gelth import GELTH
from .cards.gsetmemb import GSETMEMB
from .cards.tdsetnam import TDSETNAM
from .cards.ident import IDENT
from ..func.func_geo import  calc_new_point
from ..func.func_template import FUNC_TEMPLATE



from logging import raiseExceptions

import logging
logger = logging.getLogger(__name__)


@dataclass
class SHELL():
    fem_3d:FEM
    fem_2d:FEM

    

    def create_shell_from_solid(self,lc,boundary=None,base_setnumbers=None,setnum=1,selnum=None):
        self._creat_IDENT(selnum)
        #create Date
        self._create_DATE()
        
        # get the list of node based on hte lc
        nodes=self.fem_3d.get_nodes_in_lc(lc)  
        #create GNODES
        self._create_GNODE(nodes)
        #create GNODE conversion dict
        gnodes=self._create_gnode_conv_dict(nodes)
        #create GCOORD
        self._create_GCOORD(nodes,gnodes)
        # get the elements and create GELTMT1
        self._create_GELMNT1(gnodes,lc)
        # create elements conversion dict
        elements=self._create_element_conv_dict(lc)
        # create GELREF1
        self._create_GELREF1(elements)
        # create load BEUSLO
        self._create_BEUSLO(lc,elements) 
        # create the material card
        self._create_MISOSEL(1)
        # define the shell tickness
        self._create_GELTH(0.01)

       
        
        dup_nodes=self._find_duplicated_nodes()
        print(dup_nodes)
        self.fem_2d.write("T100.FEM")        
        print("satopp")
    
    def _create_solid_nodes(self,nodes:list[GCOORD],po:Point,alfa:float)->list[GCOORD]:
        return_nodes:list[GCOORD]=[]
        if len(nodes)==8:
            for n,node in enumerate(nodes):
                en=shell_solid_mpap_8_20[n]

                for idx in en:
                    nodes[idx]=GCOORD(node.xcoord,node.ycoord,node.zcoord)
                    if len(en)==3:
                        
                        p1=calc_new_point(po,Point(node.xcoord,node.ycoord,node.zcoord),alfa/2)
                        nodes[idx]=GCOORD(p1.x,p1.y,p1.z)
                        p2=calc_new_point(po,Point(node.xcoord,node.ycoord,node.zcoord),alfa)
                        nodes[idx]=GCOORD(p2.x,p2.y,p2.z)
                    elif len(en)==2:
                        p1=calc_new_point(po,Point(node.xcoord,node.ycoord,node.zcoord),alfa)
                        nodes[idx]=GCOORD(p1.x,p1.y,p1.z)
        
        return return_nodes
    
        






               
        


    def _create_nodes(self,element:GELMNT1,vector:Vector3)->None:
        nodes = {}
        n=1
        if element.eltype==SHELL_8:
            for sh_node,solid_node in shell_solid_mpap_8_20.items():

                
                nodes[solid_node[0]]=GCOORD(self.fem_2d.gcoord[sh_node].xcoord,
                                            self.fem_2d.gcoord[sh_node].ycoord,
                                            self.fem_2d.gcoord[sh_node].zcoord)
                if len(solid_node)==3:
                    nodes[solid_node[1]]=GCOORD(self.fem_2d.gcoord[sh_node].xcoord+0.5*vector.x,
                                            self.fem_2d.gcoord[sh_node].ycoord+0.5*vector.y,
                                            self.fem_2d.gcoord[sh_node].zcoord+0.5*vector.z)
                    
                    nodes[solid_node[1]]=GCOORD(self.fem_2d.gcoord[sh_node].xcoord+1*vector.x,
                                            self.fem_2d.gcoord[sh_node].ycoord+1*vector.y,
                                            self.fem_2d.gcoord[sh_node].zcoord+1*vector.z)
                
                
                else:
                    nodes[solid_node[1]]=GCOORD(self.fem_2d.gcoord[sh_node].xcoord+vector.x,
                                            self.fem_2d.gcoord[sh_node].ycoord+vector.y,
                                            self.fem_2d.gcoord[sh_node].zcoord+vector.z)
                    
        
    def _create_GNODE(self,nodes:list[int])->None:
       
        for n,_ in enumerate(nodes):
            self.fem_2d.gnode[n+1]=GNODE(n+1,6,123456)

    def _create_gnode_conv_dict(self,nodes:dict[int,int])->dict[int,int]:
        conv_dict={}
        for n,node in enumerate(nodes):
            conv_dict[node]=n+1
        return conv_dict
    
    def _create_GCOORD(self,nodes:dict[int,int],gnodes:dict[int,int])->None:     
        temp_dic={} 
        for node in nodes:
            temp_dic[gnodes[node]]=GCOORD(self.fem_3d.gcoord[node].xcoord,self.fem_3d.gcoord[node].ycoord,self.fem_3d.gcoord[node].zcoord) 
        
        for k in sorted(temp_dic):
            self.fem_2d.gcoord[k]=temp_dic[k]


    def _create_element_conv_dict(self,lc:int)->dict[int,int]:
        # store element information in new_el_dic. The kye is the new element number and the value is old solid element number
        new_el_dic={}
        # element number counter
        new_elnum=1
        # create the elements based on the surface load given in BEUSLO
        if lc in self.fem_3d.beuslo:            
            for elment,besulo_cards in self.fem_3d.beuslo[lc].items():
                # there can be muliple e                
                for _ in besulo_cards: 
                    # get the element type                        
                    typ=self.fem_3d.gelmnt1[elment].eltype
                    
                    #20 nodes soldi element
                    if typ==SOLID_20:                                                                                 
                        new_el_dic[new_elnum]=elment
                        new_elnum+=1 
                    if typ==SOLID_15:                                                           
                        new_el_dic[new_elnum]=elment
                        new_elnum+=1  
                    

        return new_el_dic    

        

    def _create_GELMNT1(self,gnodes:dict[int,int],lc:int)->None:
        # store element information in new_el_dic. The kye is the new element number and the value is old solid element number
        #new_el_dic={}
        # element number counter
        new_elnum=1        
        # create the elements based on the surface load given in BEUSLO
        if lc in self.fem_3d.beuslo:            
            for elment,besulo_cards in self.fem_3d.beuslo[lc].items():
                # there can be muliple e                
                for side in besulo_cards:
                    nodin=[0 for i in range(8)]
                   
                    #self.elnum_conv[new_elnum]=elment                    
                    if new_elnum not in self.fem_2d.gelmnt1:
                        self.fem_2d.gelmnt1[new_elnum]={}
                            
                    # get the element type                        
                    
                    typ=self.fem_3d.gelmnt1[elment].eltype
                    
                    # get the nodes 
                    nodes=[(n,self.fem_3d.gelmnt1[elment].nodin[n-1]) for n in side_d[typ][side]]
                    
                    #20 nodes soldi element
                    if typ==SOLID_20:                                                          
                        for n,number in nodes:
                            nodin[int(solid20_shell[side][n]-1)]=number                         
                        nodin=[gnodes[n] for n in nodin]
                        self.fem_2d.gelmnt1[new_elnum]=GELMNT1(new_elnum,eltype=SHELL_8,eltyad=0,nodin=nodin)
                        #new_el_dic[new_elnum]=elment
                        new_elnum+=1 
                    
                    if typ==SOLID_15:                                                           
                        for n,number in nodes:                            
                            nodin[int(solid15_shell[side][n]-1)]=number
                        # delet the 2 last position in the array for the 6 nodes shell elements
                        if len(nodes)==6:
                            del nodin[-2:]                                                  
                        nodin=[gnodes[n] for n in nodin]
                         # create the 8 nodes shell element
                        if len(nodin)==8:
                            self.fem_2d.gelmnt1[new_elnum]=GELMNT1(new_elnum,eltype=SHELL_8,eltyad=0,nodin=nodin)
                        # create the 6 nodes shell element
                        if len(nodin)==6:
                            self.fem_2d.gelmnt1[new_elnum]=GELMNT1(new_elnum,eltype=SHELL_6,eltyad=0,nodin=nodin)
                        #new_el_dic[new_elnum]=elment
                        new_elnum+=1                                             
      
    

    def _create_GELREF1(self,elements:dict[int,int]):
        for el_2d, el_3d in elements.items():          
            self.fem_2d.gelref1[el_2d]=GELREF1(matno=self.fem_3d.gelref1[el_3d].matno,addno=1,intno=0,mintno=0,strano=0,streno=0,strepono=0,geono=1,fixno=0,eccno=0,transno=0) 

    def _create_BEUSLO(self,lc,elements,mod_lc=1):
        for element in elements:
            if mod_lc not in self.fem_2d.beuslo:
                self.fem_2d.beuslo[mod_lc]={}
            if element not in  self.fem_2d.beuslo[mod_lc]:
                self.fem_2d.beuslo[mod_lc][element]={}
                self.fem_2d.beuslo[mod_lc][element][2]={}
            type=self.fem_2d.gelmnt1[element].eltype
            
            
            if type==SHELL_8:
                self.fem_2d.beuslo[mod_lc][element][2] =BEUSLO(loadtyp=1,complx=0,layer=0,ndof=8,intno=0,side=2,rload=[-1,-1,-1,-1,-1,-1,-1,-1])
            elif type==SHELL_6:
                self.fem_2d.beuslo[mod_lc][element][2]=BEUSLO(loadtyp=1,complx=0,layer=0,ndof=6,intno=0,side=2,rload=[-1,-1,-1,-1,-1,-1])
           
             

    def _create_GETSEMEMB(self,elements,setnum,base_setnumbers):
        fliped=self.fliip_element_dict(elements)
        new_setnums=[]
        
        
        
        for base_setnum in base_setnumbers:
            idx_count=0
            idxnum=1
        
            if setnum not in self.fem_2d.gsetmemb:
                self.fem_2d.gsetmemb[setnum]={}        
            new_el_set=[]
            for idx,v in self.fem_3d.gsetmemb[base_setnum].items():
                for el in v.irmemb:
                    if el in fliped:
                        new_el_set.extend(fliped[el])
                    
            idx_count=1
            idxnum=1
        
            for el in new_el_set:                      
                if idx_count==1:
                    self.fem_2d.gsetmemb[setnum][idxnum]=GSETMEMB()
                if idx_count==1024-4:
                    self.fem_2d.gsetmemb[setnum][idxnum].nfield=1024
                    idxnum+=1
                    idx_count=1
                    self.fem_2d.gsetmemb[setnum][idxnum]=GSETMEMB()
                    
                self.fem_2d.gsetmemb[setnum][idxnum].irmemb.append(el)
                idx_count+=1   

            if idx_count !=1024-6:
                self.fem_2d.gsetmemb[setnum][idxnum].nfield=idx_count+4
            new_setnums.append(setnum)
            setnum+=1
        return new_setnums      
            
    def _create_TDSETNAME(self,setnums):
        for setnum in setnums:
            self.fem_2d.tdsetnam[setnum]=TDSETNAM(4,124,124,f'Set{setnum}')        


            
    def _create_DATE(self)->None:   
        self.fem_2d.date= self.fem_3d.date 


    def _creat_IDENT(self,num)->None:
        if num==None:
            self.fem_2d.ident= self.fem_3d.ident   
        else:
            self.fem_2d.ident[1]=IDENT(self.fem_3d.ident[1].slevel,self.fem_3d.ident[1].selmod)
        
    
    def _create_GELTH(self,thick):
        self.fem_2d.gelth[1]=GELTH(thick,0)
        
    def _create_MISOSEL(self,matno):        
        self.fem_2d.misosel[matno]=self.fem_3d.misosel[matno]  


    def _find_duplicated_nodes(self):
        temp_dic={}
        dup_dic={}
        for node,value in self.fem_2d.gcoord.items():
            key=f'{value.xcoord}_{value.ycoord}_{value.zcoord}'
            if key not in temp_dic:
                temp_dic[key]=node
            else:
                dup_dic[temp_dic[key]]=node
        return dup_dic

    @staticmethod
    def fliip_element_dict(elements:dict[int,int])->dict[int,list[int]]:
        fliped={}
        for new,old in elements.items():
            if old not in fliped:
                fliped[old]=[]
                fliped[old].append(new)
                continue
            fliped[old].append(new)
        return fliped