

import pytest

from femipo.fem.fem import FEM   # Replace with the actual module and class name

@pytest.fixture(scope="session")
def mock_self():
    """Creates a mock object with gelmnt1 as a dictionary."""

      
    fem_obj_3d=FEM()
    fem_obj_3d.read_fem(r'C:\Users\nx74\feminterface\feminterface\tests\T11.FEM')

   
    return fem_obj_3d

def test_get_element_sides1(mock_self:FEM):

    def find_indices(list_a, list_b):
        indices = []
        for item in list_b:
            if item in list_a:
                indices.append(list_a.index(item)+1)
        return indices
    
    from src.femipo.fem.element_parameters import side_dic_20
   
    ex_node_list=[1,10,15,71,105,100,91,66,2,3,67,93,92]
    int_nodes=mock_self.get_nodes_given_exnodes(ex_node_list)
    indices=find_indices(mock_self.gelmnt1[1].nodin,int_nodes)

    sides=mock_self.get_element_sides(int_nodes,1)
    print(f'indices: {indices=}')
    assert sorted(indices) == sorted(list(set(list(side_dic_20[sides[0]]) + list(side_dic_20[sides[1]]))))
    

def test_get_element_sides2(mock_self:FEM):

    def find_indices(list_a, list_b):
        indices = []
        for item in list_b:
            if item in list_a:
                indices.append(list_a.index(item)+1)
        return indices
    
    from src.femipo.fem.element_parameters import  side_dic_20
   
    ex_node_list=[1,10,15,71,105,100,91,66]
    int_nodes=mock_self.get_nodes_given_exnodes(ex_node_list)
    indices=find_indices(mock_self.gelmnt1[1].nodin,int_nodes)

    sides=mock_self.get_element_sides(int_nodes,1)
    assert sorted(indices) == sorted(side_dic_20[sides[0]])
    assert sides[0] == 100000

