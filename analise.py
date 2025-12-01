"""
Análise de Dados de Vendas - Versão Avançada
Script principal para execução rápida
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def analise_rapida():
    """Executa uma análise rápida e eficiente"""
    print("🔍 Análise Rápida de Vendas")
    print("-" * 40)
    
    # Carregar dados
    df = pd.read_csv("sales.csv")
    
    # Limpeza básica
    df = df.drop_duplicates()
    df['date'] = pd.to_datetime(df['date'])
    
    # Cálculos básicos
    df['revenue'] = df['price'] * df['quantity']
    
    # Análise por produto
    print("\n📊 Faturamento por Produto:")
    faturamento_produto = df.groupby('product')['revenue'].sum().sort_values(ascending=False)
    for produto, valor in faturamento_produto.items():
        print(f"  {produto}: R$ {valor:,.2f}")
    
    # Análise por região
    print("\n🌍 Faturamento por Região:")
    faturamento_regiao = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
    for regiao, valor in faturamento_regiao.items():
        print(f"  {regiao}: R$ {valor:,.2f}")
    
    # Métricas gerais
    print("\n📈 Métricas Gerais:")
    print(f"  Total de Vendas: {len(df):,}")
    print(f"  Faturamento Total: R$ {df['revenue'].sum():,.2f}")
    print(f"  Ticket Médio: R$ {df['revenue'].mean():,.2f}")
    print(f"  Período: {df['date'].min().date()} a {df['date'].max().date()}")
    
    # Top performers
    melhor_venda = df.loc[df['revenue'].idxmax()]
    print(f"\n🏆 Melhor Venda:")
    print(f"  Produto: {melhor_venda['product']}")
    print(f"  Valor: R$ {melhor_venda['revenue']:,.2f}")
    print(f"  Data: {melhor_venda['date'].date()}")
    print(f"  Região: {melhor_venda['region']}")
    
    # Gerar gráfico simples
    plt.figure(figsize=(10, 6))
    faturamento_produto.plot(kind='bar', color='skyblue')
    plt.title('Faturamento por Produto', fontweight='bold')
    plt.ylabel('Faturamento (R$)')
    plt.xlabel('Produto')
    plt.tight_layout()
    plt.savefig('analise_rapida.png', dpi=150)
    
    print(f"\n✅ Análise concluída! Gráfico salvo como 'analise_rapida.png'")

if __name__ == "__main__":
    analise_rapida()