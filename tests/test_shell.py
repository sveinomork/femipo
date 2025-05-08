from  femipo.fem.fem  import FEM
from femipo.fem.shell import SHELL
fem_obj_3d=FEM()
fem_obj_2d=FEM()
fem_obj_3d.read_fem(r'C:\Users\nx74\Work\femipo\tests\T100.FEM')

sh=SHELL(fem_obj_3d,fem_obj_2d)

