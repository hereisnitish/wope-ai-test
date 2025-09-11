from crewai import Agent, LLM


def create_manager_agent(agents_config: dict) -> Agent:
	return Agent(
		config=agents_config['manager_agent'],
		llm=LLM(model="gpt-4o", temperature=0),
		verbose=True,
		allow_delegation=False,
		human_in_the_loop=False,
	)

def uiux_team_leader_agent(agents_config: dict) -> Agent:
	return Agent(
		config=agents_config['uiux_team_leader_agent'],
		llm=LLM(model="gpt-4o", temperature=0),
		verbose=True,
		allow_delegation=False,
		human_in_the_loop=False,
	)
 
def get_components_agent(agents_config: dict) -> Agent:
	return Agent(
		config=agents_config['get_components_agent'],
		llm=LLM(model="gpt-4o", temperature=0),
		verbose=True,
		allow_delegation=False,
		human_in_the_loop=False,
	)

def create_component_agent(agents_config: dict) -> Agent:
	return Agent(
		config=agents_config['create_component_agent'],
		llm=LLM(model="gpt-4o", temperature=0),
		verbose=True,
		allow_delegation=False,
		human_in_the_loop=False,
	)

def combiner_agent(agents_config: dict) -> Agent:
	return Agent(
		config=agents_config['combiner_agent'],
		llm=LLM(model="gpt-4o", temperature=0),
		verbose=True,
		allow_delegation=False,
		human_in_the_loop=False,
	)

