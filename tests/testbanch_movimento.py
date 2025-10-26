import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from package.movimento import MovimentoEstoque, TipoMovimento

def test_movimento_creation():
    print("=== Teste: Criação de Movimentos ===")
    movimento_entrada = MovimentoEstoque(
        id=1,
        produto_id=1,
        tipo=TipoMovimento.ENTRADA,
        quantidade=50,
        observacao="Compra do fornecedor"
    )
    
    assert movimento_entrada.tipo == TipoMovimento.ENTRADA
    assert movimento_entrada.quantidade == 50
    assert movimento_entrada.produto_id == 1
    print(" Movimento de entrada criado com sucesso")
    
    movimento_saida = MovimentoEstoque(
        id=2,
        produto_id=1,
        tipo=TipoMovimento.SAIDA,
        quantidade=10,
        observacao="Venda para cliente"
    )
    
    assert movimento_saida.tipo == TipoMovimento.SAIDA
    assert movimento_saida.quantidade == 10
    print(" Movimento de saída criado com sucesso")

def test_movimento_dict_conversion():
    print("\n=== Teste: Conversão Dict/Objeto ===")
    
    movimento_original = MovimentoEstoque(
        id=3,
        produto_id=2,
        tipo=TipoMovimento.ENTRADA,
        quantidade=25,
        observacao="Teste de conversão"
    )
    
    dados = movimento_original.to_dict()
    assert isinstance(dados, dict)
    assert dados['tipo'] == "entrada"
    assert dados['quantidade'] == 25
    print(" Conversão para dicionário funcionando")
    
    movimento_recriado = MovimentoEstoque.from_dict(dados)
    assert movimento_recriado.tipo == movimento_original.tipo
    assert movimento_recriado.quantidade == movimento_original.quantidade
    print(" Conversão de dicionário para objeto funcionando")

if __name__ == "__main__":
    print("== INICIANDO TESTES DE MOVIMENTOS ==\n")
    
    test_movimento_creation()
    test_movimento_dict_conversion()
    
    print("\n** TODOS OS TESTES DE MOVIMENTOS PASSARAM! **")

def main():
    print("== INICIANDO TESTES DE MOVIMENTOS ==\n")
    
    test_movimento_creation()
    test_movimento_dict_conversion()
    
    print("\n** TODOS OS TESTES DE MOVIMENTOS PASSARAM! **")

if __name__ == "__main__":
    main()