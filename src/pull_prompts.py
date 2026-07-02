"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt público `leonanluppi/bug_to_user_story_v1`
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "bug_to_user_story_v1.yml"


def serialize_prompt(prompt_obj: object) -> dict:
    """Serializa o prompt puxado em um dicionário JSON-safe."""
    try:
        prompt_json = prompt_obj.to_json()
        return json.loads(prompt_json)
    except AttributeError:
        return {"prompt_repr": repr(prompt_obj)}
    except Exception as exc:
        print(f"Falha ao serializar prompt: {exc}")
        return {"prompt_repr": repr(prompt_obj)}


def pull_prompts_from_langsmith() -> bool:
    """Puxa o prompt público do LangSmith e salva em YAML local."""
    print_section_header("PULL DO LANGSMITH PROMPT HUB")
    print(f"Prompt público: {PROMPT_NAME}")

    try:
        prompt_obj = hub.pull(PROMPT_NAME)
        prompt_data = serialize_prompt(prompt_obj)

        save_success = save_yaml(prompt_data, str(OUTPUT_PATH))
        if save_success:
            print(f"Prompt salvo em: {OUTPUT_PATH}")
            return True
        else:
            print(f"Não foi possível salvar o prompt em: {OUTPUT_PATH}")
            return False

    except Exception as exc:
        print(f"Erro ao puxar prompt do LangSmith: {exc}")
        return False


def main() -> int:
    """Função principal do script."""
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    if pull_prompts_from_langsmith():
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
