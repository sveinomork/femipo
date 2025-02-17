from src.femipo.fem.fem import FEM
from shapely.geometry import Point
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


if __name__ == "__main__":
    main()
   
