
from webbrowser import open as op
from Faz_request import *
from os import system #usado para copiar uma string para a área de transferência
from time import sleep

def Interacao_com_ap(Endereco="Não informado", Preco='Não informado', Titulo='Não informado', infos="Sem infos",
                     Link='Nao informado'):
    ir = int()
    infosadc = ''
    system("cls")
    while True:
        print(' ' * 30 + "\033[1;107m\033[1;30mApartamento escolhido\033[0;0m")
        print('+' + "__" * 41)
        print(f"|Endereço: {Endereco}")
        print(f"|Titulo: {Titulo}")
        print(f"|Preço: {Preco}")
        print(f"|Infos Adicionais:")
        for item in infos:
            print(f"|{item}")
        print('+' + "__" * 41)
        print("\n\n1 - Ir para o site \n2 - Copiar link para a área de transferêrencia \n3 - Voltar")

        ir = int(input("Digite sua escolha: "))
        if ir == 1:
            op(Link) #Abre uma aba no navegador padrão do systema
        elif ir == 2:
            system(f"{'echo '}{Link}| clip") #Copia para a área de transferência
            print("Copiado para a área de transferência")
        elif ir == 3:
            break
        else:
            print("Por favor selecione uma das opções")
        system("cls")


def ImprimirApartamentos(apartamentos, colocar_indicie=True):
    system("cls")
    indicies  = 0
    for aps in apartamentos: #Percorre e imprime todas os itens que recebeu em apartamentos
        if colocar_indicie:
            aps.append(indicies)
            indicies += 1
        print(f"+_________________________________________________________________________________________________")
        print(f"|Id: {aps[5]}")
        print(f"|Titulo: {aps[1]}")
        print(f"|Endereço: {aps[0]}")
        print(f"|Preço: {aps[2]}")
        print(f"+_________________________________________________________________________________________________")

    return apartamentos


def filtrarProximidade():
    """
    Um menu com opções de filtro por bairro ou região
    :return Retornará uma lista a qual o seu primeiro valor sera a escolha (Região ou Bairro) e o segundo valor
    a o filtro:
    """

    querfiltrolocalidade = str(input("Dejesa filtro de localidade (S/N): "))
    if querfiltrolocalidade in "Ss":

        while True:
            system("cls")
            print("Selecionar por:")
            print("1 - Região")
            print("2 - Bairro")
            regiao_bairro = int(input("Digite usa escolha: "))
            if regiao_bairro == 1:
                system("cls")
                infos = InfosCG()
                while True:
                    for indicie, regiao in enumerate(infos.regioes): #Para printar as regiões
                        print(f"{indicie} - {regiao}")

                    try:#Caso o usuário não digite um número inteiro
                        regiao = int(input("Digite o id da região: "))
                    except ValueError:
                        print("Valor inválido!")
                    else:

                        if regiao < 0 or regiao > 4:
                            print("Valor inválido")
                        else:
                            return ["Região", infos.regioes[regiao]]

            elif regiao_bairro == 2:
                digitar = str(input("Deseja digitar o bairro (S/N): "))
                infos = InfosCG() #Nesse objeto contém algumas intâncias sobre os bairros e as regiões
                if digitar in "Ss":
                    while True:
                        system("cls")
                        digitar = str(input("Digite o bairro: "))
                        #Verifica se o bairro esta na lista, caso digite o nome errado o bairro não sera encontrado
                        #Resolvi fazer tudo em um if statment so para tentar economizar espaço
                        if digitar in infos.bairros_CG["Zona Norte"] or digitar in infos.bairros_CG["Zona Sul"] or\
                                digitar in infos.bairros_CG["Zona Leste"] or digitar in infos.bairros_CG["Zona Oeste"] or\
                                digitar in infos.bairros_CG["Distritos"]:
                            print("Bairro Existente!")
                            return ["Bairro", digitar]
                        else:
                            print("Bairro não encontrado!")
                            #Para acabar não ficando na chatisse de errar o nome do bairro, aqui o usuário tera a oportunidade de mudar de escolha
                            digitar = str(input("Deseja continuar? (S/N)"))
                            if digitar in "Ss":
                                continue
                            else:
                                break
                else:

                    while True:
                        system("cls")
                        print("Bairro")


                        for indicie, bairros in enumerate(infos.bairros_lista):
                            print(f"{indicie} - {bairros}")
                        try:#trantamenteo de erro para se caso coloque um valor diferente de um inteiro
                            escolha_por_bairro = int(input("Digite o indicie do bairro: "))
                        except ValueError:
                            print("Por favor digite um valor númerico!")
                        else:
                            if escolha_por_bairro > infos.total_bairros or escolha_por_bairro < 0:
                                print("Por favor Digite um valor válido!")
                            else:
                                return ["Bairro", infos.bairros_lista[escolha_por_bairro]]
            else:
                print("Porfavor selecione uma das opções!")
    else:
        return ["Não informado", "Não informado"]


#Inicializando os objetos
print("Inicializando objetos...")
olx = Olx()
Viva = VivaReal()
system("cls")

sites = ["Olx", "Viva Real"]
tirar_aviso = 0
choice_ = int()
paginas = list()
comeco = int()

while True:
    print("Raspagem de dados de sites de apartamentos")
    print("1 - Para extrair os dados")
    print("2 - Outras Opções")
    print("3 - Sair")
    try:
        comeco = int(input("Digite sua escolha: "))
    except ValueError():
        print("Ops! digite apenas números.")
    else:
        if comeco == 1:
            while True:
                system("cls")
                try:
                    print("Insira 0 caso não queira filtrar o preço")
                    filtrar = int(input("Preço menor ou igual a: "))
                    proximidade = filtrarProximidade() #Função que ira perguntar ao usuário e retornar um lista com alguns filtros

                except ValueError:
                    print("Porfavor digite um valore válido!")
                    sleep(2)
                else:
                    print("Incializando variáveis...")
                    viva_real = VivaReal()
                    olx_variavel = Olx()
                    sleep(1)
                    print("Começando raspagem...")
                    sleep(1)
                    Alguns_apartamentos = viva_real.variasPaginas(5, filtrar, proximidade[0], proximidade[1])
                    Alguns_apartamentos += olx_variavel.variasPaginsa(5, filtrar, proximidade[0], proximidade[1])
                    if len(Alguns_apartamentos) == 0:
                        print("Nenhum apartamento encontrado")
                        system("pause")
                    else:
                        Alguns_apartamentos = ImprimirApartamentos(Alguns_apartamentos)

                        while True:
                            try:
                                id = int(input("Digite o Id do apartamento desejado: "))
                            except ValueError:
                                print("Digite um valor válido")
                            else:

                                if id >= len(Alguns_apartamentos) or id < 0:
                                    print("Nenhum id correspondente!")
                                    system("pause")
                                    continue
                                else:

                                    for iten in Alguns_apartamentos:

                                        if iten[5] == id:
                                            info_AD = iten[3].split(" | ")
                                            Interacao_com_ap(Endereco=iten[0], Titulo=iten[1], Preco=iten[2],
                                                             infos=info_AD, Link=iten[4])
                                            break
                                        else:
                                            continue
                                    cont = str(input("Deseja continuar (S/N): "))
                                    if cont in "Nn":
                                        system("cls")
                                        break
                                    else:
                                        ImprimirApartamentos(Alguns_apartamentos, False)
                            break



        elif comeco == 2:
            system("cls")
            while True:
                print("Sites de condiminio em Campina Grande")
                print("Digite o site o qual deseja fazer uma raspagem de preço")
                for i, site in enumerate(sites):
                    print(f"{i + 1} - {site}")
                print("4 - Sobre")
                print("5 - Sair")
                escolha = int(input("Digite sua escolha: "))

                if escolha == 1:  # Área OLX
                    system("cls")

                    quant_paginas = int(input("Digite a quantidade de páginas que deseja fazer a raspagem: "))
                    print("Digite 0 para não colocar um filtro")
                    filtro = int(input("Preço menor que: "))
                    proximidade = filtrarProximidade()
                    try:
                        Paginas = olx.variasPaginsa(paginas=quant_paginas, filtro=filtro, regiao_ou_bairro=proximidade[0],
                                                    regiao_bairro=proximidade[1])
                    except ConnectionError:
                        print("Ocorreu um erro na requisição da página")
                    else:

                        while True:

                            if len(Paginas) == 0: #Caso não seja retornado nenhum apartamento
                                print("Não foi encontrado nenhum apartamento!")
                                print("Vefique se não esta colocando nenhum filtro errado!")
                                system("pause")
                                break
                            else:

                                Paginas = ImprimirApartamentos(Paginas)
                                try:
                                    apescolhido_id = int(input("Digite o id do apartamento o qual deseja visualizar melhor: "))
                                except ValueError():
                                    print("Por favor digite um valor númerico")
                                    system("pause")
                                    system("cls")
                                    continue #Caso digite um valor incorreto ele iniciará outra vez no laço
                                else:

                                    if apescolhido_id >= len(Paginas) or apescolhido_id < 0:
                                        print("Id incorreto")
                                        system("pause")
                                        continue
                                    else:

                                        apescolhido = list()

                                        for ap in Paginas:#Percorre a lista Paginas a procura do item o qual possui  o id escolhido

                                            if ap[5] == apescolhido_id:
                                                apescolhido = ap[::]

                                        #Eu não filtrei os quarto, metros e vagas, por isso precisei fazer o split para
                                        #coloca-los nas infos adicionasi

                                        infos_adicionais  = apescolhido[3].split(" | ")
                                        system("cls")
                                        Interacao_com_ap(Endereco=apescolhido[0], Titulo=apescolhido[1], Preco=apescolhido[2],
                                                         infos=infos_adicionais, Link=apescolhido[4])
                                        continuar = str(input("Deseja Continuar? (S|N)"))
                                        if continuar in "Nn":
                                            system("cls")
                                            break
                                        else:
                                            system("cls")
                                            continue




                elif escolha == 2:  # Área Viva real
                    system("cls")  # Para limpar a tela, no pycharm não funciona porém no terminal normal do windows sim
                    # Usando a bibliotea para fazer a requisição de uma ou multiplas páginas
                    choice_ = int(input("Digite a quantidade de páginas as quais deseja fazer a raspagem: "))
                    if tirar_aviso == 0:
                        print("Caso não queira nenhum dos filtros basta digitar 0 quando eles forem requisitados")
                    filtrom = int(input("Preço menor que: "))  # Variável para filtrar valores que sejam menor que
                    filtrolocalidade = filtrarProximidade()


                    paginas = Viva.variasPaginas(quantidade_pag=choice_, caso_filtro=filtrom, regiao_ou_bairro=filtrolocalidade[0],
                                                 regiao_bairro=filtrolocalidade[1])
                    # Interação do usuáriol com os valores
                    continuar = str()
                    if len(paginas) == 0:
                        print("Nenhum apartamento encontrado")
                    else:
                        while True:  # Depois dos apartamentos serem mostrados chega a parte de interação com eles
                            system("cls")
                            if len(paginas) == 0:
                                print("Não foi encontrado nenhum apartamento!")
                                print("Vefique se não esta colocando nenhum filtro errado!")
                                system("pause")
                            else:
                                paginas = ImprimirApartamentos(paginas)
                                try: #Caso o usuário digite um valor diferente de um número inteiro
                                    choice = int(input("Digite o id do condomínio interessado: "))
                                except ValueError:
                                    print("Por favor digite um valor válido")
                                else:
                                    if choice >= len(paginas) or choice < 0: #Caso digite um id que seja inválido
                                        print("Id inválido")
                                        system("pause")
                                    else:
                                        percorrendo = 0
                                        escolhido = list()
                                        for iten in paginas:  # Percorre a lista para encontrar o valor

                                            if choice == iten[5]:
                                                escolhido = iten[::]
                                                break
                                            else:
                                                percorrendo += 1
                                        Interacao_com_ap(Endereco=escolhido[0], Titulo=escolhido[1],
                                                         Preco=escolhido[2], infos=escolhido[3], Link=escolhido[4])

                                        continuar = str(input("Deseja continuar? (S/N): "))
                                        if continuar in "Ss":
                                            continue
                                        else:
                                            system("cls")  # limpa a tela do terminal
                                            break


                elif escolha == 4:
                    system("cls")
                    print("Detalhes do programa: \n")
                    print("-O preço do condominio pode não está incluido, por isso quando se interesar por um apartamento,")
                    print("escolha ser endereçado, ou copiar o link para a área de trasferência para verificar cada detalhe.")
                    print("-Em alguns casos pode ser que o endereço seja apenas Campina Grande, isso acontece por que essa")
                    print("é a única informação do endereço dada pelo proprietário.")
                    print("-Por detalhes do site o ZapImoveis não teve como extrair com precisão os seus elementos, por isso ele")
                    print("contém poucas informações, inclundo a falta do link para acessar apartamento, por esse motivo ele será removido")
                    print("do programa final, mas ficará no código ou micelania do programa. ")
                    print("No caso esse problema decorre por que a tag que usalmente serve como indentificão ")
                    print("do link não está presente nos documentos html do site, pois ela foi subtituida por um evento ajax.")
                    print("-Pode acontecer de alguns apartamentos se repetirem, isso ocorre por que essas informações estão sendo")
                    print("tiradas de três sites diferentes. (Provavelmente se essa for a versão final esse não será mais um problema)")
                    print("-Caso você coloque mais páginas do que há no site, retornará o restate só que com erro ")
                    print("mas ainda assim os que forrem possível serão mostrados e esses erros ignorados pelo programa")
                    print("-Para acesar mais apartamentos a melhor escolha seria ir na parte de opções e raspar")
                    print("Um site de cada vez, pois no primeiro menu irá procurar só nas primeiras páginas de cada um")
                    print("-Caso não ache o bairro que estaá procurando, digite o nome dele quando o programa pergutar")
                    print("se você deseja digitar.")
                    print("\n\n\nDesenvolvido por Dov: Caio Jhonatan Alves Pereira")
                    print("\n\n\nLink do github: https://github.com/DovCaio")
                    print("\n\n ")
                    system("pause")
                else:
                    system("cls")
                    break
                tirar_aviso = 1
                system("cls")
        elif comeco == 3:
            print("Saindo...")
            sleep(2)
            break
        else:
            print("Por favor selecione uma das opções!")
            sleep(2)
            system("cls")
