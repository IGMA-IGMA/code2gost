from abc import ABC, abstractmethod

class ParserBase(ABC):
    @abstractmethod
    def parse(self, code: str):
        """Return (nodes, edges). Nodes: objects with id,label,type; Edges: objects with from_id,to_id,label(optional)"""
        pass
