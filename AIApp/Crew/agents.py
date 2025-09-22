from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create a LangSmith-instrumented LLM (uses .env vars automatically)
def get_llm():
    return ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )

def create_manager_agent(agents_config: dict) -> Agent:
    return Agent(
        config=agents_config['manager_agent'],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        human_in_the_loop=False,
    )

def uiux_team_leader_agent(agents_config: dict) -> Agent:
    return Agent(
        config=agents_config['uiux_team_leader_agent'],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
        human_in_the_loop=False,
    )

# def combiner_agent(agents_config: dict) -> Agent:
# 	return Agent(
# 		config=agents_config['combiner_agent'],
# 		llm=LLM(model="gpt-4o", temperature=0),
# 		verbose=True,
# 		allow_delegation=False,
# 		human_in_the_loop=False,
# 	)


# def aggregator_agent(agents_config: dict) -> Agent:
# 	return Agent(
# 		config=agents_config['aggregator_agent'],
# 		llm=LLM(model="gpt-4o", temperature=0),
# 		verbose=True,
# 		allow_delegation=False,
# 		human_in_the_loop=False,
# 	)