# LangGraph + CopilotKit Practice

Practice projects building AI agents with [LangGraph](https://github.com/langchain-ai/langgraph) and agent UIs with [CopilotKit](https://github.com/CopilotKit/CopilotKit).

| Folder | What it is |
|---|---|
| `CopilotKit/` | CopilotKit apps: todo apps, HR assistant, research canvas example |
| `CopilotKit + Langgraph/` | LangGraph backend wired to a CopilotKit frontend |
| `Langgraph/`, `langgraph2/`, `langgraph3/`, `langgraph4/` | LangGraph agents with backend + frontend (incl. resume screener) |
| `langgraph-todo-1/`, `langgraph-todo-2/`, `langgraph-todo-3/`, `langgraph_todo/` | LangGraph todo agents |
| `api + langgraph/` | FastAPI + LangGraph agent |

## Setup

Each project runs on its own. Secrets are not committed: create a `.env` in the project folder, for example:

```
GROQ_API_KEY=your_groq_key
NEXT_PUBLIC_COPILOT_CLOUD_PUBLIC_API_KEY=your_copilot_cloud_public_key
```

- Python: `python -m venv venv && pip install -r requirements.txt`
- Node: `npm install && npm run dev`
