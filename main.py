"""
SISTEMA DE CONTROLE DE ESTOQUE
Arquivo Principal - Main
"""
from package.sistema import SistemaEstoque
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n" + "="*50)
    print("          SISTEMA DE CONTROLE DE ESTOQUE")
    print("="*50)
    print("1. Cadastrar Produto")
    print("2. Listar Produtos")
    print("3. Registrar Entrada no Estoque")
    print("4. Registrar Venda")
    print("5. Gerar Relatório de Estoque Baixo")
    print("6. Executar Testes Automáticos")
    print("0. Sair")
    print("="*50)

def cadastrar_produto(sistema):
    print("\n--- CADASTRAR PRODUTO ---")
    
    nome = input("Nome do produto: ")
    descricao = input("Descrição: ")
    
    try:
        preco = float(input("Preço: R$ "))
        estoque_inicial = int(input("Estoque inicial: "))
        estoque_minimo = int(input("Estoque mínimo: "))
        categoria = input("Categoria: ") or "Geral"
        
        sucesso = sistema.cadastrar_produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque_inicial=estoque_inicial,
            estoque_minimo=estoque_minimo,
            categoria=categoria
        )
        
        if sucesso:
            print(f" Produto '{nome}' cadastrado com sucesso!")
        else:
            print(" Erro ao cadastrar produto!")
            
    except ValueError:
        print(" Erro: Digite valores numéricos válidos!")

def listar_produtos(sistema):
    print("\n--- LISTA DE PRODUTOS ---")
    
    produtos = sistema.listar_produtos()
    
    if not produtos:
        print(" Nenhum produto cadastrado.")
        return
    
    for produto in produtos:
        status = " BAIXO" if produto.verificar_estoque_baixo() else " NORMAL"
        print(f"ID: {produto.id} | {produto.nome} | R$ {produto.preco:.2f}")
        print(f"   Estoque: {produto.estoque_atual} | Mínimo: {produto.estoque_minimo} | Status: {status}")
        print(f"   Descrição: {produto.descricao}")
        print("-" * 40)

def registrar_entrada(sistema):
    print("\n--- REGISTRAR ENTRADA NO ESTOQUE ---")
    
    listar_produtos(sistema)
    
    try:
        produto_id = int(input("\nID do produto: "))
        quantidade = int(input("Quantidade: "))
        observacao = input("Observação: ") or "Entrada no estoque"
        
        sucesso = sistema.registrar_entrada(produto_id, quantidade, observacao)
        
        if sucesso:
            print(f" Entrada de {quantidade} unidades registrada com sucesso!")
        else:
            print(" Erro: Produto não encontrado ou quantidade inválida!")
            
    except ValueError:
        print(" Erro: Digite valores numéricos válidos!")

def registrar_venda(sistema):
    print("\n--- REGISTRAR VENDA ---")
    
    listar_produtos(sistema)
    
    try:
        produto_id = int(input("\nID do produto: "))
        quantidade = int(input("Quantidade vendida: "))
        
        sucesso = sistema.registrar_venda(produto_id, quantidade)
        
        if sucesso:
            print(f" Venda de {quantidade} unidades registrada com sucesso!")
        else:
            print(" Erro: Produto não encontrado ou estoque insuficiente!")
            
    except ValueError:
        print(" Erro: Digite valores numéricos válidos!")

def gerar_relatorio_estoque_baixo(sistema):
    print("\n--- RELATÓRIO DE ESTOQUE BAIXO ---")
    
    produtos_baixo = sistema.gerar_relatorio_estoque_baixo()
    
    if not produtos_baixo:
        print(" Todos os produtos com estoque normal!")
        return
    
    print(f"  {len(produtos_baixo)} produto(s) com estoque baixo:\n")
    
    for produto in produtos_baixo:
        print(f" {produto.nome}")
        print(f"   Estoque atual: {produto.estoque_atual}")
        print(f"   Estoque mínimo: {produto.estoque_minimo}")
        print(f"   Déficit: {produto.estoque_minimo - produto.estoque_atual} unidades")
        print("-" * 30)

def executar_testes_automaticos():
    print("\n--- EXECUTANDO TESTES AUTOMÁTICOS ---")
    
    try:
        print(" Executando testes de Produto")
        import subprocess
        import sys

        result= subprocess.run([sys.executable, "tests/testbanch_produto.py"], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Erros:", result.stderr)

        print("\n Executando testes de Movimento..." )
        result = subprocess.run([sys.executable, "tests/testbanch_movimento.py"],capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Erros:",result.stderr)

        print ("\n Executando testes de Sistema...")
        result = subprocess.run([sys.executable, "tests/testbanch_sistema.py"],capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Erros:", result.stderr)

        print("\n TODOS OS TESTES FORAM EXECUTADOS!")
        
    except Exception as e:
        print(f"Erro ao executar testes:{e}")
       
def main():
    sistema = SistemaEstoque()
    
    print(" Inicializando Sistema de Estoque...")
    print(f" Produtos carregados: {len(sistema.produtos)}")
    print(f" Movimentos carregados: {len(sistema.movimentos)}")
    
    input("\nPressione Enter para continuar...")
    
    while True:
        limpar_tela()
        mostrar_menu()
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            cadastrar_produto(sistema)
        elif opcao == "2":
            listar_produtos(sistema)
        elif opcao == "3":
            registrar_entrada(sistema)
        elif opcao == "4":
            registrar_venda(sistema)
        elif opcao == "5":
            gerar_relatorio_estoque_baixo(sistema)
        elif opcao == "6":
            executar_testes_automaticos()
        elif opcao == "0":
            print("\n Obrigado por usar o Sistema de Estoque!")
            break
        else:
            print(" Opção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()