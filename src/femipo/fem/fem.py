
from .write import WRITE
from .fem_modification import UPDATE
from ..func.node_func import NODE_FUNC
from .read import READ
from ..func.element_func import ELEMENT_FUNC
from ..func.set_func import SET_FUNC
from ..func.load_func import LOAD_FUNC
import pickle
from dataclasses import dataclass

@dataclass(frozen=False)
class FEM(READ,WRITE,NODE_FUNC,ELEMENT_FUNC,UPDATE,SET_FUNC,LOAD_FUNC):


    def save_obj(self,name:str)->None:
        with open(f'{name}', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
    
def load_obj(name)->FEM:   
    with open(f'{name}', 'rb') as f:
        return pickle.load(f) 

