# AutoGen Experiments

## Prerequisites

Make sure, you are in the `autogen` folder.

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate the virtual environment

```bash
source .venv/bin/activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Populate the environment variables

```bash
export OPENAI_API_KEY="..."
export AGENTOPS_API_KEY="..." # optional
export AGENTOPS_API_KEY="..." # optional
```

## Experiment: Interacting with a Database via SQL

Give the agents the `run_query(sql: str)` function as a potential tool to call, and ask questions about the database, that require filtering via SQL queries.

```bash
python sql.py
```

What we should see:

1. The agents calls the `get_tables` function to get a list of tables.
2. The agent calls the `run_query` function with a SQL query like `SELECT COUNT(*) FROM users WHERE country = 'Germany'`.
3. The agent receives an error message `no such column: country`, because the `users` table does not have a `country` column.
4. The agent calls the `run_query` function with a SQL query like `PRAGMA table_info(users)`, to receive the actual column names of the `users` table.
5. The agent realized, that the `country_code` column probably contains the country codes, and not the full country names.
6. The agent calls the `run_query` function again with a SQL query like `SELECT COUNT(*) FROM users WHERE country_code = 'DE'`, and receives the correct result (1).
7. The agent responds with the correct answer in text like `There is 1 user from Germany in the dataset.`.
