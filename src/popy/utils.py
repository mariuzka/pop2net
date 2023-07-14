import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns


def print_header(text):
    print("")
    print("")
    print("______________________________________")
    print(text)
    print("______________________________________")
    print("")


def create_agent_graph(agents) -> nx.Graph:

    projection = nx.Graph()

    for agent in agents:
        if not projection.has_node(agent.id):
            projection.add_node(agent.id)

        for agent_v in agent.neighbors():
            if not projection.has_edge(agent.id, agent_v.id):
                projection.add_edge(agent.id, agent_v.id, weight=agent.contact_weight(agent_v))

    return projection


def create_contact_matrix(agents, attr: str = "id", weighted=False, plot=False):

    contact_data = []
    attr_values = []
    pairs = []

    attr_u_name = f"{attr}_u"
    attr_v_name = f"{attr}_v"
    for agent_u in agents:

        for agent_v in agent_u.neighbors():
            attr_u = getattr(agent_u, attr)
            attr_v = getattr(agent_v, attr)

            attr_values.append(attr_u)
            attr_values.append(attr_v)

            pair = {agent_u.id, agent_v.id}

            if pair not in pairs:
                contact_data.append(
                    {
                        "id_u": agent_u.id,
                        attr_u_name: attr_u,
                        "id_v": agent_v.id,
                        attr_v_name: attr_v,
                        "weight": agent_u.contact_weight(agent_v),
                    },
                )
                pairs.append(pair)

    attr_values = list(set(attr_values))
    df = pd.DataFrame(index=sorted(attr_values, reverse=True), columns=sorted(attr_values))
    df = df.fillna(0)

    for contact in contact_data:
        weight = contact["weight"] if weighted else 1
        df.loc[contact[attr_u_name], contact[attr_v_name]] = (
            df.loc[contact[attr_u_name], contact[attr_v_name]] + weight
        )
        df.loc[contact[attr_v_name], contact[attr_u_name]] = (
            df.loc[contact[attr_v_name], contact[attr_u_name]] + weight
        )

    df = df / len(agents)

    if plot:
        sns.heatmap(df)

    return df


def group_it(value, start, step, n_steps, return_value="index", summarize_highest=False):

    assert type(value) in [int, float], f"{value} has to be a number!"
    assert value >= start, f"The value {value} is smaller than the smallest lower bound {start}."

    for i in range(n_steps):
        lower_bound = start + step * i
        upper_bound = lower_bound + step

        if lower_bound <= value:
            if return_value == "index":
                new_value = i

            elif return_value == "lower_bound":
                new_value = lower_bound

            elif return_value == "range":
                new_value = (lower_bound, upper_bound)

        if not summarize_highest:
            if i == n_steps + 1:
                if value > upper_bound:
                    new_value = np.nan

    return new_value
