class EntityList(list):
    """Simple list subclass for better print out."""

    def __str__(self):
        n = len(self)
        if n == 0:
            return "EntityList [ ]"
        
        # Count objects by type
        actor_count = 0
        location_count = 0
        for obj in self:
            t = getattr(obj, "type", None)
            if t == "Actor":
                actor_count += 1
            elif t == "Location":
                location_count += 1

        parts = []
        if actor_count:
            parts.append(f"{actor_count} {'actor' if actor_count == 1 else 'actors'}")
        if location_count:
            parts.append(f"{location_count} {'location' if location_count == 1 else 'locations'}")

        if parts:
            return f"EntityList [{', '.join(parts)}]"
        
        # TODO keep Fallback if some unknown type or throw exception at this point ? 
        return f"EntityList [{n} entities]"
