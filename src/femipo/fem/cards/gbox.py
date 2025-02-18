from dataclasses import dataclass
from typing import IO
from . import util_func

@dataclass
class GBOX:
    #key
    #geono unit vector number refered to on record GELREF1
    hz:float # height of beam current location
    ty:float  #thickness of beam web
    tb:float  # thickness of  bottom flang
    tt:float # thickness of top and bottom flang
    by:float #factors modifying the shear areas calculated by the preprocessor program
    sfy:float
    sfz:float
    nloby:float=0 #number of integration points in each hoirzontal wall (flange) of beam 
    nlobz:float=0
    

    def print(self,geono):
        TFEMmod = []
        TFEMmod.append(f'GBOX      {geono:1.8E}  {self.hz:1.8E}  {self.ty:1.8E}  {self.tb:1.8E}\n')
        TFEMmod.append(f'          {self.tt:1.8E}  {self.by:1.8E}  {self.sfy:1.8E}  {self.sfz:1.8E}\n')
        #TFEMmod.append(f'          {self.nloby:1.8E}  {self.nlobz:1.8E}  \n')
       
        return TFEMmod
    
 
    
    def print_file(self,geono,file:str):
        TFEMmod=self.print(geono)
        util_func.append_lines_to_file(TFEMmod,file)
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,2)
        return (data[0],[*data[1::]] )
