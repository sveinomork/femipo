from dataclasses import dataclass,field
from . import util_func
from typing import IO

@dataclass
class BNLOAD:
    """Class to represent a node with load"""   
    # key is llc
    # secend key is nodeno
    lotyp:int
    complex:int

    ndof:int
    rload:list[int]=field(default_factory=list)
    
    def print(self,llc:int,nodeno:int):
        TFEMmod = []                      
        TFEMmod.append(f'BNLOAD    {llc:1.8E}  {self.lotyp:1.8E}  {self.complex:1.8E}  \n')
        TFEMmod.append(f'          {nodeno:1.8E}  {self.ndof:1.8E}  {self.rload[0]:1.8E}  {self.rload[1]:1.8E}\n')  

        if self.ndof == 6:
            TFEMmod.append(f'          {self.rload[2]:1.8E}  {self.rload[3]:1.8E}  {self.rload[4]:1.8E}  {self.rload[5]:1.8E}\n')        
        else:
            TFEMmod.append(f'          {self.rload[2]:1.8E}  \n')
        return TFEMmod
    
    def print_file(self,llc:int,nodeno:int,file:str):
        TFEMmod=self.print(llc,nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,int,list[int|list[int]]]:
        data=util_func.getdata(line,fin,3)
        return (int(data[0]),int(data[3]),[int(data[1]),int(data[2]),int(data[5]),[int(i) for i in data[6:]]])
    