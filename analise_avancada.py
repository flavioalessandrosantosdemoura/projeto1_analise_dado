"""
Análise Avançada de Dados de Vendas
Autor: Sistema de Análise
Data: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configurações de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

class AnaliseVendasAvancada:
    """
    Classe para análise avançada de dados de vendas
    """
    
    def __init__(self, filepath="sales.csv"):
        """
        Inicializa a análise carregando e preparando os dados
        
        Args:
            filepath (str): Caminho para o arquivo CSV
        """
        self.filepath = filepath
        self.df = None
        self.df_processado = None
        self.metricas = {}
        self.insights = []
        
        self.carregar_dados()
        self.preparar_dados()
        
    def carregar_dados(self):
        """Carrega e valida os dados do arquivo CSV"""
        try:
            self.df = pd.read_csv(self.filepath)
            print(f"✅ Dados carregados com sucesso!")
            print(f"   • Registros: {len(self.df)}")
            print(f"   • Colunas: {list(self.df.columns)}")
            print(f"   • Período: {self.df['date'].min()} a {self.df['date'].max()}")
        except FileNotFoundError:
            print(f"❌ Arquivo {self.filepath} não encontrado!")
            raise
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            raise
    
    def preparar_dados(self):
        """Realiza limpeza, transformação e enriquecimento dos dados"""
        print("\n🔧 Preparando dados...")
        
        # Backup dos dados originais
        self.df_processado = self.df.copy()
        
        # 1. Limpeza básica
        registros_iniciais = len(self.df_processado)
        self.df_processado.drop_duplicates(inplace=True)
        self.df_processado.dropna(inplace=True)
        registros_finais = len(self.df_processado)
        
        print(f"   • Duplicados/NaN removidos: {registros_iniciais - registros_finais}")
        
        # 2. Transformação de tipos
        self.df_processado['date'] = pd.to_datetime(self.df_processado['date'])
        
        # 3. Criação de novas features
        # Faturamento
        self.df_processado['revenue'] = self.df_processado['price'] * self.df_processado['quantity']
        
        # Médias móveis (para análise temporal)
        self.df_processado['revenue_ma7'] = (
            self.df_processado.groupby('product')['revenue']
            .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
        )
        
        # Dia da semana e mês
        self.df_processado['day_of_week'] = self.df_processado['date'].dt.day_name()
        self.df_processado['month'] = self.df_processado['date'].dt.month_name()
        self.df_processado['week_number'] = self.df_processado['date'].dt.isocalendar().week
        
        # Categoria de preço
        self.df_processado['price_category'] = pd.cut(
            self.df_processado['price'],
            bins=[0, 50, 100, 150, 200],
            labels=['Baixo', 'Médio', 'Alto', 'Premium']
        )
        
        # Valor do pedido
        self.df_processado['order_value_category'] = pd.cut(
            self.df_processado['revenue'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Pequeno', 'Médio', 'Grande', 'Muito Grande']
        )
        
        # Margem (simulada para exemplo)
        np.random.seed(42)
        self.df_processado['margin_percent'] = np.random.uniform(20, 60, len(self.df_processado))
        self.df_processado['cost'] = self.df_processado['price'] * (1 - self.df_processado['margin_percent']/100)
        self.df_processado['profit'] = self.df_processado['revenue'] - (
            self.df_processado['cost'] * self.df_processado['quantity']
        )
        
        print("✅ Dados preparados com sucesso!")
    
    def calcular_metricas_gerais(self):
        """Calcula métricas gerais do negócio"""
        print("\n📊 Calculando métricas gerais...")
        
        metricas = {
            # Métricas de Volume
            'total_vendas': len(self.df_processado),
            'total_produtos_vendidos': self.df_processado['quantity'].sum(),
            'total_faturamento': self.df_processado['revenue'].sum(),
            'total_lucro': self.df_processado['profit'].sum(),
            
            # Métricas Médias
            'ticket_medio': self.df_processado['revenue'].mean(),
            'quantidade_media_por_venda': self.df_processado['quantity'].mean(),
            'preco_medio': self.df_processado['price'].mean(),
            'margem_media': self.df_processado['margin_percent'].mean(),
            
            # Métricas por Período
            'vendas_por_dia': len(self.df_processado) / self.df_processado['date'].nunique(),
            'faturamento_por_dia': self.df_processado.groupby('date')['revenue'].sum().mean(),
            
            # Diversidade
            'num_produtos': self.df_processado['product'].nunique(),
            'num_regioes': self.df_processado['region'].nunique(),
            
            # Eficiência
            'lucratividade': (self.df_processado['profit'].sum() / self.df_processado['revenue'].sum()) * 100
        }
        
        self.metricas.update(metricas)
        
        # Apresentação das métricas
        print("\n" + "="*50)
        print("MÉTRICAS GERAIS DO NEGÓCIO")
        print("="*50)
        
        for key, value in metricas.items():
            if 'total' in key or 'faturamento' in key or 'lucro' in key:
                print(f"{key.replace('_', ' ').title()}: R$ {value:,.2f}")
            elif 'percent' in key or 'margem' in key or 'lucratividade' in key:
                print(f"{key.replace('_', ' ').title()}: {value:.1f}%")
            elif 'medio' in key or 'media' in key:
                print(f"{key.replace('_', ' ').title()}: R$ {value:,.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value:,.0f}")
        
        return metricas
    
    def analise_por_produto(self):
        """Análise detalhada por produto"""
        print("\n📦 Análise por Produto")
        print("-"*40)
        
        analise_produto = self.df_processado.groupby('product').agg({
            'quantity': ['sum', 'mean', 'count'],
            'revenue': ['sum', 'mean'],
            'profit': ['sum', 'mean'],
            'price': ['mean', 'std'],
            'margin_percent': 'mean'
        }).round(2)
        
        # Renomear colunas
        analise_produto.columns = [
            'qtd_total', 'qtd_media', 'num_vendas',
            'faturamento_total', 'faturamento_medio',
            'lucro_total', 'lucro_medio',
            'preco_medio', 'preco_std',
            'margem_media'
        ]
        
        # Ordenar por faturamento
        analise_produto = analise_produto.sort_values('faturamento_total', ascending=False)
        
        print(analise_produto.to_string())
        
        # Insights
        produto_top = analise_produto.index[0]
        produto_pior = analise_produto.index[-1]
        
        self.insights.append(f"📈 Produto mais rentável: {produto_top} (R$ {analise_produto.loc[produto_top, 'faturamento_total']:,.2f})")
        self.insights.append(f"📉 Produto menos rentável: {produto_pior} (R$ {analise_produto.loc[produto_pior, 'faturamento_total']:,.2f})")
        
        return analise_produto
    
    def analise_por_regiao(self):
        """Análise detalhada por região"""
        print("\n🌍 Análise por Região")
        print("-"*40)
        
        analise_regiao = self.df_processado.groupby('region').agg({
            'revenue': ['sum', 'mean', 'count'],
            'profit': ['sum', 'mean'],
            'quantity': 'sum',
            'product': pd.Series.nunique
        }).round(2)
        
        analise_regiao.columns = [
            'faturamento_total', 'faturamento_medio', 'num_vendas',
            'lucro_total', 'lucro_medio',
            'qtd_total', 'num_produtos'
        ]
        
        # Calcular participação de mercado
        analise_regiao['participacao'] = (
            analise_regiao['faturamento_total'] / analise_regiao['faturamento_total'].sum() * 100
        ).round(1)
        
        analise_regiao = analise_regiao.sort_values('faturamento_total', ascending=False)
        
        print(analise_regiao.to_string())
        
        # Insights
        regiao_top = analise_regiao.index[0]
        participacao_top = analise_regiao.loc[regiao_top, 'participacao']
        
        self.insights.append(f"🏆 Região líder: {regiao_top} ({participacao_top}% do faturamento total)")
        
        return analise_regiao
    
    def analise_temporal(self):
        """Análise de tendências temporais"""
        print("\n📅 Análise Temporal")
        print("-"*40)
        
        # Agrupar por data
        vendas_diarias = self.df_processado.groupby('date').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'profit': 'sum'
        }).resample('D').sum()
        
        # Preencher dias sem vendas
        date_range = pd.date_range(
            start=self.df_processado['date'].min(),
            end=self.df_processado['date'].max()
        )
        vendas_diarias = vendas_diarias.reindex(date_range, fill_value=0)
        
        # Métricas temporais
        crescimento_diario = vendas_diarias['revenue'].pct_change().mean() * 100
        
        print(f"📈 Crescimento médio diário: {crescimento_diario:.2f}%")
        print(f"📊 Faturamento médio diário: R$ {vendas_diarias['revenue'].mean():,.2f}")
        print(f"📈 Melhor dia: {vendas_diarias['revenue'].idxmax().date()} (R$ {vendas_diarias['revenue'].max():,.2f})")
        print(f"📉 Pior dia: {vendas_diarias['revenue'].idxmin().date()} (R$ {vendas_diarias['revenue'].min():,.2f})")
        
        # Análise por dia da semana
        vendas_dia_semana = self.df_processado.groupby('day_of_week').agg({
            'revenue': ['sum', 'mean', 'count']
        }).round(2)
        
        vendas_dia_semana.columns = ['faturamento_total', 'faturamento_medio', 'num_vendas']
        
        # Ordenar por ordem da semana
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        vendas_dia_semana = vendas_dia_semana.reindex(dias_ordem)
        
        print("\n📆 Faturamento por Dia da Semana:")
        print(vendas_dia_semana.to_string())
        
        melhor_dia = vendas_dia_semana['faturamento_total'].idxmax()
        self.insights.append(f"🗓️ Melhor dia para vendas: {melhor_dia}")
        
        return {
            'vendas_diarias': vendas_diarias,
            'vendas_dia_semana': vendas_dia_semana
        }
    
    def analise_cruzada(self):
        """Análises cruzadas entre diferentes dimensões"""
        print("\n🔀 Análises Cruzadas")
        print("-"*40)
        
        # Produto x Região
        print("📊 Produto x Região (Faturamento):")
        pivot_produto_regiao = pd.pivot_table(
            self.df_processado,
            values='revenue',
            index='product',
            columns='region',
            aggfunc='sum',
            fill_value=0
        )
        print(pivot_produto_regiao.to_string())
        
        # Região x Categoria de Preço
        print("\n🏷️ Região x Categoria de Preço:")
        pivot_regiao_categoria = pd.pivot_table(
            self.df_processado,
            values='revenue',
            index='region',
            columns='price_category',
            aggfunc='sum',
            fill_value=0
        )
        print(pivot_regiao_categoria.to_string())
        
        return {
            'produto_regiao': pivot_produto_regiao,
            'regiao_categoria': pivot_regiao_categoria
        }
    
    def identificar_padroes(self):
        """Identifica padrões e anomalias nos dados"""
        print("\n🔍 Identificando Padrões")
        print("-"*40)
        
        # 1. Produtos com maior ticket médio
        ticket_medio_produto = self.df_processado.groupby('product')['revenue'].mean().sort_values(ascending=False)
        print("🎫 Ticket Médio por Produto:")
        print(ticket_medio_produto.to_string())
        
        # 2. Regiões com maior margem
        margem_regiao = self.df_processado.groupby('region')['margin_percent'].mean().sort_values(ascending=False)
        print("\n💰 Margem Média por Região:")
        print(margem_regiao.to_string())
        
        # 3. Sazonalidade semanal
        vendas_semana = self.df_processado.groupby('week_number')['revenue'].sum()
        crescimento_semanal = vendas_semana.pct_change().mean() * 100
        print(f"\n📈 Crescimento semanal médio: {crescimento_semanal:.2f}%")
        
        # 4. Identificar outliers
        Q1 = self.df_processado['revenue'].quantile(0.25)
        Q3 = self.df_processado['revenue'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = self.df_processado[
            (self.df_processado['revenue'] < (Q1 - 1.5 * IQR)) |
            (self.df_processado['revenue'] > (Q3 + 1.5 * IQR))
        ]
        
        if len(outliers) > 0:
            print(f"\n⚠️  {len(outliers)} outliers identificados nas vendas")
            self.insights.append(f"⚠️  {len(outliers)} vendas atípicas detectadas")
        
        # 5. Correlações
        correlacao = self.df_processado[['price', 'quantity', 'revenue', 'profit']].corr()
        print("\n🔄 Matriz de Correlação:")
        print(correlacao.to_string())
    
    def gerar_visualizacoes(self):
        """Gera visualizações gráficas dos dados"""
        print("\n🎨 Gerando visualizações...")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Dashboard de Análise de Vendas', fontsize=16, fontweight='bold')
        
        # 1. Faturamento por Produto
        faturamento_produto = self.df_processado.groupby('product')['revenue'].sum()
        axes[0, 0].bar(faturamento_produto.index, faturamento_produto.values, color='skyblue')
        axes[0, 0].set_title('Faturamento por Produto', fontweight='bold')
        axes[0, 0].set_ylabel('Faturamento (R$)')
        axes[0, 0].ticklabel_format(axis='y', style='plain')
        
        # 2. Faturamento por Região
        faturamento_regiao = self.df_processado.groupby('region')['revenue'].sum()
        axes[0, 1].pie(faturamento_regiao.values, labels=faturamento_regiao.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Participação por Região', fontweight='bold')
        
        # 3. Evolução Temporal
        vendas_diarias = self.df_processado.groupby('date')['revenue'].sum()
        axes[0, 2].plot(vendas_diarias.index, vendas_diarias.values, marker='o', linewidth=2)
        axes[0, 2].set_title('Evolução Diária', fontweight='bold')
        axes[0, 2].set_ylabel('Faturamento (R$)')
        axes[0, 2].tick_params(axis='x', rotation=45)
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Ticket Médio por Dia da Semana
        ticket_dia_semana = self.df_processado.groupby('day_of_week')['revenue'].mean()
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ticket_dia_semana = ticket_dia_semana.reindex(dias_ordem)
        axes[1, 0].bar(ticket_dia_semana.index, ticket_dia_semana.values, color='lightgreen')
        axes[1, 0].set_title('Ticket Médio por Dia', fontweight='bold')
        axes[1, 0].set_ylabel('Ticket Médio (R$)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 5. Quantidade vs Preço
        scatter = axes[1, 1].scatter(
            self.df_processado['price'],
            self.df_processado['quantity'],
            c=self.df_processado['revenue'],
            cmap='viridis',
            alpha=0.6,
            s=100
        )
        axes[1, 1].set_title('Preço vs Quantidade', fontweight='bold')
        axes[1, 1].set_xlabel('Preço (R$)')
        axes[1, 1].set_ylabel('Quantidade')
        plt.colorbar(scatter, ax=axes[1, 1], label='Faturamento')
        
        # 6. Heatmap Produto x Região
        pivot_data = pd.pivot_table(
            self.df_processado,
            values='revenue',
            index='product',
            columns='region',
            aggfunc='sum',
            fill_value=0
        )
        im = axes[1, 2].imshow(pivot_data.values, cmap='YlOrRd', aspect='auto')
        axes[1, 2].set_title('Produto x Região (Faturamento)', fontweight='bold')
        axes[1, 2].set_xticks(range(len(pivot_data.columns)))
        axes[1, 2].set_xticklabels(pivot_data.columns, rotation=45)
        axes[1, 2].set_yticks(range(len(pivot_data.index)))
        axes[1, 2].set_yticklabels(pivot_data.index)
        plt.colorbar(im, ax=axes[1, 2], label='Faturamento (R$)')
        
        plt.tight_layout()
        plt.savefig('dashboard_vendas.png', dpi=300, bbox_inches='tight')
        print("✅ Dashboard salvo como 'dashboard_vendas.png'")
        
        # Gráfico interativo com Plotly
        fig_interactive = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Faturamento por Produto', 'Evolução Temporal', 
                          'Margem por Região', 'Correlações'),
            specs=[[{'type': 'bar'}, {'type': 'scatter'}],
                   [{'type': 'pie'}, {'type': 'heatmap'}]]
        )
        
        # Gráfico 1: Barras
        fig_interactive.add_trace(
            go.Bar(x=faturamento_produto.index, y=faturamento_produto.values,
                  name='Faturamento', marker_color='indianred'),
            row=1, col=1
        )
        
        # Gráfico 2: Linha
        fig_interactive.add_trace(
            go.Scatter(x=vendas_diarias.index, y=vendas_diarias.values,
                      mode='lines+markers', name='Evolução',
                      line=dict(color='royalblue', width=2)),
            row=1, col=2
        )
        
        # Gráfico 3: Pizza
        margem_regiao = self.df_processado.groupby('region')['margin_percent'].mean()
        fig_interactive.add_trace(
            go.Pie(labels=margem_regiao.index, values=margem_regiao.values,
                  name='Margem', hole=0.3),
            row=2, col=1
        )
        
        # Gráfico 4: Heatmap
        fig_interactive.add_trace(
            go.Heatmap(z=correlacao.values,
                      x=correlacao.columns,
                      y=correlacao.index,
                      colorscale='RdBu',
                      zmid=0),
            row=2, col=2
        )
        
        fig_interactive.update_layout(height=800, showlegend=False,
                                    title_text="Dashboard Interativo de Vendas")
        fig_interactive.write_html('dashboard_interativo.html')
        print("✅ Dashboard interativo salvo como 'dashboard_interativo.html'")
        
        plt.show()
    
    def gerar_relatorio(self):
        """Gera um relatório completo em formato markdown"""
        print("\n📝 Gerando relatório completo...")
        
        relatorio = f"""
# 📊 Relatório de Análise de Vendas
**Data da análise:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Período analisado:** {self.df_processado['date'].min().date()} a {self.df_processado['date'].max().date()}

## 📈 Resumo Executivo
- **Total de Vendas:** {self.metricas.get('total_vendas', 0):,}
- **Faturamento Total:** R$ {self.metricas.get('total_faturamento', 0):,.2f}
- **Lucro Total:** R$ {self.metricas.get('total_lucro', 0):,.2f}
- **Lucratividade:** {self.metricas.get('lucratividade', 0):.1f}%

## 🎯 Insights Principais
{chr(10).join(f"- {insight}" for insight in self.insights)}

## 📦 Desempenho por Produto
| Produto | Vendas | Faturamento | Lucro | Ticket Médio |
|---------|--------|-------------|-------|--------------|
"""
        analise_produto = self.analise_por_produto()
        for produto, dados in analise_produto.iterrows():
            relatorio += f"| {produto} | {dados['num_vendas']:,} | R$ {dados['faturamento_total']:,.2f} | R$ {dados['lucro_total']:,.2f} | R$ {dados['faturamento_medio']:,.2f} |\n"

        relatorio += f"""
## 🌍 Desempenho por Região
| Região | Participação | Faturamento | Vendas |
|--------|--------------|-------------|--------|
"""
        analise_regiao = self.analise_por_regiao()
        for regiao, dados in analise_regiao.iterrows():
            relatorio += f"| {regiao} | {dados['participacao']}% | R$ {dados['faturamento_total']:,.2f} | {dados['num_vendas']:,} |\n"

        relatorio += f"""
## 📅 Análise Temporal
- **Crescimento médio diário:** {self.df_processado.groupby('date')['revenue'].sum().pct_change().mean()*100:.2f}%
- **Melhor dia da semana:** {analise_produto.index[0]}
- **Sazonalidade:** {'Crescimento consistente' if self.metricas.get('crescimento_diario', 0) > 0 else 'Estabilidade'}

## 💡 Recomendações
1. **Focar no produto {analise_produto.index[0]}** que representa a maior fatia do faturamento
2. **Expandir na região {analise_regiao.index[0]}** que apresenta melhor desempenho
3. **Otimizar preços** dos produtos com menor margem
4. **Investigar dias com baixa performance** para identificar causas

## 📊 Visualizações
- Dashboard estático: `dashboard_vendas.png`
- Dashboard interativo: `dashboard_interativo.html`

---

*Relatório gerado automaticamente pelo Sistema de Análise de Vendas*
"""
        
        with open('relatorio_analise.md', 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        print("✅ Relatório salvo como 'relatorio_analise.md'")
        return relatorio
    
    def exportar_resultados(self, formatos=['csv', 'excel']):
        """Exporta resultados para diferentes formatos"""
        print("\n💾 Exportando resultados...")
        
        # DataFrame principal
        if 'csv' in formatos:
            self.df_processado.to_csv('dados_processados.csv', index=False)
            print("✅ Dados processados exportados para 'dados_processados.csv'")
        
        # Análise por produto
        analise_produto = self.analise_por_produto()
        if 'csv' in formatos:
            analise_produto.to_csv('analise_produto.csv')
            print("✅ Análise por produto exportada para 'analise_produto.csv'")
        
        # Análise por região
        analise_regiao = self.analise_por_regiao()
        if 'csv' in formatos:
            analise_regiao.to_csv('analise_regiao.csv')
            print("✅ Análise por região exportada para 'analise_regiao.csv'")
        
        # Exportar para Excel com múltiplas abas
        if 'excel' in formatos:
            with pd.ExcelWriter('resultados_completos.xlsx', engine='openpyxl') as writer:
                self.df_processado.to_excel(writer, sheet_name='Dados Completos', index=False)
                analise_produto.to_excel(writer, sheet_name='Análise Produto')
                analise_regiao.to_excel(writer, sheet_name='Análise Região')
                
                # Adicionar métricas
                metricas_df = pd.DataFrame(list(self.metricas.items()), columns=['Métrica', 'Valor'])
                metricas_df.to_excel(writer, sheet_name='Métricas Gerais', index=False)
                
                # Insights
                insights_df = pd.DataFrame(self.insights, columns=['Insights'])
                insights_df.to_excel(writer, sheet_name='Insights', index=False)
            
            print("✅ Resultados completos exportados para 'resultados_completos.xlsx'")
    
    def executar_analise_completa(self):
        """Executa toda a pipeline de análise"""
        print("\n" + "="*60)
        print("🚀 INICIANDO ANÁLISE AVANÇADA DE VENDAS")
        print("="*60)
        
        # Pipeline de análise
        self.calcular_metricas_gerais()
        self.analise_por_produto()
        self.analise_por_regiao()
        self.analise_temporal()
        self.analise_cruzada()
        self.identificar_padroes()
        self.gerar_visualizacoes()
        self.gerar_relatorio()
        self.exportar_resultados(formatos=['csv', 'excel'])
        
        print("\n" + "="*60)
        print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\n📁 Arquivos gerados:")
        print("   • dashboard_vendas.png")
        print("   • dashboard_interativo.html")
        print("   • relatorio_analise.md")
        print("   • dados_processados.csv")
        print("   • resultados_completos.xlsx")
        print("\n🎯 Insights principais:")
        for insight in self.insights[:5]:  # Mostrar apenas os 5 principais
            print(f"   • {insight}")


# Função principal
def main():
    """Função principal do sistema de análise"""
    try:
        # Inicializar análise
        analise = AnaliseVendasAvancada("sales.csv")
        
        # Executar análise completa
        analise.executar_analise_completa()
        
    except Exception as e:
        print(f"\n❌ Erro durante a análise: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()