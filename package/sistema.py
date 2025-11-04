import json
import os
from datetime import datetime
from package.produto import Produto
from package.movimento import MovimentoEstoque, TipoMovimento

class SistemaEstoque:
    def __init__(self):
        self.produtos = []
        self.movimentos = []
        self.proximo_id_produto = 1
        self.proximo_id_movimento = 1
        self.carregar_dados()
    
    def cadastrar_produto(self, nome: str, descricao: str, preco: float, 
                         estoque_inicial: int, estoque_minimo: int, categoria: str = "Geral") -> bool:
        try:
            produto = Produto(
                id=self.proximo_id_produto,
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque_atual=estoque_inicial,
                estoque_minimo=estoque_minimo,
                categoria=categoria
            )
            self.produtos.append(produto)
            self.proximo_id_produto += 1
            self.salvar_dados()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar produto: {e}")
            return False
    
    def buscar_produto_por_id(self, id: int) -> Produto:
        for produto in self.produtos:
            if produto.id == id and produto.ativo:
                return produto
        return None
    
    def registrar_entrada(self, produto_id: int, quantidade: int, observacao: str = "") -> bool:
        produto = self.buscar_produto_por_id(produto_id)
        if produto and quantidade > 0:
            if produto.atualizar_estoque(quantidade):
                movimento = MovimentoEstoque(
                    id=self.proximo_id_movimento,
                    produto_id=produto_id,
                    tipo=TipoMovimento.ENTRADA,
                    quantidade=quantidade,
                    observacao=observacao
                )
                self.movimentos.append(movimento)
                self.proximo_id_movimento += 1
                self.salvar_dados()
                return True
        return False
    
    def registrar_venda(self, produto_id: int, quantidade: int) -> bool:
        produto = self.buscar_produto_por_id(produto_id)
        if produto and produto.estoque_atual >= quantidade and quantidade > 0:
            if produto.atualizar_estoque(-quantidade):
                movimento = MovimentoEstoque(
                    id=self.proximo_id_movimento,
                    produto_id=produto_id,
                    tipo=TipoMovimento.SAIDA,
                    quantidade=quantidade,
                    observacao="Venda"
                )
                self.movimentos.append(movimento)
                self.proximo_id_movimento += 1
                self.salvar_dados()
                return True
        return False
    
    def gerar_relatorio_estoque_baixo(self) -> list:
        return [produto for produto in self.produtos if produto.verificar_estoque_baixo() and produto.ativo]
    
    def listar_produtos(self) -> list:
        return [produto for produto in self.produtos if produto.ativo]
    
    def carregar_dados(self):
        try:
            if os.path.exists('produtos.json'):
                with open('produtos.json', 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.produtos = [Produto.from_dict(produto) for produto in dados]
                    if self.produtos:
                        self.proximo_id_produto = max(p.id for p in self.produtos) + 1
            
            if os.path.exists('movimentos.json'):
                with open('movimentos.json', 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.movimentos = [MovimentoEstoque.from_dict(mov) for mov in dados]
                    if self.movimentos:
                        self.proximo_id_movimento = max(m.id for m in self.movimentos) + 1
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
    
    def salvar_dados(self):
        try:
            os.makedirs('db', exist_ok=True)
            
            with open('produtos.json', 'w', encoding='utf-8') as f:
                json.dump([produto.to_dict() for produto in self.produtos], f, indent=2, ensure_ascii=False)
            with open('movimentos.json', 'w', encoding='utf-8') as f:
                json.dump([movimento.to_dict() for movimento in self.movimentos], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
