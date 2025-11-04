import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from package.sistema import SistemaEstoque

def main():
    st.set_page_config(page_title="Sistema de Estoque", page_icon="====", layout="wide")
    
    if 'sistema' not in st.session_state:
        st.session_state.sistema = SistemaEstoque()
    
    st.title(" Sistema de Controle de Estoque")
    
    menu = st.sidebar.selectbox(
        "Menu Principal",
        ["Dashboard", "Cadastrar Produto", "Listar Produtos", "Registrar Entrada", 
         "Registrar Venda", "Relatórios", "Executar Testes"]
    )    
    if menu == "Dashboard":
        show_dashboard()
    elif menu == "Cadastrar Produto":
        cadastrar_produto()
    elif menu == "Listar Produtos":
        listar_produtos()
    elif menu == "Registrar Entrada":
        registrar_entrada()
    elif menu == "Registrar Venda":
        registrar_venda()
    elif menu == "Relatórios":
        gerar_relatorios()
    elif menu == "Executar Testes":
        executar_testes()

def show_dashboard():
    st.header("Dashboard")
    
    sistema = st.session_state.sistema
    total_produtos = len(sistema.produtos)
    produtos_baixo_estoque = len(sistema.gerar_relatorio_estoque_baixo())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Produtos", total_produtos)
    
    with col2:
        st.metric("Produtos com Estoque Baixo", produtos_baixo_estoque)
    
    with col3:
        st.metric("Movimentos Registrados", len(sistema.movimentos))
    
    if produtos_baixo_estoque > 0:
        st.warning(f" {produtos_baixo_estoque} produto(s) com estoque baixo!")
        produtos_baixo = sistema.gerar_relatorio_estoque_baixo()
        for produto in produtos_baixo:
            st.error(f"**{produto.nome}** - Estoque: {produto.estoque_atual} (Mínimo: {produto.estoque_minimo})")

def cadastrar_produto():
    st.header("Cadastrar Novo Produto")
    
    with st.form("cadastro_produto"):
        nome = st.text_input("Nome do Produto*")
        descricao = st.text_area("Descrição")
        preco = st.number_input("Preço*", min_value=0.0, step=0.01)
        estoque_inicial = st.number_input("Estoque Inicial*", min_value=0, step=1)
        estoque_minimo = st.number_input("Estoque Mínimo*", min_value=0, step=1)
        categoria = st.text_input("Categoria", value="Geral")
        
        submitted = st.form_submit_button("Cadastrar Produto")
        
        if submitted:
            if nome and preco > 0:
                sistema = st.session_state.sistema
                sucesso = sistema.cadastrar_produto(
                    nome=nome,
                    descricao=descricao,
                    preco=preco,
                    estoque_inicial=estoque_inicial,
                    estoque_minimo=estoque_minimo,
                    categoria=categoria
                )
                
                if sucesso:
                    st.success(f" Produto '{nome}' cadastrado com sucesso!")
                else:
                    st.error(" Erro ao cadastrar produto!")
            else:
                st.warning(" Preencha todos os campos obrigatórios!")

def listar_produtos():
    st.header("📋 Lista de Produtos")
    
    sistema = st.session_state.sistema
    produtos = sistema.listar_produtos()
    
    if not produtos:
        st.info(" Nenhum produto cadastrado.")
        return
    
    for produto in produtos:
        with st.expander(f"**{produto.nome}** - R$ {produto.preco:.2f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**ID:** {produto.id}")
                st.write(f"**Descrição:** {produto.descricao}")
                st.write(f"**Categoria:** {produto.categoria}")
            
            with col2:
                status = " ESTOQUE BAIXO" if produto.verificar_estoque_baixo() else "🟢 NORMAL"
                st.write(f"**Status:** {status}")
                st.write(f"**Estoque Atual:** {produto.estoque_atual}")
                st.write(f"**Estoque Mínimo:** {produto.estoque_minimo}")

def registrar_entrada():
    st.header(" Registrar Entrada no Estoque")
    
    sistema = st.session_state.sistema
    produtos = sistema.listar_produtos()
    
    if not produtos:
        st.warning("Cadastre produtos primeiro!")
        return
    
    produtos_dict = {f"{p.id} - {p.nome}": p.id for p in produtos}
    produto_selecionado = st.selectbox("Selecione o produto:", list(produtos_dict.keys()))
    
    quantidade = st.number_input("Quantidade:", min_value=1, step=1)
    observacao = st.text_input("Observação:")
    
    if st.button("Registrar Entrada"):
        produto_id = produtos_dict[produto_selecionado]
        sucesso = sistema.registrar_entrada(produto_id, quantidade, observacao)
        
        if sucesso:
            st.success(f" Entrada de {quantidade} unidades registrada!")
        else:
            st.error(" Erro ao registrar entrada!")

def registrar_venda():
    st.header(" Registrar Venda")
    
    sistema = st.session_state.sistema
    produtos = sistema.listar_produtos()
    
    if not produtos:
        st.warning("Cadastre produtos primeiro!")
        return
    
    produtos_dict = {f"{p.id} - {p.nome} (Estoque: {p.estoque_atual})": p.id for p in produtos}
    produto_selecionado = st.selectbox("Selecione o produto:", list(produtos_dict.keys()))
    
    quantidade = st.number_input("Quantidade vendida:", min_value=1, step=1)
    
    if st.button("Registrar Venda"):
        produto_id = produtos_dict[produto_selecionado]
        sucesso = sistema.registrar_venda(produto_id, quantidade)
        
        if sucesso:
            st.success(f"Venda de {quantidade} unidades registrada!")
        else:
            st.error(" Erro: Estoque insuficiente ou produto não encontrado!")

def gerar_relatorios():
    st.header(" Relatórios")
    
    sistema = st.session_state.sistema
    
    st.subheader(" Produtos com Estoque Baixo")
    produtos_baixo = sistema.gerar_relatorio_estoque_baixo()
    
    if not produtos_baixo:
        st.success(" Todos os produtos com estoque normal!")
    else:
        st.warning(f" {len(produtos_baixo)} produto(s) com estoque baixo:")
        
        for produto in produtos_baixo:
            deficit = produto.estoque_minimo - produto.estoque_atual
            st.error(f"**{produto.nome}** - Estoque: {produto.estoque_atual} | Mínimo: {produto.estoque_minimo} | Déficit: {deficit} unidades")

def executar_testes():
    st.header(" Testes Automatizados")
    
    if st.button("Executar Todos os Testes"):
        import subprocess
        import sys
        
        st.info("Executando testes...")
        
        with st.spinner("Testando classe Produto..."):
            result = subprocess.run([sys.executable, "tests/testbanch_produto.py"], 
                                  capture_output=True, text=True)
            st.text_area("Resultado - Produto", result.stdout, height=150)
        
        with st.spinner("Testando classe Movimento..."):
            result = subprocess.run([sys.executable, "tests/testbanch_movimento.py"], 
                                  capture_output=True, text=True)
            st.text_area("Resultado - Movimento", result.stdout, height=150)
        
        with st.spinner("Testando Sistema Integrado..."):
            result = subprocess.run([sys.executable, "tests/testbanch_sistema.py"], 
                                  capture_output=True, text=True)
            st.text_area("Resultado - Sistema", result.stdout, height=150)
        
        st.success(" Todos os testes executados!")

if __name__ == "__main__":
    main()