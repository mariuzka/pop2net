import popy
import popy.utils as utils
from tabulate import tabulate
import pandas as pd

########## Function 1: Print Tabellen pro Location   ############

"""
Parameter
- locations =>  Liste aller location Instanzen des Netzwerkes (streng genommen reicht auch Liste von allen die man sich anschauen will)
- select_locations => einzelner Konstruktor oder Liste von Klassen Konstruktoren
- agent_attributes => Liste oder einzelnenes Attribute der Agenten, die in der Output-Tabelle erscheinen sollen

Output: Pro Location Instance der ausgewählten Location Klassen werden 
        Pandas Dataframes (Columns gefiltert durch agent_attributes) 
        mit Hilfe von tabulate als Konsolen print ausgegeben

"""


def location_information(locations,
                         select_locations: type[popy.Location] = None,
                         agent_attributes:str = None):
    # TODO Case einfügen, dass man nur locations angibt und dann alle
    # stats für alle locations sieht? 


    #locations = tuple(locations)

    # Unifiy parameter types
    if select_locations:
        if not isinstance(select_locations, list):
            # TESTING HOW TO MAKE LIST FROM CONSTRUCTOR
            select_locations = [select_locations]
    #else:
        #print("Error: Select at least one location for stats overview")
        #return
    if agent_attributes:
        if not isinstance(agent_attributes, list):
            agent_attributes = [agent_attributes]

    # determine eligible locations classes
    valid_locations = []
    if select_locations:
        for location_instance in locations:
            #str_location_instance = str(location_instance).split(" ")[0]
            for locationtype in select_locations:
                if isinstance(location_instance, locationtype):
                    valid_locations.append(location_instance)
    else:
        valid_locations = [location_instance for location_instance in locations]
        

    # create agent df per location instance
    agent_dfs = {}
    if agent_attributes:

        for i, location_instance in enumerate(valid_locations):

            # Create the title of printout
            title = f'{i+1}.Location: {str(location_instance).split(" ")[0]}'
            
            # get all agents per location instance, subset df by agent-attributes
            df = utils.get_df_agents(agents = location_instance.agents)
            df = df[[c for c  in agent_attributes]]
            agent_dfs[title] = df
    else:

        for i, location_instance in enumerate(valid_locations):
            title = f'{i+1}.Location: {str(location_instance).split(" ")[0]}'
            df = utils.get_df_agents(agents = location_instance.agents)
            df.drop(df.iloc[:,0:7], axis = 1, inplace = True)
            agent_dfs[title] = df

    #### Print Part "Basic"
    for  title, df in agent_dfs.items():
        print(f'{title} \n')
        print(tabulate(df, headers="keys", tablefmt="fancy_grid")) 
        print("\n")  


def location_crosstab(locations,
                      select_locations,
                      agent_attributes:str
                      ):
    # Make every Parameter a list 
    if select_locations:
        if not isinstance(select_locations, list):
            select_locations = [select_locations]

    if agent_attributes:
        if not isinstance(agent_attributes, list):
            agent_attributes = [agent_attributes]

    # determine eligible locations classes
    valid_locations = []
    if select_locations:
        for location_instance in locations:
            
            for locationtype in select_locations:
                if isinstance(location_instance, locationtype):
                    valid_locations.append(location_instance)
    else:
        valid_locations = [location_instance for location_instance in locations]
        

    # create agent df per location instance
    agent_dfs = {}
    if agent_attributes:

        for i, location_instance in enumerate(valid_locations):

            title = f'{i+1}.Location: {str(location_instance).split(" ")[0]}'
            df = utils.get_df_agents(agents=location_instance.agents)
            df = df[[c for c  in agent_attributes]]
            agent_dfs[title] = df
    
    
    
    for title, df in agent_dfs.items():
        
        for agent_attribute in agent_attributes:

            crosstab_table = pd.crosstab(index= df[agent_attribute],
                                   columns="count",)
            
            print(f"{title}")
            print(tabulate(crosstab_table,
                           headers=[agent_attribute, "count"],
                           tablefmt="fancy_grid"))
            print(f"\n")