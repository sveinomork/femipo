from pathlib import Path
import pytest
from femipo.fem.fem import FEM

@pytest.fixture
def file_path(tmp_path: Path) -> Path:
    file = tmp_path / "test_file.txt"
    file.write_text("""IDENT     1.00000000E+00  1.10000000E+01  3.00000000E+00  0.00000000E+00
BNLOAD    6.60000000e+01  1.00000000e+00  0.00000000e+00  0.00000000e+00
          3.92192000e+05  3.00000000e+00  1.00000000e+00  0.00000000e+00
          0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00""")
    return file

def test_read_bnload(file_path):
    fem_obj = FEM()
    fem_obj.read_fem(file_path)

    # Check key values for the BNLOAD object
    bnload = fem_obj.bnload[int(float(6.60000000e+01))][int(float(3.92192000e+05))  ]
    assert bnload.lotyp == float(1.00000000e+00)
    assert bnload.complex == float(0.00000000e+00)
    assert bnload.ndof ==float(3.00000000e+00)
    assert bnload.rload[2] == float(0.00000000e+00)