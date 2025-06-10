from femipo.fem.cards import mgmass
from .cards.ident import IDENT
from .cards.date import DATE
from .cards.text import TEXT
from .cards.gcoord import GCOORD
from .cards.gnode import GNODE
from .cards.misosel import MISOSEL
from .cards.gelmnt1 import GELMNT1
from .cards.gelref1 import GELREF1
from .cards.gsetmemb import GSETMEMB
from .cards.tdsetnam import TDSETNAM
from .cards.tdload import TDLOAD    
from .cards.beuslo import BEUSLO
from .cards.bnbcd import BNBCD
from .cards.units import UNITS
from .cards.tdmater import TDMATER
from .cards.bgrav import BGRAV
from .cards.tdsect import TDSECT
from .cards.gelth import GELTH
from .cards.gbeamg import GBEAMG
from .cards.giorh import GIORH
from .cards.gchan import GCHAN  
from .cards.gbox import GBOX        
from .cards.gpipe import GPIPE          
from .cards.gbarm import GBARM  
from .cards.glsec import GLSEC
from .cards.giorhr import GIORHR    
from .cards.tdsconc import TDSCONC
from .cards.sconcept import SCONCEPT
from .cards.sconmesh import SCONMESH
from .cards.sconplis import SCONPLIS
from .cards.sprosele import SPROSELE
from .cards.sprocode import SPROCODE
from .cards.gunivec import GUNIVEC
from .cards.geccen import GECCEN
from .cards.tdnode import TDNODE
from .cards.belfix import BELFIX
from .cards.bldep import BLDEP
from .cards.gchanr import GCHANR
from .cards.hierarch import HIERARCH
from .cards.hsupstat import HSUPSTAT
from .cards.hsuptran import HSUPTRAN
from .cards.mgmass import MGMASS


from collections import OrderedDict

from dataclasses import dataclass,field
@dataclass
class FEM_BASE():
    
    cards:list[str]=field(default_factory=list)
    ident: dict[int,IDENT] = field(default_factory=dict)
    date:dict[int,DATE]=field(default_factory=dict)
    text:dict[int,TEXT]=field(default_factory=dict)
    gcoord: OrderedDict[int,GCOORD]= field(default_factory=OrderedDict)
    gnode: OrderedDict[int,GNODE] = field(default_factory=OrderedDict)
    misosel:dict[int,MISOSEL]=field(default_factory=dict)
    gelmnt1: OrderedDict[int,GELMNT1] = field(default_factory=OrderedDict)
    gelref1: OrderedDict[int,GELREF1] = field(default_factory=OrderedDict)
    gsetmemb: dict[int,dict[int,dict[int,GSETMEMB]]]=field(default_factory=dict)
    #tdsetnam: dict[int,dict[int,TDSETNAM]]=field(default_factory=dict)
    tdsetnam: dict[int,TDSETNAM]=field(default_factory=dict)
    tdload: dict[int,TDLOAD]=field(default_factory=dict)
    beuslo: dict[int,dict[int,dict[int,BEUSLO]]] = field(default_factory=dict)
    bello2: dict[int,dict[int,dict[int,dict[int,BEUSLO]]]] = field(default_factory=dict)
    bnbcd: dict[int,BNBCD]= field(default_factory=dict)
    units: dict[int,UNITS]= field(default_factory=dict)
    tdmater:dict[int,TDMATER]=field(default_factory=dict)
    bgrav:dict[int,BGRAV]=field(default_factory=dict)
    tdsect:dict[int,TDSECT]=field(default_factory=dict)
    gelth:dict[int,GELTH]=field(default_factory=dict)
    gbeamg:dict[int,GBEAMG]=field(default_factory=dict)
    giorh:dict[int,GIORH]=field(default_factory=dict)
    gchan:dict[int,GCHAN]=field(default_factory=dict)
    gbox:dict[int,GBOX]=field(default_factory=dict)
    gpipe:dict[int,GPIPE]=field(default_factory=dict)
    gbarm:dict[int,GBARM]=field(default_factory=dict)
    glsec:dict[int,GLSEC]=field(default_factory=dict)
    giorhr:dict[int,GIORHR]=field(default_factory=dict)
    tdsconc:dict[int,TDSCONC]=field(default_factory=dict)
    sconcept:dict[int,SCONCEPT]=field(default_factory=dict)
    sconmesh:dict[int,SCONMESH]=field(default_factory=dict)
    sconplis:dict[int,SCONPLIS]=field(default_factory=dict)
    sprosele:dict[int,SPROSELE]=field(default_factory=dict)
    sprocode:dict[int,SPROCODE]=field(default_factory=dict)
    gunivec:dict[int,GUNIVEC]=field(default_factory=dict)
    geccen:dict[int,GECCEN]=field(default_factory=dict)
    tdnode:dict[int,TDNODE]=field(default_factory=dict)
    belfix:dict[int,BELFIX]=field(default_factory=dict)
    bldep:dict[int,BLDEP]=field(default_factory=dict)
    gchanr:dict[int,GCHANR]=field(default_factory=dict)
    hierarch:dict[int,HIERARCH]=field(default_factory=dict)
    hsupstat:dict[int,HSUPSTAT]=field(default_factory=dict)
    hsuptran:dict[int,HSUPTRAN]=field(default_factory=dict)
    mgmass:dict[int,MGMASS]=field(default_factory=dict)
    
    
    

    
   
  
    
   
    


    