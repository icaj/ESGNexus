# etapa3_exploracao.py
# ══════════════════════════════════════════════════════════════════
# Etapa 3 — Análise Exploratória
# Edenred Brasil | CESAR School 2025
# ══════════════════════════════════════════════════════════════════

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd

from .config import FEATURES_SCORES, PASTA_SAIDA


def etapa3_exploracao(df: pd.DataFrame):
    """
    Gera o painel de análise exploratória com 7 visualizações:
      1. Distribuição de maturidade (donut)
      2. Empresas por grade total (barras)
      3. Distribuição dos scores por pilar (histograma)
      4. Scatter E × S colorido por maturidade
      5. Score ESG médio por indústria (top 12)
      6. Matriz de Criticidade (scatter impacto × risco)
      7. Distribuição do risco por grade (boxplot)

    Salva em: PASTA_SAIDA/analise_exploratoria.png
    """
    print("\n" + "═"*62)
    print("ETAPA 3 — ANÁLISE EXPLORATÓRIA")
    print("═"*62)

    fig = plt.figure(figsize=(18, 14), facecolor='#F7F8FA')
    fig.suptitle('Análise ESG — Base de 722 Empresas (ESG Enterprise)',
                 fontsize=16, fontweight='bold', color='#1A1A2E', y=0.98)

    gs   = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35,
                             top=0.93, bottom=0.05, left=0.07, right=0.97)
    CORES = {'High': '#2ECC71', 'Medium': '#E74C3C'}
    COLS  = ['#3498DB', '#E74C3C', '#F39C12']

    # 1. Distribuição de maturidade
    ax1 = fig.add_subplot(gs[0, 0])
    vc  = df['total_level'].value_counts()
    wedges, texts, autotexts = ax1.pie(
        vc.values, labels=vc.index,
        colors=[CORES[k] for k in vc.index],
        autopct='%1.1f%%', startangle=90,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(10); at.set_fontweight('bold')
    ax1.set_title('Distribuição de Maturidade', fontweight='bold', fontsize=11)

    # 2. Empresas por grade total
    ax2    = fig.add_subplot(gs[0, 1])
    grades = ['B', 'BB', 'BBB', 'A']
    counts = [df['total_grade'].value_counts().get(g, 0) for g in grades]
    bars   = ax2.bar(grades, counts,
                     color=['#E74C3C','#E67E22','#3498DB','#2ECC71'],
                     edgecolor='white', linewidth=1.5, width=0.6)
    for bar, val in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 str(val), ha='center', fontsize=10, fontweight='bold')
    ax2.set_title('Empresas por Grade Total', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Nº de empresas')
    ax2.set_facecolor('#FAFAFA')
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.grid(axis='y', alpha=0.3)

    # 3. Distribuição dos scores por pilar
    ax3 = fig.add_subplot(gs[0, 2])
    for col, cor, label in zip(FEATURES_SCORES, COLS,
                                ['Ambiental', 'Social', 'Governança']):
        ax3.hist(df[col], bins=25, alpha=0.6, color=cor, label=label)
    ax3.set_title('Distribuição dos Scores por Pilar', fontweight='bold', fontsize=11)
    ax3.set_xlabel('Score (0–1000)')
    ax3.legend(fontsize=8)
    ax3.set_facecolor('#FAFAFA')
    ax3.spines[['top', 'right']].set_visible(False)

    # 4. Scatter E × S por maturidade
    ax4 = fig.add_subplot(gs[1, 0])
    for nivel, cor in CORES.items():
        sub = df[df['total_level'] == nivel]
        ax4.scatter(sub['environment_score'], sub['social_score'],
                    c=cor, alpha=0.5, s=20, label=nivel)
    ax4.set_xlabel('Environment Score')
    ax4.set_ylabel('Social Score')
    ax4.set_title('E × S por Maturidade', fontweight='bold', fontsize=11)
    ax4.legend(fontsize=8)
    ax4.set_facecolor('#FAFAFA')
    ax4.spines[['top', 'right']].set_visible(False)

    # 5. Score médio por indústria (top 12)
    ax5     = fig.add_subplot(gs[1, 1:])
    top_ind = (df.groupby('industry')['total_score']
                 .mean()
                 .sort_values(ascending=False)
                 .head(12))
    colors_bar = ['#2ECC71' if v >= 900 else '#E74C3C' for v in top_ind.values]
    ax5.barh(range(len(top_ind)), top_ind.values, color=colors_bar,
             edgecolor='white', height=0.7)
    ax5.set_yticks(range(len(top_ind)))
    ax5.set_yticklabels(top_ind.index, fontsize=8)
    ax5.axvline(900, color='#2ECC71', ls='--', lw=1.5, alpha=0.7, label='Limiar High (900)')
    ax5.set_title('Score ESG Médio por Indústria (Top 12)', fontweight='bold', fontsize=11)
    ax5.set_xlabel('Total Score')
    ax5.legend(fontsize=8)
    ax5.set_facecolor('#FAFAFA')
    ax5.grid(axis='x', alpha=0.3)
    ax5.spines[['top', 'right']].set_visible(False)

    # 6. Matriz de Criticidade
    ax6       = fig.add_subplot(gs[2, :2])
    cores_quad = {
        'Alto Impacto / Alto Risco':    '#E74C3C',
        'Alto Impacto / Baixo Risco':   '#F1C40F',
        'Baixo Impacto / Alto Risco':   '#E67E22',
        'Baixo Impacto / Baixo Risco':  '#2ECC71',
    }
    for quad, cor in cores_quad.items():
        sub = df[df['quadrante'] == quad]
        ax6.scatter(sub['impacto'], sub['risco'],
                    c=cor, alpha=0.4, s=15,
                    label=f"{quad} (n={len(sub)})")
    ax6.axvline(50, color='gray', ls='--', lw=1, alpha=0.5)
    ax6.axhline(50, color='gray', ls='--', lw=1, alpha=0.5)
    ax6.set_xlabel('Impacto (percentil score_ponderado no setor)')
    ax6.set_ylabel('Risco ESG (%)')
    ax6.set_title('Matriz de Criticidade', fontweight='bold', fontsize=11)
    ax6.legend(fontsize=7, loc='upper left')
    ax6.set_facecolor('#FAFAFA')
    ax6.spines[['top', 'right']].set_visible(False)

    # 7. Distribuição do risco por grade
    ax7      = fig.add_subplot(gs[2, 2])
    ordem    = ['A', 'BBB', 'BB', 'B']
    data_box = [df[df['total_grade'] == g]['risco'].values for g in ordem]
    bp       = ax7.boxplot(data_box, labels=ordem, patch_artist=True)
    cores_box = ['#2ECC71', '#3498DB', '#E67E22', '#E74C3C']
    for patch, cor in zip(bp['boxes'], cores_box):
        patch.set_facecolor(cor); patch.set_alpha(0.7)
    ax7.set_title('Distribuição do Risco por Grade', fontweight='bold', fontsize=11)
    ax7.set_xlabel('Grade')
    ax7.set_ylabel('Risco ESG (%)')
    ax7.set_facecolor('#FAFAFA')
    ax7.spines[['top', 'right']].set_visible(False)

    plt.savefig(f'{PASTA_SAIDA}/analise_exploratoria.png',
                dpi=140, bbox_inches='tight', facecolor='#F7F8FA')
    plt.close()
    print(f"\nGráfico salvo: {PASTA_SAIDA}/analise_exploratoria.png")

    # Estatísticas textuais
    print("\nCorrelação entre features e total_score:")
    print(df[FEATURES_SCORES + ['total_score']]
          .corr()['total_score']
          .drop('total_score')
          .round(3))

    print("\nScore médio por maturidade:")
    print(df.groupby('maturidade')[
        FEATURES_SCORES + ['total_score', 'risco', 'impacto']
    ].mean().round(1))


if __name__ == "__main__":
    from .etapa1_preprocessamento import etapa1_preprocessamento
    from .etapa2_metricas import etapa2_metricas
    df, _, _ = etapa2_metricas(etapa1_preprocessamento())
    etapa3_exploracao(df)
