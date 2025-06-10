import json
from typing import Any, Dict

class JsonPersistence:
    """
    Gerencia leitura e escrita de dados em JSON.
    """

    @staticmethod
    def save(filename: str, data: Dict[str, Any]) -> None:
        """
        Salva o dicionário `data` em um arquivo JSON.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(filename: str) -> Dict[str, Any]:
        """
        Carrega e retorna o conteúdo de um arquivo JSON.
        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
