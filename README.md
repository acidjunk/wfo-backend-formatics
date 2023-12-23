# Example Workflow Orchestrator

Example workflow orchestrator
(https://workfloworchestrator.org/orchestrator-core/) implementation.

**Note: work in progress; first version expected to be released in February 2024**

## Quickinstall

Create a venv, then run these commands:

```
pip install -r requirements.txt
python main.py db upgrade heads
python -u -m uvicorn --reload --workers 4 --host 0.0.0.0 --port 8080 main:app
```

This assumes an environment that has correct settings with a fallback on the orchestrator-core 
default settings (e.g. DB name orchestrator-core, when you don't configure it).

An example can be found in `.env.example`

You can find a list with default settings [here](https://github.com/workfloworchestrator/orchestrator-core/blob/main/orchestrator/settings.py)
