# GraphRAG

Start a local Neo4j database with APOC plugin enabled.

```bash
docker run \
    -p 7474:7474 -p 7687:7687 \
    --name neo4j-apoc \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_PLUGINS=\[\"apoc\"\] \
    --env NEO4J_AUTH=neo4j/local_test_pw_123 \
    --volume=./neo4j-data:/data \
    neo4j:5.24.0
```

Run the llm-graph-builder project locally. For this, download the repository and create a `.env` file with the following content:

```
VITE_LLM_MODELS="diffbot,openai-gpt-3.5,openai-gpt-4o"
OPENAI_API_KEY="..."
```

Then run the following command.

```bash
docker compose up --build
```

The project will be available at `http://localhost:3000`.

Create a connection with the Neo4j database at `neo4j://host.docker.internal:7687` with the credentials `neo4j/local_test_pw_123`.

Upload the demo Wikipedia data from the `data` folder and create the graph.

Use the Chatbot to query the graph.
