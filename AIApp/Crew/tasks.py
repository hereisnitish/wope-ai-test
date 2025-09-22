from crewai import Task
from .tools import *

def create_manager_task(tasks_config: dict, manager_agent) -> Task:
	return Task(
		config=tasks_config['manager_task'],
		agent=manager_agent
	)


def uiux_team_leader_task(tasks_config: dict, uiux_team_leader_agent) -> Task:
	return Task(
		config=tasks_config['uiux_team_leader_task'],
		agent=uiux_team_leader_agent,
		tools=[get_existing_components, save_html_to_database_with_embeddings]
	)


# # New specialized template tasks

# def combiner_task(tasks_config: dict, combiner_agent) -> Task:
# 	return Task(
# 		config=tasks_config['combiner_task'],
# 		agent=combiner_agent,
# 		tools=[combine_components]
# 	) 


# def aggregator_task(tasks_config: dict, aggregator_agent) -> Task:
# 	return Task(
# 		config=tasks_config['aggregator_task'],
# 		agent=aggregator_agent,
# 		tools=[save_final_html, copy_html_file]
# 	)