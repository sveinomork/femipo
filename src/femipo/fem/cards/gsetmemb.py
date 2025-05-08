from dataclasses import dataclass,field
from typing import IO
from . import util_func
import math


@dataclass
class GSETMEMB:
    #index in dic isref_index
    #isref is key
    
    #isref:int  # internal set identification number
    #index:int # sequential record number
    
    nfield:int=0
    istype:int=2 #set type 1:nodes 2:elements
    isorgi:int=1
    irmemb:list[int]=field(default_factory=list)

    
   
    
    
    def print(self,isref,istype,index):
        TFEMmod = []                      
        TFEMmod.append(f'GSETMEMB  {self.nfield:1.8E}  {isref:1.8E}  {index:1.8E}  {istype:1.8E}\n')
        TFEMmod.append(f'          {self.isorgi:1.8E}  {self.irmemb[0]:1.8E}  {self.irmemb[1]:1.8E}  {self.irmemb[2]:1.8E}\n')
        TFEMmod.append("        ")
        util_func.printDataItem(TFEMmod,self.irmemb[3:])
        TFEMmod.append("\n")            
          
        return TFEMmod
    
    def print_abaqus(self)->list[str]:
        return_list:list[str]=[]
       
        for i in range(0, len(self.irmemb), 16):
            return_list.append(f"    {', '.join(str(self.irmemb[j]) for j in range(i, min(i + 16, len(self.irmemb))))}\n")  
        
        return return_list
    
    def print_file(self,isref:int,istype:int,index,file:str):
        TFEMmod=self.print(isref,istype,index)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,int,int,list[int| list[int]]]:
        data=util_func.getdata(line,fin,1)
        nfield=int(data[0]) # number of data fields on this record       
        isref=int(data[1])   # internal set identification number as defined TDSETNAME
        index=int(data[2])   # sequential record number for current set
        istype=int(data[3])  # 1 set of nodes, 2 set of elements        
        data=util_func.getdata(line,fin,math.ceil(nfield/4))
        isorgi=int(data[4])
        irmemb=[int(el) for el in data[5:]]               
        return (isref,istype,index,[nfield,istype,isorgi,irmemb])


    

