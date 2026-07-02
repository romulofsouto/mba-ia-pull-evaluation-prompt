"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

ROOT_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT_DIR / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt_data = load_prompts(str(PROMPT_PATH))
        prompt = prompt_data["bug_to_user_story_v2"]
        system_prompt = prompt.get("system_prompt", "")

        assert isinstance(system_prompt, str)
        assert system_prompt.strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt_data = load_prompts(str(PROMPT_PATH))
        prompt = prompt_data["bug_to_user_story_v2"]
        system_prompt = prompt.get("system_prompt", "").lower()

        assert any(
            phrase in system_prompt
            for phrase in ["você é", "persona", "product manager"]
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt_data = load_prompts(str(PROMPT_PATH))
        prompt = prompt_data["bug_to_user_story_v2"]
        system_prompt = prompt.get("system_prompt", "").lower()

        assert any(
            phrase in system_prompt
            for phrase in ["markdown", "user story", "formato obrigatório", "template"]
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt_data = load_prompts(str(PROMPT_PATH))
        prompt = prompt_data["bug_to_user_story_v2"]
        system_prompt = prompt.get("system_prompt", "").lower()

        assert "exemplo" in system_prompt
        assert "bug_report:" in system_prompt

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt_data = load_prompts(str(PROMPT_PATH))
        prompt = prompt_data["bug_to_user_story_v2"]
        system_prompt = prompt.get("system_prompt", "")

        assert "[TODO]" not in system_prompt

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt_data = load_prompts(str(PROMPT_PATH))
        prompt = prompt_data["bug_to_user_story_v2"]
        techniques = prompt.get("tecnicas", [])

        assert isinstance(techniques, list)
        assert len(techniques) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])