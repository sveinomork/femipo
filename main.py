from calendar import c
from femipo import fem
from src.femipo.fem.fem import FEM
from src.femipo.fem.revolve import Revolve,Alfa
from src.femipo.fem.asembly import ASSEMBLY
from shapely import Point

import math
def main():
    fem_obj=FEM()
    fem_obj.read_fem(r'C:\Users\nx74\femip_test\T11.FEM')
    n=a.get_nodes_in_lc(1)
    print("stopp")
    
    def linz(z:float,value:float)->tuple[float,float,float]:
        if z<0.5:
            return int(value*(151.9359911-z*100)),0,0
        else:
            return 0,0,0
    def const(x,y,z,value:float)->float:
        return 1.0

    
    p1=Point(0,0,0.0)
    p2=Point(1.0,0.0,0.0)
    p3=Point(1.0,1.0,0.0)

    at=fem_obj.get_surf_element_side(p1,p2,p3)

    fem_obj.create_beuslo(lc=1,loadtype=1,load_surf=at,load_func=const,lf=1,value=1)

    fem_obj.write(f'T111.FEM')

def main2():
    center=Point(0,0,0)
    p2=Point(0.0,1,0)
    alfa=180


    def calc_new_point(center: Point, p2: Point, alfa: float) -> Point:
        # Calculate the angle of p2 relative to center
        current_angle = math.atan2(p2.y - center.y, p2.x - center.x)
        
        # Calculate radius from the given point
        r = math.sqrt((p2.x - center.x)**2 + (p2.y - center.y)**2)
        
        # Calculate new angle by adding alfa (converted to radians)
        new_angle = current_angle + math.radians(alfa)
        
        # Calculate new coordinates
        x3 = center.x + r * math.cos(new_angle)
        y3 = center.y + r * math.sin(new_angle)
        
        return Point(x3, y3, center.z)
    
    nx=calc_new_point(center,p2,alfa)
    print(f'{nx.x},{nx.y}')
    print(f'{nx.x},{nx.y}')

def main3():
    fem_obj_2d=FEM()
    fem_obj_2d.read_fem(r'C:\Users\nx74\Work\femipo\src\T55.FEM')
    fem_obj_3d=FEM()
    _alafas=[0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0]
    #_alafas2=[0.0,20.0,40.0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,220.0,240.0,260.0,280.0,300.0,320.0,340.0]
    _alafas=[0.0,10.0,20,30]
    alfas=[Alfa(start=alfa,stop=alfa+10) for alfa in _alafas]
    #alfas2=[Alfa(start=alfa,stopp=alfa+10) for alfa in _alafas2]
    rev=Revolve(fem_obj_2d,fem_obj_3d,Point(0,0,0))
    
    base_elements=[5]
    rev.create_solid_from_shell(base_elements,alfas,1,1)
    rev._create_node_set(alfas,[2],2,"surfaces")
    #rev._create_boundary_condition(alfas,[2],[1,1,1])
    #rev.create_solid_from_shell([4],alfas,1)
    def const(x,y,z,value:float)->float:
        return 1.0

    rev._create_loads(alfas,[2],1,const)
    #rev.(lc=1,loadtype=1,load_surf=at,load_func=const,lf=1,value=1)










    fem_obj_3d.write(r'C:\Users\nx74\Work\femipo\src\T11.FEM')
    print("stopp")

def main4():
    fem_obj_2d=FEM()
    fem_obj_2d.read_fem(r'C:\Users\nx74\Work\femipo\src\T1.FEM')
    fem_obj_3d1=FEM()
    fem_obj_3d2=FEM()
   
    _alafas1=[0.0,10.0]
    alfas1=[Alfa(start=alfa,stop=alfa+10) for alfa in _alafas1]

    _alafas2=[0.0,-10.0]
    alfas2=[Alfa(start=alfa,stop=alfa-10) for alfa in _alafas2]
   
   
    #alfas2=[Alfa(start=alfa,stopp=alfa+10) for alfa in _alafas2]
    rev1=Revolve(fem_obj_2d,fem_obj_3d1,Point(0,0,0))
    rev2=Revolve(fem_obj_2d,fem_obj_3d2,Point(0,0,0))
    
    base_elements=[1]
    rev1.create_solid_from_shell(base_elements,alfas1,1,create_set=False)
    rev2.create_solid_from_shell(base_elements,alfas2,1,create_set=False)
    
    fem_obj_3d1.write(r'C:\Users\nx74\Work\femipo\src\T5.FEM')
    fem_obj_3d2.write(r'C:\Users\nx74\Work\femipo\src\T6.FEM')

    assembly=ASSEMBLY(fem_obj_3d1)
    assembly.add(fem_obj_3d2)
    fem_obj_3d1.write(r'C:\Users\nx74\Work\femipo\src\T7.FEM')
    print("stopp")

    
def main5():
    shel=f'C:\DNV\Workspaces\GeniE\T1.FEM'
    fem_obj_2d=FEM()
    fem_obj_2d.read_fem(shel)
    p1=Point(0,0,0.0)
    p2=Point(1.0,0.0,0.0)
    p3=Point(0.0,0.0,1.0)

    at=fem_obj_2d.get_surf_element_side(p1,p2,p3)
    
    def const(x,y,z,value:float)->float:
        return value
    fem_obj_2d.create_beuslo(lc=11,loadtype=1,load_surf=at,load_func=const,lf=1,value=1)
  
    fem_obj_2d.write(r'C:\Users\nx74\Work\femipo\src\T8.FEM')

    print("finish")

def main6():
    def outer_pres1(x,y,z,value)->float:
        if z<=22.567:
            return (22.567-z)*10.05
        
        return 0
    
    def outer_pres2(x,y,z)->float:
        if z<=13.649:
            return (13.649-z)*10.05
        
        return 0.0
    
  
    
    def outer_pres3(x,y,z)->float:
        if z<=19.08106321:
            return (19.08106321-z)*10.05
        
        return 0.0
    
    def outer_pres4(x,y,z)->float:
        if z<=16.18525254:
            return (16.18525254-z)*10.05
        
        return 0.0

    def comp_pres1(x,y,z)->float:
        if z<=16.18525254:
            return (16.18525254-z)*10.05
        
        return 0.0
    
    def comp_pres2(x,y,z)->float:
        if z<=11.5:
            return (11.5-z)*10.05
        
        return 0.0
    
    
    
    
    def comp_pres3(x,y,z)->float:
        if z<=7.3:
            return (7.3-z)*10.05

        return 0.0
    
    def comp_pres4(x,y,z)->float:
        if z<=3.7:
            return (3.7-z)*10.05

        return 0
       
    shel=r'C:\Users\nx74\Work\femipo\T1.FEM'
    fem_obj=FEM()
    fem_obj.read_fem(shel)
    fem_obj.create_beusol_based_on_lc(lc=79,base_lc=2,load_type=1,load_func=outer_pres1,lf=1.0)
    print(f'LOADC RN=1 LC=17,111   % Outer water pressure 22.5m')
    fem_obj.create_beusol_based_on_lc(lc=80,base_lc=2,load_type=1,load_func=outer_pres2,lf=1.0)
    print(f'LOADC RN=1 LC=18,112   % Outer water pressure 13.65m')
    start_lc=81
    for i in range(9):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+i,base_lc=54+i,load_type=1,load_func=comp_pres1,lf=1.0)
        #print(f'create load {start_lc+i} based on {54+i}')
        print(f'LOADC RN=1 LC={start_lc+i},{110+i}  ')
      
    for i in range(3):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+9+i,base_lc=63+i,load_type=1,load_func=comp_pres1,lf=1.0)
        #print(f'create load {start_lc+9+i} based on {63+i}')
        print(f'LOADC RN=1 LC={start_lc+9+i},{120+i}  ')
    
    start_lc=start_lc+12
    for i in range(9):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+i,base_lc=54+i,load_type=1,load_func=comp_pres2,lf=1.0)
        #print(f'create load {start_lc+i} based on {2+i}')
        print(f'LOADC RN=1 LC={start_lc+i},{130+i}  ')
      
    for i in range(3):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+9+i,base_lc=63+i,load_type=1,load_func=comp_pres2,lf=1.0)
        #print(f'create load {start_lc+9+i} based on {14+i}')
        print(f'LOADC RN=1 LC={start_lc+9+i},{140+i}  ')
    
    start_lc=start_lc+12
    for i in range(9):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+i,base_lc=54+i,load_type=1,load_func=comp_pres3,lf=1.0)
        #print(f'create load {start_lc+9+i} based on {2+i}')
        print(f'LOADC RN=1 LC={start_lc+i},{150+i}  ')
      
    for i in range(3):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+9+i,base_lc=63+i,load_type=1,load_func=comp_pres3,lf=1.0)
        #print(f'create load {start_lc+9+i} based on {14+i}')
        print(f'LOADC RN=1 LC={start_lc+9+i},{160+i}  ')
    
    start_lc=start_lc+12
    for i in range(9):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+i,base_lc=54+i,load_type=1,load_func=comp_pres4,lf=1.0)
        #print(f'create load {start_lc+i} based on {2+i}')
        print(f'LOADC RN=1 LC={start_lc+i},{170+i}  ')
      
    for i in range(3):
        fem_obj.create_beusol_based_on_lc(lc=start_lc+9+i,base_lc=63+i,load_type=1,load_func=comp_pres4,lf=1.0)
        #print(f'create load {start_lc+9+i} based on {14+i}')
        print(f'LOADC RN=1 LC={start_lc+9+i},{180+i}  ')
   
    fem_obj.create_beusol_based_on_lc(lc=130,base_lc=2,load_type=1,load_func=outer_pres3,lf=1.0)
    print(f'LOADC RN=1 LC=17,111   % Outer water pressure 22.5m')
    fem_obj.create_beusol_based_on_lc(lc=131,base_lc=2,load_type=1,load_func=outer_pres4,lf=1.0)
    print(f'LOADC RN=1 LC=18,112   % Outer water pressure 13.65m')


    fem_obj.create_grav(lc=129)
    print(f'LOADC RN=1 LC=76,101   % Dead weight')
    
    
    fem_obj.write(r'C:\Users\nx74\Work\femipo\T2.FEM')
    

    
    pass

if __name__ == "__main__":
    main6()

