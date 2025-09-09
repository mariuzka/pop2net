class EntityList(list):
    """Simple list subclass for better print out."""

    def __str__(self):
        return "EntityList [ ]" if len(self) == 0 else f"EntityList [{len(self)} entities]"

    def __repr__(self):
        return "EntityList [ ]" if len(self) == 0 else f"EntityList [{len(self)} entities]"
