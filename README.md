# 📈 Sistema Avançado de Análise de Vendas

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema completo para análise, visualização e geração de insights a partir de dados de vendas.

## ✨ Funcionalidades

### 🔍 Análise Completa
- **Análise Descritiva**: Métricas gerais do negócio
- **Segmentação**: Por produto, região, período e categoria
- **Análise Temporal**: Tendências, sazonalidade e crescimento
- **Análise Cruzada**: Múltiplas dimensões simultaneamente

### 📊 Visualizações
- Dashboard estático (Matplotlib/Seaborn)
- Dashboard interativo (Plotly)
- Gráficos especializados por tipo de análise
- Exportação em alta qualidade

### 📈 Insights Automatizados
- Identificação de padrões
- Detecção de anomalias
- Recomendações baseadas em dados
- Relatórios executivos automáticos

### 💾 Exportação
- Dados processados (CSV, Excel)
- Relatórios em Markdown
- Gráficos em PNG/HTML
- Resultados estruturados

## 🚀 Começando

### Instalação Rápida
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/analise-vendas.git

# Entre no diretório
cd analise-vendas

# Instale as dependências
pip install -r requirements.txt
```

### Execução Simples
```bash
# Análise básica (rápida)
python analise.py

# Análise completa (avançada)
python analise_avancada.py
```

### Execução em Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar análise
python analise_avancada.py
```

## 📁 Estrutura de Saída

Após a execução, serão gerados:

```
📁 outputs/
├── 📊 dashboard_vendas.png          # Dashboard estático
├── 🌐 dashboard_interativo.html     # Dashboard interativo
├── 📝 relatorio_analise.md          # Relatório completo
├── 💾 dados_processados.csv         # Dados limpos
├── 📦 analise_produto.csv           # Análise por produto
├── 🌍 analise_regiao.csv            # Análise por região
└── 📋 resultados_completos.xlsx     # Excel com todas as análises
```

## 🔧 Dependências Principais

| Biblioteca | Versão | Finalidade |
|------------|--------|------------|
| pandas | ≥2.0.0 | Manipulação de dados |
| numpy | ≥1.24.0 | Computação numérica |
| matplotlib | ≥3.7.0 | Visualização estática |
| seaborn | ≥0.12.0 | Visualização estatística |
| plotly | ≥5.15.0 | Visualização interativa |
| scikit-learn | ≥1.3.0 | Análise preditiva |
| openpyxl | ≥3.1.0 | Exportação Excel |

## 📚 Exemplos de Uso

### Análise Personalizada
```python
from src.analysis import AnaliseVendasAvancada

# Criar instância
analise = AnaliseVendasAvancada("sales.csv")

# Executar análises específicas
metricas = analise.calcular_metricas_gerais()
produtos = analise.analise_por_produto()
regioes = analise.analise_por_regiao()

# Gerar visualizações
analise.gerar_visualizacoes()

# Exportar resultados
analise.exportar_resultados(formatos=['csv', 'excel'])
```

### Pipeline Completo
```python
# Executar toda a pipeline
analise.executar_analise_completa()
```

## 🧪 Testes

```bash
# Executar testes unitários
python -m pytest tests/ -v

# Executar testes com cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

## 📊 Métricas Calculadas

### Básicas
- Total de vendas e faturamento
- Ticket médio
- Quantidade média por venda
- Crescimento diário/semanal

### Avançadas
- Lucratividade por produto/região
- Participação de mercado
- Correlação entre variáveis
- Detecção de padrões sazonais
- Identificação de outliers

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/analise-vendas/issues)
- **Documentação**: Consulte os docstrings no código
- **Exemplos**: Veja a pasta `examples/`

## 📞 Contato

Desenvolvido por [Seu Nome] - [seu.email@example.com]

---
⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!