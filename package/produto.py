import json
from typing import List

class Produto:
    def __init__(self, id: int, nome: str, descricao: str, preco: float, 
                 estoque_atual: int, estoque_minimo: int, categoria: str = "Geral"):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque_atual = estoque_atual
        self.estoque_minimo = estoque_minimo
        self.categoria = categoria
        self.ativo = True
    
    def atualizar_estoque(self, quantidade: int) -> bool:
        novo_estoque = self.estoque_atual + quantidade
        if novo_estoque >= 0:
            self.estoque_atual = novo_estoque
            return True
        return False
    
    def verificar_estoque_baixo(self) -> bool:
        return self.estoque_atual <= self.estoque_minimo
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque_atual': self.estoque_atual,
            'estoque_minimo': self.estoque_minimo,
            'categoria': self.categoria,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        produto = cls(
            id=int(data.get('id', 0)),
            nome=str(data.get('nome', 'Sem Nome')),
            descricao=str(data.get('descricao', '')),
            preco=float(data.get('preco', 0.0)),
            estoque_atual=int(data.get('estoque_atual', 0)),
            estoque_minimo=int(data.get('estoque_minimo', 0)),
            categoria=str(data.get('categoria', 'Geral'))
        )
        produto.ativo = bool(data.get('ativo', True))
        return produto
    
    def __str__(self):
        return f"Produto {self.id}: {self.nome} - R$ {self.preco:.2f} (Estoque: {self.estoque_atual})"
