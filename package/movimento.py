from datetime import datetime
from enum import Enum

class TipoMovimento(Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"

class MovimentoEstoque:
    def __init__(self, id: int, produto_id: int, tipo: TipoMovimento, 
                 quantidade: int, data: datetime = None, observacao: str = ""):
        self.id = id
        self.produto_id = produto_id
        self.tipo = tipo
        self.quantidade = quantidade
        self.data = data if data else datetime.now()
        self.observacao = observacao
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'tipo': self.tipo.value,
            'quantidade': self.quantidade,
            'data': self.data.isoformat(),
            'observacao': self.observacao
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            produto_id=data['produto_id'],
            tipo=TipoMovimento(data['tipo']),
            quantidade=data['quantidade'],
            data=datetime.fromisoformat(data['data']),
            observacao=data.get('observacao', '')
        )
    
    def __str__(self):
        return f"Movimento {self.id}: {self.tipo.value} {self.quantidade} unidades do produto {self.produto_id}"
