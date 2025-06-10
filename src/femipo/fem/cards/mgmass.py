from dataclasses import dataclass,field
from . import util_func
from typing import IO


@dataclass
class MGMASS:
    #key
    #manto:int
    ndof:int
    m:list[float]=field(default_factory=list)
 
    
    def print(self,matno):
        if self.ndof != 6: 
            raise ValueError(f"ndof must be 6, but got {self.ndof}")
        TFEMmod = []                      
        TFEMmod.append(f'MGMASS    {matno:1.8E}  {self.ndof:1.8E}  {self.m[0]:1.8E}  {self.m[1]:1.8E}\n')
        TFEMmod.append(f'          {self.m[2]:1.8E}  {self.m[3]:1.8E}  {self.m[4]:1.8E}  {self.m[5]:1.8E}\n')
        TFEMmod.append(f'          {self.m[6]:1.8E}  {self.m[7]:1.8E}  {self.m[8]:1.8E}  {self.m[9]:1.8E}\n')
        TFEMmod.append(f'          {self.m[10]:1.8E}  {self.m[11]:1.8E}  {self.m[12]:1.8E}  {self.m[13]:1.8E}\n')
        TFEMmod.append(f'          {self.m[14]:1.8E}  {self.m[15]:1.8E}  {self.m[16]:1.8E}  {self.m[17]:1.8E}\n')
        TFEMmod.append(f'          {self.m[18]:1.8E}  {self.m[19]:1.8E}  {self.m[20]:1.8E}  {self.m[21]:1.8E}\n')
        return TFEMmod
    
    def print_file(self,matno,file:str):
        TFEMmod=self.print(matno)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float|list[float]]]:
        data=util_func.getdata(line,fin,6)
        
        return (int(data[0]),[int(data[1]),[float(data[i+2]) for i in range(22)]])