import os
from typing import Any
import autogen
import agentops
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, config_list_from_json, register_function
import autogen.runtime_logging
import sqlite3

# Start tracing
agentops.init(api_key=os.environ.get("AGENTOPS_API_KEY"), tags=["simple-autogen-example"])

# Init database connection
connection = sqlite3.connect("demo.db")

# Seeding
# cursor = connection.cursor()
# cursor.execute("DROP TABLE IF EXISTS cars")
# cursor.execute("DROP TABLE IF EXISTS orders")
# cursor.execute("DROP TABLE IF EXISTS users")
# cursor.execute("CREATE TABLE cars (id INTEGER PRIMARY KEY, make TEXT, model TEXT)")
# cursor.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, car_id INTEGER)")
# cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, country_code TEXT)")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Linda', 30, 'US')")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Peter', 25, 'US')")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Alice', 27, 'US')")
# cursor.execute("INSERT INTO users (name, age, country_code) VALUES ('Robin-Manuel', 33, 'DE')")
# connection.commit()


def get_tables() -> list[str]:
  """
  Returns the list of tables in the database.

  Returns:
    list[str]: The list of tables in the database.
  """

  cursor = connection.cursor()
  result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
  return result.fetchall()

def run_query(sql: str) -> list[Any]:
  """
  Executes the given SQL query and returns a list of results.

  Args:
    sql (str): The SQL query to be executed.

  Returns:
    list[dict]: A list of results.
  """
  print(f"Running query: {sql}")
  cursor = connection.cursor()
  result = cursor.execute(sql)
  return result.fetchall()

# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple questions about the dataset. "
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the functions to the two agents.
register_function(
    get_tables,
    caller=assistant,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="get_tables",  # Executes the given SQL query and returns a list of results.
    description="Returns the list of tables in the database.",  # A description of the tool.
)

register_function(
    run_query,
    caller=assistant,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="run_query",  # Executes the given SQL query and returns a list of results.
    description="Executes the given SQL query and returns a list of results.",  # A description of the tool.
)

# chat_result = user_proxy.initiate_chat(assistant, message="How many users exist in our dataset?")
chat_result = user_proxy.initiate_chat(assistant, message="How many users are from Germany?")
print(chat_result)

# Stop tracing
agentops.end_session("Success")
