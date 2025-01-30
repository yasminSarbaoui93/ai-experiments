import os
import autogen
# import agentops
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, config_list_from_json
import autogen.runtime_logging

# Start logging with logger_type and the filename to log to
logging_session_id = autogen.runtime_logging.start(logger_type="sqlite", config={"dbname": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

# agentops.init(api_key=os.environ.get("AGENTOPS_API_KEY"), tags=["simple-autogen-example"])
# agentops.start_session(tags=["autogen-tool-example"])

cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # Never ask for human input.
)

joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]}, # Use OpenAI's GPT-4 model
    #llm_config={"config_list": [{"model": "phi3", "temperature": 0.7, "base_url": "http://127.0.0.1:11434/v1"}]}, # Use a local ollama model
    human_input_mode="NEVER",  # Never ask for human input.
)

result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)

# agentops.end_session("Success")
autogen.runtime_logging.stop()
