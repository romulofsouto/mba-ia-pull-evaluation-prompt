"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import re
import sys
from pathlib import Path
from typing import Any
import re
import yaml
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.loading import load_prompt
from langsmith import Client
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()

USERNAME_HANDLE_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    print_section_header("PUSH DO LANGSMITH PROMPT HUB")
    print(f"Prompt local: {PROMPT_FILE}")
    print(f"Prompt no Hub: {prompt_name}\n")

    valid, errors = validate_prompt(prompt_data)
    if not valid:
        print("❌ Validação do prompt falhou:")
        for error in errors:
            print(f"   - {error}")
        return False

    prompt_template = build_prompt_template(prompt_data)
    description = prompt_data.get("description", "Prompt otimizado para bug_to_user_story_v2")
    tags = [str(tag) for tag in prompt_data.get("tags", []) if tag]

    version = prompt_data.get("version")
    if version:
        normalized_version = str(version)
        if not normalized_version.startswith("v"):
            normalized_version = f"v{normalized_version}"
        if normalized_version not in tags:
            tags.insert(0, normalized_version)

    try:
        client = Client()
        url = client.push_prompt(
            prompt_name,
            object=prompt_template,
            tags=tags or None,
            description=description,
            is_public=True,
        )
        print(f"✅ Prompt enviado com sucesso: {url}")
        return True
    except Exception as exc:
        print(f"❌ Falha ao enviar prompt com Client.push_prompt: {exc}")
        return False



def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    errors: list[str] = []

    if not prompt_data.get("description"):
        errors.append("Campo obrigatório faltando: description")
    if not prompt_data.get("system_prompt"):
        errors.append("Campo obrigatório faltando: system_prompt")
    if not prompt_data.get("version"):
        errors.append("Campo obrigatório faltando: version")

    tags = prompt_data.get("tags", [])
    if not isinstance(tags, list):
        errors.append("Campo 'tags' deve ser uma lista")

    return (len(errors) == 0, errors)



def validate_username_handle(username: str) -> bool:
    return bool(USERNAME_HANDLE_REGEX.match(username))

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "bug_to_user_story_v2.yml"
DEFAULT_USER_PROMPT = "{bug_report}"


def normalize_prompt_data(prompt_data: dict) -> dict:
    if isinstance(prompt_data, dict) and len(prompt_data) == 1:
        first_value = next(iter(prompt_data.values()))
        if isinstance(first_value, dict):
            return first_value
    return prompt_data


def parse_prompt_file_fallback(file_path: Path) -> dict:
    raw_text = file_path.read_text(encoding="utf-8")
    prompt_data: dict[str, Any] = {}

    description_match = re.search(r'^description:\s*"([^"]*)"', raw_text, flags=re.M)
    if description_match:
        prompt_data["description"] = description_match.group(1).strip()

    version_match = re.search(r'^\s{2}version:\s*"([^"]*)"', raw_text, flags=re.M)
    if version_match:
        prompt_data["version"] = version_match.group(1).strip()

    tags_match = re.search(r'^\s{2}tags:\s*(\[.*?\])', raw_text, flags=re.M | re.S)
    if tags_match:
        try:
            prompt_data["tags"] = load_yaml_text(tags_match.group(1)) or []
        except Exception:
            prompt_data["tags"] = []

    user_prompt_match = re.search(r'^\s{2}user_prompt:\s*"([^"]*)"', raw_text, flags=re.M)
    if user_prompt_match:
        prompt_data["user_prompt"] = user_prompt_match.group(1).strip()

    system_prompt_match = re.search(
        r"^system_prompt:\s*\|\n(.*?)(?=^\s{2}(?:user_prompt|version|created_at|tags):|\Z)",
        raw_text,
        flags=re.M | re.S,
    )
    if system_prompt_match:
        prompt_data["system_prompt"] = system_prompt_match.group(1).rstrip("\n")

    return prompt_data


def load_yaml_text(text: str) -> Any:
    return yaml.safe_load(text)


def load_prompt_data(file_path: Path) -> dict:
    prompt_data = load_yaml(str(file_path))
    if prompt_data is not None:
        return normalize_prompt_data(prompt_data)
    return normalize_prompt_data(parse_prompt_file_fallback(file_path))


def build_prompt_template(prompt_data: dict) -> ChatPromptTemplate:
    if isinstance(prompt_data, ChatPromptTemplate):
        return prompt_data

    system_prompt = prompt_data.get("system_prompt")
    if not system_prompt:
        raise ValueError("O prompt não contém 'system_prompt' válido.")

    user_prompt = prompt_data.get("user_prompt", DEFAULT_USER_PROMPT)
    return ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )


def load_prompt_template(prompt_path: Path) -> ChatPromptTemplate:
    try:
        return load_prompt(str(prompt_path))
    except Exception:
        prompt_data = load_prompt_data(prompt_path)
        return build_prompt_template(prompt_data)



def main() -> int:
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    if not username:
        print("❌ USERNAME_LANGSMITH_HUB não configurada no .env")
        return 1

    if not validate_username_handle(username):
        print("❌ USERNAME_LANGSMITH_HUB inválida: use apenas letras, números, '_' ou '-' sem espaços.")
        print("   Exemplo correto: USERNAME_LANGSMITH_HUB=seu_handle")
        return 1

    prompt_name = f"{username}/bug_to_user_story_v2"
    prompt_data = load_prompt_data(PROMPT_FILE)

    if not prompt_data:
        print(f"❌ Não foi possível carregar os dados do prompt em: {PROMPT_FILE}")
        return 1

    if push_prompt_to_langsmith(prompt_name, prompt_data):
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
