import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from package.sistema import SistemaEstoque

def test_sistema_cadastro_produto():
    print("=== Teste: Cadastro de Produto no Sistema ===")
    
    sistema = SistemaEstoque()
    
    sistema.produtos = []
    sistema.proximo_id_produto = 1
    resultado = sistema.cadastrar_produto(
        nome="Notebook Gamer",
        descricao="Notebook i7 16GB RAM",
        preco=3500.00,
        estoque_inicial=5,
        estoque_minimo=1,
        categoria="Eletrônicos"
    )
    
    assert resultado == True
    assert len(sistema.produtos) == 1
    assert sistema.produtos[0].nome == "Notebook Gamer"
    print(" Cadastro de produto funcionando")

def test_sistema_busca_produto():
    print("\n=== Teste: Busca de Produto ===")
    
    sistema = SistemaEstoque()
    produto = sistema.buscar_produto_por_id(1)
    assert produto is not None
    assert produto.nome == "Notebook Gamer"
    print(" Busca de produto existente funcionando")
    produto = sistema.buscar_produto_por_id(999)
    assert produto is None
    print(" Busca de produto inexistente funcionando")

def test_sistema_movimentos_estoque():
    print("\n=== Teste: Movimentos de Estoque ===")
    
    sistema = SistemaEstoque()
    
    resultado_entrada = sistema.registrar_entrada(1, 10, "Compra do fornecedor")
    assert resultado_entrada == True
    produto = sistema.buscar_produto_por_id(1)
    assert produto.estoque_atual == 15
    print(" Entrada no estoque funcionando")
    
    resultado_venda = sistema.registrar_venda(1, 3)
    assert resultado_venda == True
    produto = sistema.buscar_produto_por_id(1)
    assert produto.estoque_atual == 12
    print(" Venda (saída do estoque) funcionando")
    
    resultado_venda = sistema.registrar_venda(1, 50)
    assert resultado_venda == False
    produto = sistema.buscar_produto_por_id(1)
    assert produto.estoque_atual == 12 
    print(" Controle de venda com estoque insuficiente funcionando")

def test_sistema_relatorio_estoque_baixo():
    print("\n=== Teste: Relatório de Estoque Baixo ===")
    
    sistema = SistemaEstoque()
    sistema.cadastrar_produto(
        nome="Mouse Pad",
        descricao="Mouse Pad Grande",
        preco=25.00,
        estoque_inicial=2,
        estoque_minimo=5
    )
    
    relatorio = sistema.gerar_relatorio_estoque_baixo()
    assert len(relatorio) >= 1
    
    produtos_baixo = [p.nome for p in relatorio]
    assert "Mouse Pad" in produtos_baixo
    print(" Relatório de estoque baixo funcionando")

def test_sistema_persistencia_dados():
    print("\n=== Teste: Persistência de Dados ===")

    sistema2 = SistemaEstoque()
    
    assert len(sistema2.produtos) >= 2
    print(" Persistência de dados funcionando")

def main():
    print("== INICIANDO TESTES DO SISTEMA ==\n")
    
    test_sistema_cadastro_produto()
    test_sistema_busca_produto()
    test_sistema_movimentos_estoque()
    test_sistema_relatorio_estoque_baixo()
    test_sistema_persistencia_dados()
    
    print("\n** TODOS OS TESTES DO SISTEMA PASSARAM! **")

if __name__ == "__main__":
    main()