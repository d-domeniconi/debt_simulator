import matplotlib.pyplot as plt

def valor_parcela(valor_vista, 
                  valor_entrada, 
                  juros_mensais, 
                  numero_parcelas):
    parcela = (valor_vista - valor_entrada) * (1 - juros_mensais) / (juros_mensais ** ((-1) * numero_parcelas) - 1)
    if numero_parcelas == 0:
        parcela = valor_vista - valor_entrada
    return parcela

def tabela_comparativa(valor_vista, 
                       valor_entrada, 
                       juros_mensais, 
                       max_parcelas = 1000):
    tabela = []
    for numero_parcelas in range(0, max_parcelas + 1):
        if numero_parcelas == 0:
            valor_parcela_atual = valor_vista - valor_entrada
        else:
            valor_parcela_atual = valor_parcela(valor_vista, valor_entrada, juros_mensais, numero_parcelas)
        tabela.append((numero_parcelas, valor_parcela_atual))
    return tabela

def encontrar_numero_parcelas(tabela, valor_parcela_desejado):
    
    for numero_parcelas, valor_parcela_atual in tabela:
        
        if numero_parcelas > 420:
            break  # agora faz sentido usar break

        if valor_parcela_atual <= valor_parcela_desejado:
            return numero_parcelas

    # Se chegou aqui, nem 420 meses foi suficiente
    valor_420 = next((v for n, v in tabela if n == 420), None)

    if valor_420 is not None:
        print('Número de parcelas necessário passou o limite de 420 meses (30 anos).')
        print(f'Valor mínimo da parcela: R$ {(valor_420+0.00001*valor_420):.2f}')

    return None