from src.actiongraphgen.structure.action_graph import ActionGraph


class Generator:
    def __init__(self, max_nodes: int, param_types: dict, processes: dict) -> None:
        self.max_nodes = max_nodes
        self.param_types = param_types
        self.processes = processes
        self.action_graph = ActionGraph(max_nodes, param_types)
