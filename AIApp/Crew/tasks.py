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
	)

def get_components_task(tasks_config: dict, get_components_agent) -> Task:
	return Task(
		config=tasks_config['get_components_task'],
		agent=get_components_agent,
		tools=[get_existing_components]
	)


def create_component_task(tasks_config: dict, create_component_agent) -> Task:
	return Task(
		config=tasks_config['create_component_task'],
		agent=create_component_agent,
		tools=[create_new_component]
	)


# New specialized template tasks

def combiner_task(tasks_config: dict, combiner_agent) -> Task:
	return Task(
		config=tasks_config['combiner_task'],
		agent=combiner_agent,
		tools=[combine_components,save_final_html, copy_html_file]
	) 

