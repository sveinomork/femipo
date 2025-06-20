from pathlib import Path
import pytest
from femipo.fem.fem import FEM
from src.femipo.fem.cards.gbeamg import GBEAMG
from src.femipo.fem.read import READ

@pytest.fixture
def file_path(tmp_path: Path) -> Path:
    # Create a temporary file within the pytest temporary directory
    file = tmp_path / "test_file.txt"
    
    # Write the content to the file
    file.write_text("""IDENT     1.00000000E+00  1.10000000E+01  3.00000000E+00  0.00000000E+00
GBEAMG    2.00000000e+01  0.00000000e+00  7.28480935e-01  7.99413729e+00
          3.99706864e+00  3.99706864e+00  0.00000000e+00  2.40056276e+00
          1.20028138e+00  1.20028138e+00  3.64247262e-01  3.64247262e-01
          0.00000000e+00  0.00000000e+00  7.68145263e-01  7.68145263e-01
          1.32000000e-04  0.00000000e+00  7.68145263e-01  7.68145263e-01""")
    
    return file

def test_read_gbeamg(file_path):
    fem_obj = FEM()
    fem_obj.read_fem(file_path)
    
    # Test key properties of the GBEAMG object
    assert fem_obj.gbeamg[int(float(2.00000000e+01))].area == float(7.28480935e-01)
    assert fem_obj.gbeamg[int(float(2.00000000e+01))].ix == float(7.99413729e+00)
    assert fem_obj.gbeamg[int(float(2.00000000e+01))].wymin == float(1.20028138e+00)
    assert fem_obj.gbeamg[int(float(2.00000000e+01))].wxmin == float(2.40056276e+00)
    assert fem_obj.gbeamg[int(float(2.00000000e+01))].shceny == float(0.00000000e+00)
    assert fem_obj.gbeamg[int(float(2.00000000e+01))].wpy == float(1.32000000e-04)

