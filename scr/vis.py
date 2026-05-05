import matplotlib.pyplot as plt
from . import loan
from . import equity as eq

def plotar_patrimonio_por_tempo(patrimonio_inicial, 
                                aporte_mensal, 
                                rendimento_mensal, 
                                aumento_aporte_mensal, 
                                meses):
    patrimonio_por_mes = eq.patrimonio_puro_por_tempo(patrimonio_inicial, 
                                                      aporte_mensal, 
                                                      rendimento_mensal, 
                                                      aumento_aporte_mensal, 
                                                      meses)

    plt.figure(figsize=(10, 6))
    plt.plot(patrimonio_por_mes, marker='')
    plt.title('Evolução do Patrimônio ao Longo do Tempo')
    plt.xlabel('Meses')
    plt.ylabel('Patrimônio (R$)')
    plt.grid()
    plt.show()

def plotar_comparacao(patrimonio_inicial, 
                      aporte_mensal, 
                      rendimento_mensal, 
                      aumento_aporte_mensal, 
                      meses):
    patrimonio_com_aumento = eq.patrimonio_puro_por_tempo(patrimonio_inicial, 
                                                          aporte_mensal, 
                                                          rendimento_mensal, 
                                                          aumento_aporte_mensal, 
                                                          meses)
    patrimonio_sem_aumento = eq.patrimonio_puro_por_tempo(patrimonio_inicial, 
                                                          aporte_mensal, 
                                                          rendimento_mensal, 
                                                          1.0, 
                                                          meses)

    plt.figure(figsize=(10, 6))
    plt.plot(patrimonio_com_aumento, label='Com Aumento de Aporte Mensal', marker='')
    plt.plot(patrimonio_sem_aumento, label='Sem Aumento de Aporte Mensal', marker='')
    plt.title('Comparação do Patrimônio com e sem Aumento de Aporte Mensal')
    plt.xlabel('Meses')
    plt.ylabel('Patrimônio (R$)')
    plt.legend()
    plt.grid()
    plt.show()

def plotar_patrimonio_total_por_tempo(patrimonio_inicial, 
                                      aporte_mensal_fixo, 
                                      rendimento_mensal, 
                                      aumento_aporte_mensal, 
                                      tempo_horizonte,
                                      valor_vista, 
                                      valor_entrada, 
                                      valor_parcela, 
                                      valor_manutencao, 
                                      ganho_problema, 
                                      mes_compra, 
                                      juros_mensais):
    
    num_parcelas = loan.encontrar_numero_parcelas(
        loan.tabela_comparativa(valor_vista, valor_entrada, juros_mensais),
        valor_parcela
    )

    meses_apos = tempo_horizonte - mes_compra - num_parcelas

    serie_antes = eq.patrimonio_antes_por_tempo(
        patrimonio_inicial, 
        aporte_mensal_fixo, 
        rendimento_mensal, 
        aumento_aporte_mensal, 
        mes_compra,
        valor_parcela,
        valor_manutencao
    )

    serie_durante = eq.patrimonio_durante_por_tempo(
        patrimonio_inicial, 
        aporte_mensal_fixo, 
        rendimento_mensal, 
        aumento_aporte_mensal, 
        mes_compra,
        valor_vista, 
        valor_entrada, 
        valor_parcela, 
        juros_mensais, 
        valor_manutencao, 
        ganho_problema
    )

    serie_apos = eq.patrimonio_apos_por_tempo(
        patrimonio_inicial, 
        aporte_mensal_fixo, 
        rendimento_mensal, 
        aumento_aporte_mensal, 
        meses_apos,
        valor_vista, 
        valor_entrada, 
        valor_parcela, 
        valor_manutencao, 
        ganho_problema, 
        mes_compra, 
        juros_mensais
    )

    patrimonio_por_tempo = (
        serie_antes +
        serie_durante[:-2] +
        serie_apos[1:]
    )
    
    mes_fim_divida = mes_compra + num_parcelas +1
    mes_final = len(patrimonio_por_tempo) - 1

    if mes_fim_divida > tempo_horizonte:
        mes_fim_divida = tempo_horizonte    

    if mes_final > tempo_horizonte:
        mes_final = tempo_horizonte

    plt.figure(figsize=(21,9))
    plt.plot(patrimonio_por_tempo[0:tempo_horizonte], '-.')

    # inicial
    plt.plot(0,
                patrimonio_por_tempo[0],
                marker='s',
                color='blue',
                label=f'Patrimônio inicial: R$ {patrimonio_inicial:.0f}')

    # compra
    plt.plot(mes_compra-1,
                patrimonio_por_tempo[mes_compra-1],
                marker='o',
                color='blue',
                label=f'Patrimônio total no mês da compra: R$ {patrimonio_por_tempo[mes_compra-1]:.0f}')
    
    # começo da dívida
    plt.plot(mes_compra,
                patrimonio_por_tempo[mes_compra],
                marker='v',
                color='red',
                label=f'Começo da dívida: R$ {patrimonio_por_tempo[mes_compra]:.0f}')

    # fim da dívida
    plt.plot(mes_fim_divida-3,
                patrimonio_por_tempo[mes_fim_divida-3],
                marker='v',
                color='red',
                label=f'Fim da dívida: R$ {patrimonio_por_tempo[mes_fim_divida-3]:.0f}')

    # final
    plt.plot(mes_final,
                patrimonio_por_tempo[mes_final],
                marker='^',
                color='green',
                label=f'Final: R$ {patrimonio_por_tempo[mes_final]:.0f}')

    # layout
    plt.title('Evolução do Patrimônio Total',fontsize=17)
    plt.xlabel('Meses',fontsize=15)
    plt.ylabel('Patrimônio (R$)',fontsize=15)
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend(fontsize=20)
    plt.grid()
    plt.show()

def plotar_patrimonio_a_vista_por_tempo(patrimonio_inicial, 
                                        aporte_mensal_fixo, 
                                        rendimento_mensal, 
                                        aumento_aporte_mensal, 
                                        tempo_horizonte,
                                        valor_vista, 
                                        valor_manutencao, 
                                        ganho_problema, 
                                        mes_compra,
                                        valor_parcela):
    
    patrimonio_por_tempo = []

    #append do patrimônio por tempo antes da dívida:
    patrimonio_por_tempo.extend(eq.patrimonio_antes_por_tempo(patrimonio_inicial, 
                                                           aporte_mensal_fixo, 
                                                           rendimento_mensal, 
                                                           aumento_aporte_mensal, 
                                                           mes_compra,
                                                           valor_parcela,
                                                           valor_manutencao))

    patrimonio_apos_compra = patrimonio_por_tempo[mes_compra-1] - valor_vista
    
    # aporte mensal resultante após a compra:
    aporte_mensal_apos = aporte_mensal_fixo * (aumento_aporte_mensal ** mes_compra) + ganho_problema + valor_parcela

    # tempo desde a compra até o horizonte:
    meses_apos_compra = tempo_horizonte -  mes_compra

    #append do patrimônio por tempo após a dívida:
    patrimonio_por_tempo.extend(eq.patrimonio_puro_por_tempo(patrimonio_apos_compra,
                                                           aporte_mensal_apos,
                                                           rendimento_mensal,
                                                           aumento_aporte_mensal,
                                                           meses_apos_compra))
    
    #plot do patrimônio total por tempo:
    plt.figure(figsize=(21, 9))
    plt.plot(patrimonio_por_tempo, '-.')

    plt.plot(0,
             patrimonio_inicial+aporte_mensal_fixo+valor_parcela+valor_manutencao,
             marker='s',
             color = 'cyan',
             label=f'Patrimônio inicial: R$ {patrimonio_inicial+aporte_mensal_fixo+valor_parcela+valor_manutencao:.0f}')
    
    plt.plot(mes_compra-1,
             patrimonio_por_tempo[mes_compra-1], 
             marker='o', 
             color = 'blue', 
             label=f'Patrimônio total no mês da compra: R$ {patrimonio_por_tempo[mes_compra-1]:.0f}')
    
    plt.plot(mes_compra,
             patrimonio_por_tempo[mes_compra],
             marker='v', 
             color = 'red', 
             label=f'Patrimônio no mês após a compra: R$ {patrimonio_por_tempo[mes_compra]:.0f}')
    
    plt.plot(tempo_horizonte,
             patrimonio_por_tempo[tempo_horizonte],
             marker='^',
             color = 'green', 
             label=f'Patrimônio no Horizonte: R$ {patrimonio_por_tempo[tempo_horizonte]:.0f}')
    
    plt.title('Evolução do Patrimônio Total',fontsize=17)
    plt.xlabel('Meses',fontsize=15)
    plt.ylabel('Patrimônio (R$)',fontsize=15)
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend(fontsize=20)
    plt.grid()
    plt.show()
