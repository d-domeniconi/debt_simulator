import matplotlib.pyplot as plt
from . import loan

def anual_para_mensal(taxa_anual):
    return (taxa_anual ** (1/12))

def _patrimonio_acumulado_de_aportes(aporte_mensal, 
                                    rendimento_mensal, 
                                    aumento_aporte_mensal, 
                                    meses):
    return aporte_mensal * ( (rendimento_mensal ** (meses + 1)) - (aumento_aporte_mensal ** (meses + 1)) ) / (rendimento_mensal - aumento_aporte_mensal)

def patrimonio_puro(patrimonio_inicial, 
                    aporte_mensal, 
                    rendimento_mensal, 
                    aumento_aporte_mensal, 
                    meses):

    rendimento_patrimonio_inicial = patrimonio_inicial * (rendimento_mensal ** meses)

    patrimônio_resultante_de_aportes = _patrimonio_acumulado_de_aportes(aporte_mensal, 
                                                                       rendimento_mensal, 
                                                                       aumento_aporte_mensal, 
                                                                       meses)

    return rendimento_patrimonio_inicial + patrimônio_resultante_de_aportes

def patrimonio_puro_por_tempo(patrimonio_inicial, 
                              aporte_mensal, 
                              rendimento_mensal, 
                              aumento_aporte_mensal, 
                              meses):
    patrimonio_por_mes = []

    for mes in range(meses + 1):
        patrimonio_atual = patrimonio_puro(patrimonio_inicial, 
                                           aporte_mensal, 
                                           rendimento_mensal, 
                                           aumento_aporte_mensal, 
                                           mes)
        patrimonio_por_mes.append(patrimonio_atual)

    return patrimonio_por_mes

def patrimonio_antes_por_tempo(patrimonio_inicial, 
                               aporte_mensal_fixo, 
                               rendimento_mensal, 
                               aumento_aporte_mensal, 
                               meses,
                               valor_parcela,
                               valor_manutencao):
    patrimonio_por_mes = []

    aporte_efetivo = aporte_mensal_fixo + valor_parcela + valor_manutencao

    for mes in range(meses):
        patrimonio_atual = patrimonio_puro(patrimonio_inicial, 
                                           aporte_efetivo, 
                                           rendimento_mensal, 
                                           aumento_aporte_mensal, 
                                           mes)
        patrimonio_por_mes.append(patrimonio_atual)

    return patrimonio_por_mes

def patrimonio_durante(patrimonio_inicial, 
                       aporte_mensal_fixo, 
                       rendimento_mensal, 
                       aumento_aporte_mensal, 
                       mes_compra,
                       valor_vista, 
                       valor_entrada, 
                       valor_parcela, 
                       juros_mensais,
                       valor_manutencao, 
                       ganho_problema,
                       meses,
                       info=False):
    aporte_efetivo = aporte_mensal_fixo + valor_parcela + valor_manutencao

    if meses == -1:
        meses = loan.encontrar_numero_parcelas(loan.tabela_comparativa(valor_vista, 
                                                                       valor_entrada, 
                                                                       juros_mensais), 
                                                                       valor_parcela)

    novo_patrimonio_inicial = patrimonio_puro(patrimonio_inicial, 
                                              aporte_efetivo, 
                                              rendimento_mensal, 
                                              aumento_aporte_mensal, 
                                              mes_compra-1) - valor_entrada
    
    if info==True:
        print(f"Patrimônio antes de comprar o Bem: R$ {patrimonio_puro(patrimonio_inicial, 
                                                                       aporte_efetivo, 
                                                                       rendimento_mensal, 
                                                                       aumento_aporte_mensal, 
                                                                       mes_compra-1):.2f}")
        print(f"Patrimônio após comprar o Bem: R$ {novo_patrimonio_inicial:.2f}")

    return patrimonio_puro(novo_patrimonio_inicial, 
                           aporte_mensal_fixo * (aumento_aporte_mensal ** mes_compra) + ganho_problema, 
                           rendimento_mensal, 
                           aumento_aporte_mensal, 
                           meses)

def patrimonio_durante_por_tempo(patrimonio_inicial, 
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
                       ):
    patrimonio_por_mes = []

    for mes in range(loan.encontrar_numero_parcelas(loan.tabela_comparativa(valor_vista, 
                                                                  valor_entrada, 
                                                                  juros_mensais), 
                                                                  valor_parcela) + 1):
        patrimonio_atual = patrimonio_durante(patrimonio_inicial, 
                       aporte_mensal_fixo, 
                       rendimento_mensal, 
                       aumento_aporte_mensal, 
                       mes_compra,
                       valor_vista, 
                       valor_entrada, 
                       valor_parcela, 
                       juros_mensais,
                       valor_manutencao, 
                       ganho_problema,
                       mes,
                       info=False)
        
        patrimonio_por_mes.append(patrimonio_atual)

    return patrimonio_por_mes

def patrimonio_apos(patrimonio_inicial, 
                    aporte_mensal_fixo, 
                    rendimento_mensal, 
                    aumento_aporte_mensal, 
                    meses_quitados,
                    valor_vista, 
                    valor_entrada, 
                    valor_parcela, 
                    valor_manutencao, 
                    ganho_problema, 
                    mes_compra, 
                    juros_mensais):
    
     

    meses_pagando = loan.encontrar_numero_parcelas(loan.tabela_comparativa(valor_vista, 
                                                                           valor_entrada, 
                                                                           juros_mensais), 
                                                                           valor_parcela)
    
    novo_patrimonio_inicial = patrimonio_durante(patrimonio_inicial, 
                                                 aporte_mensal_fixo, 
                                                 rendimento_mensal, 
                                                 aumento_aporte_mensal, 
                                                 mes_compra,
                                                 valor_vista, 
                                                 valor_entrada, 
                                                 valor_parcela, 
                                                 juros_mensais,
                                                 valor_manutencao, 
                                                 ganho_problema,
                                                 -1)

    return patrimonio_puro(novo_patrimonio_inicial,
                           (aporte_mensal_fixo * (aumento_aporte_mensal ** (mes_compra+meses_pagando)) + ganho_problema + valor_parcela), 
                           rendimento_mensal, 
                           aumento_aporte_mensal, 
                           meses_quitados)

def patrimonio_apos_por_tempo(patrimonio_inicial, 
                              aporte_mensal_fixo, 
                              rendimento_mensal, 
                              aumento_aporte_mensal, 
                              meses_quitados,
                              valor_vista, 
                              valor_entrada, 
                              valor_parcela, 
                              valor_manutencao, 
                              ganho_problema, 
                              mes_compra, 
                              juros_mensais):
    
    patrimonio_por_mes = []

    for mes in range(meses_quitados + 1):
        patrimonio_atual = patrimonio_apos(patrimonio_inicial, 
                                           aporte_mensal_fixo, 
                                           rendimento_mensal, 
                                           aumento_aporte_mensal, 
                                           mes,
                                           valor_vista, 
                                           valor_entrada, 
                                           valor_parcela, 
                                           valor_manutencao, 
                                           ganho_problema, 
                                           mes_compra, 
                                           juros_mensais)
        patrimonio_por_mes.append(patrimonio_atual)

    return patrimonio_por_mes

def patrimonio_total_com_endividamento(patrimonio_inicial, 
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
                                       juros_mensais, 
                                       taxa_preciacao_Bem):
    

    meses_pagando = loan.encontrar_numero_parcelas(loan.tabela_comparativa(valor_vista, 
                                                                           valor_entrada, 
                                                                           juros_mensais), 
                                                                           valor_parcela)

    meses_quitados = tempo_horizonte - mes_compra - meses_pagando

    #valor do bem adicionado ao patrimonio total:
    contribuicao_bem = valor_vista * (taxa_preciacao_Bem ** (tempo_horizonte - mes_compra))
                                                             
    #print(f"Contribuição do bem: {contribuicao_bem}")

    if meses_quitados >= 0:
        return patrimonio_apos(patrimonio_inicial, 
                               aporte_mensal_fixo, 
                               rendimento_mensal, 
                               aumento_aporte_mensal, 
                               meses_quitados,
                               valor_vista, 
                               valor_entrada, 
                               valor_parcela, 
                               valor_manutencao, 
                               ganho_problema, 
                               mes_compra, 
                               juros_mensais) + contribuicao_bem
    else:
        return patrimonio_durante(patrimonio_inicial, 
                                 aporte_mensal_fixo, 
                                 rendimento_mensal, 
                                 aumento_aporte_mensal, 
                                 mes_compra,
                                 valor_vista, 
                                 valor_entrada, 
                                 valor_parcela, 
                                 juros_mensais,
                                 valor_manutencao, 
                                 ganho_problema,
                                 tempo_horizonte-mes_compra) + contribuicao_bem

def patrimonio_com_endividamento_defeito_domínio(patrimonio_inicial, 
                                                 aporte_mensal_fixo, 
                                                 rendimento_mensal, 
                                                 aumento_aporte_mensal, 
                                                 meses, 
                                                 mes_endividamento, 
                                                 valor_parcela, 
                                                 valor_manutencao, 
                                                 valor_entrada, 
                                                 valor_vista,
                                                 juros_mensais ,
                                                 ganho_problema ,
                                                 taxa_preciacao_Bem):
    
    aporte_efetivo = aporte_mensal_fixo + valor_parcela + valor_manutencao
    
    # Calcular o patrimônio acumulado até o mês de endividamento:
    patrimonio_ate_endividamento = patrimonio_puro(patrimonio_inicial, 
                                                   aporte_efetivo, 
                                                   rendimento_mensal, 
                                                   aumento_aporte_mensal, 
                                                   mes_endividamento)

    # O patrimônio até aqui será reduzido pelo valor da entrada ao se endividar:
    patrimonio_apos_endividamento = patrimonio_ate_endividamento - valor_entrada

    # O patrimônio restante renderá normalmente até o final do horizonte de tempo:
    patrimonio_apos_endividamento_final = patrimonio_apos_endividamento * (rendimento_mensal ** (meses - mes_endividamento))

    # Calcular o numero de parcelas necessárias para o valor da parcela desejado usando a tabela comparativa:
    numero_parcelas = loan.encontrar_numero_parcelas(loan.tabela_comparativa(valor_vista, 
                                                                   valor_entrada, 
                                                                   juros_mensais), 
                                                                   valor_parcela)

    # Calcular o dinheiro economizado a partir do mês de endividamento, durante o endividamento, considerando o pagamento das parcelas, o valor de manutenção e o ganho do problema:
    economia_durante_endividamento = patrimonio_puro(0,                                                                                                                 # Supondo que o patrimônio inicial seja 0 para calcular apenas a economia durante o endividamento
                                                      (aporte_efetivo * aumento_aporte_mensal ** mes_endividamento + ganho_problema - valor_parcela - valor_manutencao), # Aporte mensal ajustado para o mês de endividamento, considerando o aumento do aporte mensal, o ganho do problema, o valor da parcela e o valor de manutenção
                                                       rendimento_mensal, aumento_aporte_mensal,                                                                        # Rendimento mensal e aumento de aporte mensal permanecem os mesmos durante o endividamento
                                                       numero_parcelas                                                                                                  # Número de parcelas durante o endividamento, que determina por quantos meses esse tipo de economia ocorrerá
                                                       )
    
    # Contribuição ao patrimônio do valor do Bem adquirido, considerando a taxa de apreciação do Bem:
    contribuicao_bem = valor_vista * (taxa_preciacao_Bem ** (meses - mes_endividamento))

    # Calcular o patrimônio acumulado após o pagamento de todas as parcelas, considerando o valor de manutenção e o ganho do problema:
    economia_apos_endividamento = patrimonio_puro(0,                                                                                                                        # Supondo que o patrimônio inicial seja 0 para calcular apenas a economia após o endividamento
                                                      (aporte_efetivo * aumento_aporte_mensal ** (mes_endividamento + numero_parcelas) + ganho_problema - valor_manutencao), # Aporte mensal ajustado para o período após o endividamento, considerando o aumento do aporte mensal, o ganho do problema e o valor de manutenção (sem considerar o valor da parcela, pois já foi pago durante o endividamento)
                                                       rendimento_mensal, aumento_aporte_mensal,                                                                            # Rendimento mensal e aumento de aporte mensal permanecem os mesmos após o endividamento
                                                       (meses - mes_endividamento - numero_parcelas)                                                                        # Número de meses após o endividamento, que determina por quantos meses esse tipo de economia ocorrerá
                                                       )

    # Retornar soma resultante:
    return patrimonio_apos_endividamento_final + economia_durante_endividamento + contribuicao_bem + economia_apos_endividamento

def patrimonio_final_sem_endividamento(patrimonio_inicial,
                                       aporte_mensal_fixo,
                                       rendimento_mensal,
                                       aumento_aporte_mensal,
                                       mes_compra,
                                       valor_vista,
                                       valor_parcela,
                                       ganho_problema,
                                       valor_manutencao,
                                       tempo_horizonte,
                                       preciacao_mensal):
    aporte_efetivo = aporte_mensal_fixo + ganho_problema + valor_manutencao
    
    # acumulo de patrimônio antes de comprar o Bem:
    patrimonio_disponivel_para_compra = patrimonio_puro(patrimonio_inicial, 
                                                        aporte_efetivo, 
                                                        rendimento_mensal, 
                                                        aumento_aporte_mensal, 
                                                        mes_compra-1)
    
    # patrimonio após compra à vista do Bem:
    patrimonio_apos_compra = patrimonio_disponivel_para_compra - valor_vista 

    # aporte mensal resultante após a compra:
    aporte_mensal_apos_compra = aporte_mensal_fixo * (aumento_aporte_mensal ** (mes_compra-1)) + ganho_problema + valor_parcela

    # tempo desde a compra até o horizonte:
    meses_apos_compra = tempo_horizonte -  mes_compra

    # contribuição do Bem:
    contibuicao_Bem = valor_vista * preciacao_mensal ** meses_apos_compra

    # retornando o acumulo de patrimônio após comprar o Bem:
    return patrimonio_puro(patrimonio_apos_compra   ,
                           aporte_mensal_apos_compra,
                           rendimento_mensal        ,
                           aumento_aporte_mensal    ,
                           meses_apos_compra        ) + contibuicao_Bem
