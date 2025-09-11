import os
import json
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .agents import create_manager_agent, uiux_team_leader_agent as create_uiux_team_leader_agent, combiner_agent as create_combiner_agent, aggregator_agent as create_aggregator_agent
from .tasks import create_manager_task, uiux_team_leader_task as create_uiux_team_leader_task, combiner_task as create_combiner_task, aggregator_task as create_aggregator_task



@CrewBase
class DjangoProjectGeneratorCrew():
	"""Django Project Generator crew"""

	@agent
	def manager_agent(self) -> Agent:
		return create_manager_agent(self.agents_config)

	@agent
	def uiux_team_leader_agent(self) -> Agent:
		return create_uiux_team_leader_agent(self.agents_config)


	@agent
	def combiner_agent(self) -> Agent:
		return create_combiner_agent(self.agents_config)

	@agent
	def aggregator_agent(self) -> Agent:
		return create_aggregator_agent(self.agents_config)

	@task
	def manager_task(self) -> Task:
		return create_manager_task(self.tasks_config, self.manager_agent())

	@task
	def uiux_team_leader_task(self) -> Task:
		return create_uiux_team_leader_task(self.tasks_config, self.uiux_team_leader_agent())

	@task
	def combiner_task(self) -> Task:
		return create_combiner_task(self.tasks_config, self.combiner_agent())

	@task
	def aggregator_task(self) -> Task:
		return create_aggregator_task(self.tasks_config, self.aggregator_agent())


	@crew
	def crew(self) -> Crew:
		return Crew(
			agents= [
				self.uiux_team_leader_agent(),
				self.aggregator_agent(),
				self.combiner_agent(),
    
			],  # Automatically collected by the @agent decorator
			tasks= [
				self.manager_task(),
				self.uiux_team_leader_task(),
				self.combiner_task(),
				self.aggregator_task(),
			],  # Automatically collected by the @task decorator
			verbose=True,
			process=Process.hierarchical,
			manager_agent=self.manager_agent(),
		)


# if __name__ == "__main__":
# 	initial_prompt = get_user_input(
# 		"What kind of Django project would you like to build? (e.g., 'Build me a website with login and dashboard')"
# 	)
# 	print(f"\n🎯 Starting project generation for: {initial_prompt}")
# 	print("🔗 First, the system will clone the base repository...")
# 	print("🤔 Then agents will ask questions to understand your requirements.")
# 	print("=" * 50)
# 	try:
# 		crewai_crew = DjangoProjectGeneratorCrew()
# 		crew_object = crewai_crew.crew()
# 		print("🔧 Crew created successfully, starting execution...")
# 		response = crew_object.kickoff(inputs=dict(user_prompt=initial_prompt))
# 		print("\n✅ Project planning completed!")
# 		print("=" * 50)
# 		os.makedirs("outputs", exist_ok=True)
# 		with open("outputs/response.json", "w") as f:
# 			json.dump(response.model_dump(), f, indent=2)
# 		with open("outputs/response.md", "w") as f:
# 			f.write(response.raw if hasattr(response, "raw") else str(response))
		
# 	except Exception as e:
# 		print(f"\n❌ Error occurred: {e}")
# 		import traceback
# 		traceback.print_exc()
# 		print("Please check your API key and try again.") 