class Family:
    """A family tree"""
    def __init__(self,name):
        """Initializing function

        Args:
            name (str): name of the family
        """
        self.name = name
        self.parents = []  # List to store parents - Tysen
        self.children = []  # List to store children -Tysen
    def add_parent(self, parent_name):
        """Add a parent to the family tree

        Args:
            parent_name (str): Name of the parent to add
        """
        self.parents.append(parent_name) # Appends parent name to parent list - Guy

    def add_child(self, child_name):
        """Add a child to the family tree

        Args:
            child_name (str): Name of the child to add
        """
        self.children.append(child_name) # Appends child name to child list
