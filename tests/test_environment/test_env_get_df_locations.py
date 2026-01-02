import pandas as pd
import pop2net as p2n


def test_1():
    env = p2n.Environment()

    class Classroom(p2n.LocationDesigner):
        pass

    class School(p2n.LocationDesigner):
        pass

    df = pd.DataFrame(
        {"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]}
    )
    actor_dict = df.to_dict()
    for i in range(len(actor_dict["status"])):
        actor = p2n.Actor()
        actor.status = actor_dict["status"][i]
        actor.class_id = actor_dict["class_id"][i]
        env.add_actor(p2n.Actor())

    school = School()
    classroom = Classroom()
    classroom.label = "Biology"
    env.add_location(school)
    env.add_location(classroom)
    school.add_actors(env.actors)
    classroom.add_actors(env.actors[:2])

    df_locations = env.get_df_locations()
    
    assert df_locations.shape[0] == 2
    assert df_locations.label.to_list() == ["School", "Biology"]
    assert df_locations.type.to_list() == ["School", "Classroom"]
