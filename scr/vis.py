import matplotlib.pyplot as plt
from . import loan
from . import equity as eq

def plot_puro(patrimonio_inicial, 
              aporte_mensal, 
              rendimento_mensal, 
              aumento_aporte_mensal, 
              meses):
    patrimonio_por_mes = eq.patrimonio_puro_por_tempo(patrimonio_inicial, 
                                                      aporte_mensal, 
                                                      rendimento_mensal, 
                                                      aumento_aporte_mensal, 
                                                      meses)
    
    for i in range(len(patrimonio_por_mes)):
        patrimonio_por_mes[i] = patrimonio_por_mes[i] / 1000

    plt.figure(figsize=(21, 9))
    plt.plot(patrimonio_por_mes, '-.')

    plt.plot(0,
             patrimonio_por_mes[0],
             marker='s',
             color='blue',
             label=f'Patrimônio inicial: R$ {patrimonio_inicial*1e-3:.0f} mil')
    
    plt.plot(len(patrimonio_por_mes) - 1,
                patrimonio_por_mes[-1],
                marker='^',
                color='green',
                label=f'Final: R$ {patrimonio_por_mes[-1]:.0f} mil')

    plt.title('Evolução do Patrimônio Puro', fontsize=18)
    plt.xlabel('Meses', fontsize=15)
    plt.ylabel('Patrimônio (mil R$)', fontsize=15)
    plt.grid()
    plt.legend(fontsize=15)
    plt.show()

def plot_vantagem_aumento(patrimonio_inicial, 
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
    
    for i in range(len(patrimonio_com_aumento)):
        patrimonio_com_aumento[i] = patrimonio_com_aumento[i] / 1000
        patrimonio_sem_aumento[i] = patrimonio_sem_aumento[i] / 1000

    plt.figure(figsize=(21, 9))

    plt.plot(patrimonio_com_aumento, '-.', 
             label='Com Aumento de Aporte Mensal')
    
    plt.plot(patrimonio_sem_aumento, '--', 
             label='Sem Aumento de Aporte Mensal')
    
    #inicial
    plt.plot(0,
             patrimonio_com_aumento[0],
             marker='s',
             color='blue',
             label=f'Patrimônio inicial: R$ {patrimonio_inicial*1e-3:.0f} mil')
    
    #final com aumento
    plt.plot(len(patrimonio_com_aumento) - 1,
             patrimonio_com_aumento[-1],
             marker='^',
             color='green',
             label=f'Final com aumento: R$ {patrimonio_com_aumento[-1]:.0f} mil')

    #final sem aumento
    plt.plot(len(patrimonio_sem_aumento) - 1,
             patrimonio_sem_aumento[-1],
             marker='^',
             color='red',
             label=f'Final sem aumento: R$ {patrimonio_sem_aumento[-1]:.0f} mil')

    plt.title('Comparação do Patrimônio com e sem Aumento de Aporte Mensal', fontsize=18)
    plt.xlabel('Meses', fontsize=15)
    plt.ylabel('Patrimônio (mil R$)', fontsize=15)
    plt.legend(fontsize=15)
    plt.grid()
    plt.show()

def plot_in_debt_buy(patrimonio_inicial, 
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
        serie_durante[:] +
        serie_apos[:]
    )
    
    mes_fim_divida = mes_compra + num_parcelas
    mes_final = len(patrimonio_por_tempo)

    if mes_fim_divida > tempo_horizonte:
        mes_fim_divida = tempo_horizonte    

    if mes_final > tempo_horizonte:
        mes_final = tempo_horizonte

    for i in range(len(patrimonio_por_tempo)):
        patrimonio_por_tempo[i] = patrimonio_por_tempo[i] / 1000

    plt.figure(figsize=(21,9))
    plt.plot(patrimonio_por_tempo[0:mes_final+1], '-.')

    # inicial
    plt.plot(0,
                patrimonio_por_tempo[0],
                marker='s',
                color='blue',
                label=f'Patrimônio inicial: R$ {patrimonio_inicial*1e-3:.0f} mil')

    # compra
    plt.plot(mes_compra-1,
                patrimonio_por_tempo[mes_compra-1],
                marker='o',
                color='blue',
                label=f'Total no mês da compra: R$ {patrimonio_por_tempo[mes_compra-1]:.0f} mil')
    
    # começo da dívida
    plt.plot(mes_compra,
                patrimonio_por_tempo[mes_compra],
                marker='v',
                color='red',
                label=f'Começo da dívida: R$ {patrimonio_por_tempo[mes_compra]:.0f} mil')

    # fim da dívida
    plt.plot(mes_fim_divida,
                patrimonio_por_tempo[mes_fim_divida],
                marker='v',
                color='red',
                label=f'Fim da dívida: R$ {patrimonio_por_tempo[mes_fim_divida-1]:.0f} mil')

    # final
    plt.plot(mes_final,
                patrimonio_por_tempo[mes_final],
                marker='^',
                color='green',
                label=f'Final: R$ {patrimonio_por_tempo[mes_final]:.0f} mil')

    # layout
    plt.title('Evolução do Patrimônio com Dívida',fontsize=17)
    plt.xlabel('Meses',fontsize=15)
    plt.ylabel('Patrimônio (mil R$)',fontsize=15)
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend(fontsize=20)
    plt.grid()
    plt.show()

def plot_in_full_buy(patrimonio_inicial, 
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
    
    for i in range(len(patrimonio_por_tempo)):
        patrimonio_por_tempo[i] = patrimonio_por_tempo[i] / 1000
    
    #plot do patrimônio total por tempo:
    plt.figure(figsize=(21, 9))
    plt.plot(patrimonio_por_tempo, '-.')

    plt.plot(0,
             (patrimonio_inicial+aporte_mensal_fixo+valor_parcela+valor_manutencao)*1e-3,
             marker='s',
             color = 'cyan',
             label=f'Patrimônio inicial: R$ {patrimonio_inicial*1e-3:.0f} mil')
    
    plt.plot(mes_compra-1,
             patrimonio_por_tempo[mes_compra-1], 
             marker='o', 
             color = 'blue', 
             label=f'Total no mês da compra: R$ {patrimonio_por_tempo[mes_compra-1]:.0f} mil')
    
    plt.plot(mes_compra,
             patrimonio_por_tempo[mes_compra],
             marker='v', 
             color = 'red', 
             label=f'No mês após a compra: R$ {patrimonio_por_tempo[mes_compra]:.0f} mil')
    
    plt.plot(tempo_horizonte,
             patrimonio_por_tempo[tempo_horizonte],
             marker='^',
             color = 'green', 
             label=f'No Horizonte: R$ {patrimonio_por_tempo[tempo_horizonte]:.0f} mil')
    
    for i in range(len(patrimonio_por_tempo)):
        patrimonio_por_tempo[i] = patrimonio_por_tempo[i] / 1000

    plt.title('Evolução do Patrimônio sem Dívida',fontsize=17)
    plt.xlabel('Meses',fontsize=15)
    plt.ylabel('Patrimônio (mil R$)',fontsize=15)
    plt.ticklabel_format(style='plain', axis='y')
    plt.legend(fontsize=20)
    plt.grid()
    plt.show()
