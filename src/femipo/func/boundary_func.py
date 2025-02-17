
from ..fem.fem_base import FEM_BASE
from .func_template import FUNC_TEMPLATE
from ..fem.cards.bnbcd import BNBCD
import logging
logger = logging.getLogger(__name__)

   

class NODE_FUNC(FEM_BASE,FUNC_TEMPLATE):
    def _add_bnbc_card(self)->None:
        if "BNBCD" not in self.cards:
            self.cards.append("BNBCD")

    
    def add_bnbc(self,nodes:list[int],fix:list[int])->None:
        self._add_bnbc_card()
        for node in nodes:
            self.bnbcd[node]=BNBCD(6,fix)
        
        
        
