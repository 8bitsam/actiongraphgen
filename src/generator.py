class Generator:
    def __init__(self, fill : function, processes : dict) -> None:
        self.processes = processes
        self.fill = fill