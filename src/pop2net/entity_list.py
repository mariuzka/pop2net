from .actor import Actor
from .location import Location


class EntityList(list):
    """Simple list subclass for better print out."""

    def __str__(self):
        n = len(self)
        if n == 0:
            return "EntityList [ ]"

        actor_count = sum(isinstance(o, Actor) for o in self)
        location_count = sum(isinstance(o, Location) for o in self)
        unknown = n - actor_count - location_count

        parts = []
        if actor_count:
            parts.append(f"{actor_count} {'actor' if actor_count == 1 else 'actors'}")
        if location_count:
            parts.append(f"{location_count} {'location' if location_count == 1 else 'locations'}")
        if unknown:
            parts.append(f"{unknown} {'entity' if unknown == 1 else 'entities'}")

        return f"EntityList [{', '.join(parts)}]"

    def __repr__(self):
        return self.__str__()
