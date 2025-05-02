from src.femipo.fem.fem import FEM
from src.femipo.fem.revolve import Revolve,Alfa
from shapely.geometry import Point
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
    fem_obj_2d.read_fem(r'C:\Users\nx74\Work\femipo\src\T11.FEM')
    fem_obj_3d=FEM()
    _alafas=[0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0,190.0,200.0,210.0,220.0,230.0,240.0,250.0,260.0,270.0,280.0,290.0,300.0,310.0,320.0,330.0,340.0,350.0]
    #_alafas2=[0.0,20.0,40.0,60.0,80.0,100.0,120.0,140.0,160.0,180.0,200.0,220.0,240.0,260.0,280.0,300.0,320.0,340.0]
    _alafas=[0.0,10.0]
    alfas=[Alfa(start=alfa,stopp=alfa+10) for alfa in _alafas]
    #alfas2=[Alfa(start=alfa,stopp=alfa+10) for alfa in _alafas2]
    rev=Revolve(fem_obj_2d,fem_obj_3d,Point(0,0,0))
    
    base_elements=[5]
    rev.create_solid_from_shell(base_elements,alfas,1)
    rev._create_set(alfas,[2],1,"surfaces")
    #rev.create_solid_from_shell([4],alfas2,1)
    fem_obj_3d.write(r'C:\Users\nx74\Work\femipo\src\T31.FEM')
    print("stopp")


    
     

if __name__ == "__main__":
    main3()

