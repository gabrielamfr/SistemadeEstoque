import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from package.produto import Produto

def test_produto_creation():
    print("=== Teste: Criação de Produto ===")
    
    produto = Produto(
        id=1,
        nome="Notebook Dell",
        descricao="Notebook i5 8GB RAM",
        preco=2500.00,
        estoque_atual=10,
        estoque_minimo=2,
        categoria="Eletrônicos"
    )
    
    assert produto.id == 1
    assert produto.nome == "Notebook Dell"
    assert produto.preco == 2500.00
    assert produto.estoque_atual == 10
    assert produto.ativo == True
    
    print(" Produto criado com sucesso!")
    print(f"   {produto}")

def test_produto_estoque_operations():
    print("\n=== Teste: Operações de Estoque ===")
    
    produto = Produto(2, "Mouse", "Mouse USB", 50.00, 20, 5)
    
    resultado = produto.atualizar_estoque(10)
    assert resultado == True
    assert produto.estoque_atual == 30
    print(" Entrada no estoque funcionando")
    
    resultado = produto.atualizar_estoque(-8)
    assert resultado == True
    assert produto.estoque_atual == 22
    print(" Saída do estoque funcionando")
    
    resultado = produto.atualizar_estoque(-30)
    assert resultado == False
    assert produto.estoque_atual == 22
    print(" Controle de estoque insuficiente funcionando")

def test_produto_estoque_baixo():
    print("\n=== Teste: Verificação de Estoque Baixo ===")
    
    produto_normal = Produto(3, "Teclado", "Teclado Mecânico", 200.00, 10, 3)
    assert produto_normal.verificar_estoque_baixo() == False
    print(" Estoque normal detectado")
    
    produto_baixo = Produto(4, "Monitor", "Monitor 24\"", 800.00, 2, 3)
    assert produto_baixo.verificar_estoque_baixo() == True
    print(" Estoque baixo detectado")

def test_produto_dict_conversion():
    print("\n=== Teste: Conversão Dict/Objeto ===")
    
    produto_original = Produto(5, "Webcam", "Webcam 1080p", 150.00, 15, 4)
    dados = produto_original.to_dict()
    assert isinstance(dados, dict)
    assert dados['nome'] == "Webcam"
    assert dados['preco'] == 150.00
    print(" Conversão para dicionário funcionando")
    
    produto_recriado = Produto.from_dict(dados)
    assert produto_recriado.nome == produto_original.nome
    assert produto_recriado.preco == produto_original.preco
    print(" Conversão de dicionário para objeto funcionando")

if __name__ == "__main__":
    print("== INICIANDO TESTES DO PRODUTO ==\n")
    
    test_produto_creation()
    test_produto_estoque_operations()
    test_produto_estoque_baixo()
    test_produto_dict_conversion()
    
    print("\n*** TODOS OS TESTES DO PRODUTO PASSARAM! ***")
def main():
    print("== INICIANDO TESTES DO PRODUTO ==\n")
    test_produto_creation()
    test_produto_estoque_operations()
    test_produto_estoque_baixo()
    test_produto_dict_conversion()
    print("\n** TODOS OS TESTES DO PRODUTO PASSARAM! **")

if __name__ == "__main__":
    main()