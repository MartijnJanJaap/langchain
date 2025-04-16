import typer
from pathlib import Path
from main import run
import json
from config import AppConfig

app = typer.Typer()

@app.command()
def start():
    current_dir = Path.cwd()
    workspace = current_dir / "workspace"
    prompts = current_dir / "prompts"

    if not workspace.exists() or not prompts.exists():
        typer.echo("❌ Missing 'workspace/' or 'prompts/' directory.")
        raise typer.Exit(code=1)

    with open("OAI_CONFIG_LIST.json") as f:
        llm_config_file = json.load(f)

    config = AppConfig(
        workspace_path=workspace,
        prompts_dir=prompts,
        llm_model=llm_config_file[0]["model"],
        llm_api_key=llm_config_file[0]["api_key"],
        llm_base_url=llm_config_file[0].get("base_url")
    )

    typer.echo("🚀 Starting LangGraph assistant...")
    run(config)

if __name__ == "__main__":
    app()
