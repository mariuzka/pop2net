import pandas as pd
from pop2net.inspector import NetworkInspector
from pop2net.actor import Actor
from pop2net.location import Location
from pop2net.environment import Environment


def test_location_information_df():
    
    def setup_env():
        env = Environment()
        a1 = Actor() 
        a1.status = "pupil"
        a2 = Actor()
        a2.status = "teacher"
        loc = Location()
        loc.label = "TestLoc"
        env.add_actors([a1, a2])
        env.add_location(loc)
        [env.add_actor_to_location(loc, actor) for actor in env.actors]
        return env
    
    env = setup_env()
    inspector = NetworkInspector(env)
    df = inspector.location_information(
        location_labels="TestLoc",
        actor_attributes=["status", "id_p2n"],
        output_format="df"
    )
    assert isinstance(df, pd.DataFrame)
    # expect 2 rows, one per actor
    assert len(df) == 2
    # columns: location_id, status, id_p2n, location_type
    assert list(df.columns) == ["location_id", "status", "id_p2n", "location_type"]
    # location_id constant 0, location_type correct
    assert set(df["location_id"]) == {0}
    assert set(df["location_type"]) == {"TestLoc"}
    # statuses present
    assert set(df["status"]) == {"teacher", "pupil"}

def test_location_information_table(capsys):

    def setup_env():
        env = Environment()
        a1 = Actor() 
        a1.status = "pupil"
        a2 = Actor()
        a2.status = "teacher"
        loc = Location()
        loc.label = "TestLoc"
        env.add_actors([a1, a2])
        env.add_location(loc)
        [env.add_actor_to_location(loc, actor) for actor in env.actors]
        return env

    env = setup_env()
    inspector = NetworkInspector(env)
    result = inspector.location_information(
        location_labels="TestLoc",
        actor_attributes="status",
        output_format="table"
    )
    # table mode returns None and prints header + table
    assert result is None
    captured = capsys.readouterr().out
    assert "1.Location: TestLoc" in captured
    assert "teacher" in captured and "pupil" in captured
