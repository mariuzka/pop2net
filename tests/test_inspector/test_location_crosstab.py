from pop2net.actor import Actor
from pop2net.environment import Environment
from pop2net.inspector import NetworkInspector
from pop2net.location import Location


def test_crosstab_df():
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
    result = inspector.location_crosstab(
        location_labels="TestLoc", actor_attributes="status", output_format="df"
    )
    # should return a list with one DataFrame
    assert isinstance(result, list) and len(result) == 1
    df = result[0]
    # check columns and types
    assert list(df.columns) == ["location_id", "status", "count", "location_type"]
    # two rows for the two statuses
    assert len(df) == 2
    # counts are all 1
    assert set(df["count"]) == {1}
    # statuses appear in 'index'
    assert set(df["status"]) == {"teacher", "pupil"}
    # location_id is 0 and location_type matches
    assert set(df["location_id"]) == {0}
    assert set(df["location_type"]) == {"TestLoc"}


def test_crosstab_table(capsys):
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
    result = inspector.location_crosstab(
        location_labels="TestLoc", actor_attributes="status", output_format="table"
    )
    # table mode returns None and prints fancy grid
    assert result is None
    out = capsys.readouterr().out
    assert "1.Location: TestLoc" in out
    assert "pupil" in out and "teacher" in out
    assert "count" in out
