from dataclasses import dataclass,field
from typing import IO
from . import util_func

@dataclass
class GCOORD:
  
    xcoord:float
    ycoord:float
    zcoord:float

    # Optional instance-specific tolerance (different from global default)
    # Using field() with default_factory to avoid mutable default issues
    tolerance: float = field(default=1e-3)
    
    def print(self,nodeno):
        TFEMmod=[]
        TFEMmod.append("GCOORD    ")
        TFEMmod.append(f'{nodeno:1.8E} {self.xcoord: 1.8E} {self.ycoord: 1.8E} {self.zcoord: 1.8E}\n')               
        return TFEMmod
    
    def print_file(self,nodeno,file:str):
        TFEMmod=self.print(nodeno)
        util_func.append_lines_to_file(TFEMmod,file)

    def print_abaqus(self,nodeno:int)->list[str]:
       
        return [f'{nodeno}, {self.xcoord}, {self.ycoord}, {self.zcoord}\n']
    
    @staticmethod
    def create(line:str,fin:IO)->tuple[int,list[float]]:
        data=util_func.getdata(line,fin,1)
        return (int(data[0]),[data[1],data[2],data[3]] )
    
    def __eq__(self, other):
        """
        Compare two points for equality using the class tolerance.
        
        Args:
            other: Another Point object to compare with
            
        Returns:
            True if points are equal within tolerance, False otherwise
        """
        if not isinstance(other, GCOORD):
            return NotImplemented
            
        return (abs(self.xcoord - other.xcoord) <= self.tolerance and 
                abs(self.ycoord - other.ycoord) <= self.tolerance and 
                abs(self.zcoord - other.zcoord) <= self.tolerance)
    
    def equals_with_tolerance(self, other, tolerance=1e-6):
        """
        Compare two points with a custom tolerance.
        
        Args:
            other: Another GCOORD object to compare with
            tolerance: Custom tolerance for this comparison
            
        Returns:
            True if points are equal within the specified tolerance
        """
        if not isinstance(other, GCOORD):
            return False
            
        return (abs(self.xcoord - other.xcoord) <= tolerance and 
                abs(self.ycoord - other.ycoord) <= tolerance and 
                abs(self.zcoord - other.zcoord) <= tolerance)