from langchain.agents import AgentType, initialize_agent
from langchain.llms import Ollama
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.utilities.github import GitHubAPIWrapper
from dotenv import load_dotenv

load_dotenv()

llm = Ollama(
    model="llama2:13b",
)

github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)
tools = toolkit.get_tools()

agent_executor = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent_executor.run("Tell me about marumemomo/MushockAGI github repo")
