# Class for node data storage/params
class NodeData:
    def __init__(self, max_nodes: int, param_types: dict) -> None:
        self.max_nodes = max_nodes
        self.param_types = param_types
        self.data_list = self._init_data()

    def _init_data(self) -> list[dict]:
        # Initializes the structure of a node param dictionary list filled with None
        lst = []
        for _ in range(self.max_nodes):
            data_dict = {param: None for param, dtype in self.param_types.items()}
            lst.append(data_dict)
        return lst
