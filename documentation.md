# Example Code from main.py

Here is an example of how to use the `FEM` class to read a FEM file and get nodes in a load case.

```python
from src.femipo.fem.fem import FEM

def main():
    fem_obj = FEM()
    fem_obj.read_fem(r'C:\Users\nx74\femip_test\T11.FEM')
    n = fem_obj.get_nodes_in_lc(1)
    print(n)

if __name__ == "__main__":
    main()
```