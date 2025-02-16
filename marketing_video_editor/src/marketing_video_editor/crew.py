from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.videojungle_edit_tool import VideoJungleEditTool
from .tools.videojungle_download import VideoJungleDownloadTool
from .tools.videojungle_search_tool import VideoJungleSearchTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MarketingVideoEditor():
	"""MarketingVideoEditor crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def video_editor(self) -> Agent:
		return Agent(
			config=self.agents_config['video_editor'],
			tools=[VideoJungleEditTool],
			verbose=True
		)

	@agent
	def video_sourcing_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['video_sourcing_agent'],
			tools=[VideoJungleSearchTool, VideoJungleDownloadTool],
			verbose=True
		)
	
	@agent
	def scriptwriter(self) -> Agent:
		return Agent(
			config=self.agents_config['scriptwriter'],
			tools=[], 
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task 
	def scriptwriting_task(self) -> Task:
		return Task(
			config=self.tasks_config['scriptwriting_task'],
			output_file='script.json'
		)
	
	@task
	def script_to_scene(self) -> Task:
		return Task(
			config=self.tasks_config['script_to_scene'],
			output_file='scene.json'
		)

	@task
	def sourcing_task(self) -> Task:
		return Task(
			config=self.tasks_config['sourcing_task'],
			output_file='edit.json'
		)


	@task
	def video_editor_task(self) -> Task:
		return Task(
			config=self.tasks_config['video_editor_task'],
			output_file='video.mp4'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MarketingVideoEditor crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
