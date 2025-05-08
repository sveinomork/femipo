from dataclasses import dataclass,field
from . import util_func
from typing import IO

@dataclass
class BNBCD:
    # key is nodeno
    ndof:int
    fix:list[int]=field(default_factory=list)
    
    def print(self,nodeno):
        TFEMmod = []                      
        TFEMmod.append(f'BNBCD     {nodeno:1.8E}  {self.ndof:1.8E}  {self.fix[0]:1.8E}  {self.fix[1]:1.8E}\n')
        if self.ndof == 6:
            TFEMmod.append(f'          {self.fix[2]:1.8E}  {self.fix[3]:1.8E}  {self.fix[4]:1.8E}  {self.fix[5]:1.8E}\n')        
        else:
            TFEMmod.append(f'          {self.fix[2]:1.8E}  \n')
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[int|list[int]]]:
        data=util_func.getdata(line,fin,2)
        return (int(data[0]),[int(data[1]),[int(i) for i in data[2:]]])