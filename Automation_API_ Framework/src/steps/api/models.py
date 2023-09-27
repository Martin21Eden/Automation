from dataclasses import dataclass
from typing import Any


@dataclass
class Meta:
    path: str
    response_schema: Any = None

    def build_path(self, item):
        return self.path + f'/{item}/'
