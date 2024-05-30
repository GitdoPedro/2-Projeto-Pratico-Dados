import googlemaps

def formatar_reais(x):
    if isinstance(x, (int, float)):
        return f'R$ {x:,.2f}'
    return x

def obter_cep(rua, bairro, cidade, gmaps):
    address = f"{rua}, 2, {bairro}, {cidade}"
    geocode_result = gmaps.geocode(address)
    
    if geocode_result:
        for result in geocode_result:
            for component in result['address_components']:
                if 'postal_code' in component['types']:
                    return component['long_name']
    return 'CEP não encontrado'

def substituir_cep_nao_encontrado(linha, df):
    if linha['cep'] == 'CEP não encontrado':
        mesmo_bairro = df[(df['district'] == linha['district']) & (df['cep'] != 'CEP não encontrado')]
        if not mesmo_bairro.empty:
            return mesmo_bairro['cep'].iloc[0]
    return linha['cep']

def ajustar_cep(cep):
    if len(cep) == 4:
        return f"0{cep}-000"
    return cep

def classificar_zona(cep):
    cep = cep.replace('-', '')
    if len(cep) == 8:
        prefixo = int(cep[:5])
        if 1000 <= prefixo <= 1599:
            return 'Central'
        elif 2000 <= prefixo <= 2999:
            return 'Norte'
        elif (3000 <= prefixo <= 3999) or (8000 <= prefixo <= 8499):
            return 'Leste'
        elif 4000 <= prefixo <= 4999:
            return 'Sul'
        elif 5000 <= prefixo <= 5899:
            return 'Oeste'
        elif 6000 <= prefixo <= 9999:
            return 'Grande SP'
    return 'Central'
