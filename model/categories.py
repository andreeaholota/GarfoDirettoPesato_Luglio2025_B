from dataclasses import dataclass

@dataclass
class Category:
    category_id: int
    category_name: str = None


    def __hash__(self):
        return hash(self.category_id)

    def __eq__(self,other):
        return isinstance(other,Category) and self.category_id == other.category_id


