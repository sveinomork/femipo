from dataclasses import dataclass,field
from typing import IO
from . import util_func
from ..cards.gelmnt1 import GELMNT1
@dataclass

class GELREF1:
    
    matno:int # mat number
    addno:int #element type number
    intno:int #additonal information related to element typ
    mintno:int
    strano:int
    streno:int
    strepono:int
    geono:int
    fixno:int
    eccno:int
    transno:int
    geonos:list[float]=field(default_factory=list)
    
    def print(self,elno):
        TFEMmod = []
        TFEMmod.append(f'GELREF1   {elno:1.8E}  {self.matno:1.8E}  {self.addno:1.8E}  {self.intno:1.8E}\n') 
        TFEMmod.append(f'          {self.mintno:1.8E}  {self.strano:1.8E}  {self.streno:1.8E}  {self.strepono:1.8E}\n')
        TFEMmod.append(f'          {self.geono:1.8E}  {self.fixno:1.8E} {self.eccno: 1.8E} {self.transno: 1.8E}\n')
        if len(self.geonos)>0:
            TFEMmod.append("        ")
            util_func.printDataItem(TFEMmod,self.geonos)
            TFEMmod.append("\n")  

        return TFEMmod
    
    def print_file(self,elno,file:str):
        TFEMmod=self.print(elno)
        util_func.append_lines_to_file(TFEMmod,file)

    @staticmethod
    def create(line:str,fin:IO,gelmnt1:dict[int,GELMNT1])->tuple[int,list[int|list[float]]]:
        data=util_func.getdata(line,fin,3)
        data= [int(d) if i < 12 else d for i, d in enumerate(data)] 
        
        le=len([var for var in data[8:12] if var < 0])
        if le > 0:
            ndof=len(gelmnt1[int(data[0])].nodin)
            n=(le*ndof)//4+1
            data1=util_func.getdata(line,fin,n+1)
            genos:list[float]=[data1[i+4] for i in range(ndof*le)]

            return (int(data[0]),[int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7]),int(data[8]),int(data[9]),int(data[10]),int(data[11]),genos])
        else:

         return (int(data[0]),[int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7]),int(data[8]),int(data[9]),int(data[10]),int(data[11])])

    def __eq__(self, other):
        if not isinstance(other, GELREF1):
            return NotImplemented
        return (
            self.__dict__ == other.__dict__
        )