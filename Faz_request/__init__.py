from requests import get
from bs4 import BeautifulSoup
from time import sleep


#Essa variável, servirá para filtrar a localização dos apartamentos
class InfosCG:
    """
    Para trasferrir essas informaçções para outros modolos
    """
    def __init__(self):
        #Instância com os bairros por região
        self.bairros_CG = {"Zona Norte": ["Alto Branco", "Araxá", "Bairro das Nações", "Conceição", "Cuités",
            "Jardim Continental", "Jardim Tavares", "Jeremias", "Lauritzen", "Louzeiro", "Monte Santo", "Palmeira"],
              "Zona Sul": ["Acácio Figueiredo", "Bairro das Cidades", "Catolé", "Catolé de Zé Ferreira",
            "Conjunto Cinza", "Cruzeiro", "Distrito Industrial", "Estação Velha", "Itararé", "Jardim Borborema",
            "Jardim Paulistano", "Liberdade", "Novo Cruzeiro", "Palmeira Imperial", "Pres. Médici Quarenta",
            "Ressurreição", "Rocha Cavalcante", "Rosa Cruz", "Sandra Cavalcante", "São José", "Tambor", "Três Irmãs",
            "Velame" ],
              "Zona Leste": ["Belo Monte", "Cachoeira",  "Castelo Branco",  "Glória", "José Pinheiro", "Mirante",
            "Monte Castelo", "Nova Brasília", "Santo Antônio", "Vila Cabral" ],
              "Zona Oeste": ["Bela Vista", "Bodocongó", "Centenário", "Dinamérica", "Jardim Verdejante", "Malvinas",
            "Mutirão do Serrotão", "Novo Bodocongó", "Pedregal", "Prata", "Ramadinha", "Santa Cruz", "Santa Rosa",
            "São Januário", "Serrotão", "Universitário" ],
              "Distritos": ["Catolé", "Galante", "Marinho", "Santa Terezinha", "São José da Mata"]}
        #Instância da quantidade de bairrros
        self.zona_norte_quant = len(self.bairros_CG["Zona Norte"])
        self.zona_sul_quant = len(self.bairros_CG["Zona Sul"])
        self.zona_leste_quant = len(self.bairros_CG["Zona Leste"])
        self.zona_oeste_quant = len(self.bairros_CG["Zona Oeste"])
        self.distritos_quant = len(self.bairros_CG["Distritos"])
        self.total_bairros = self.zona_norte_quant + self.zona_sul_quant + self.zona_leste_quant + self.zona_oeste_quant + self.distritos_quant


        self.regioes = ["Zona Norte", "Zona Sul", "Zona Leste", "Zona Oeste", "Distritos"]

        bairros_numa_lista = list() #auxiliar
        for regi in self.regioes:#Coloca dentro de uma lista todos os bairros
            bairros_numa_lista += self.bairros_CG[f"{regi}"]
        self.bairros_lista = bairros_numa_lista[::]



def tirarAcentos(palavra):
    letras_acentuadas = ["á", "â", "ã", "é", "ê", "í", "ó", "õ", "ú"]

    palavra_sem_acento = ''
    for caracter in range(0, len(palavra)): #Percorre os caracteres da palavra recebida
        for char in range(0, len(letras_acentuadas)):#Percorre a lista
            if palavra[caracter].lower() == letras_acentuadas[char]:#Caso o caracter da vez seja acentuado ele entrará dentro de uma sequência de if statment que verificará qual caracter acentuado ele recebeu dependendo do valor de char
                if char < 3:
                    palavra_sem_acento += 'a'
                    break
                elif char < 5:
                    palavra_sem_acento += 'e'
                    break
                elif char < 6:
                    palavra_sem_acento += 'i'
                    break
                elif char < 8:
                    palavra_sem_acento += 'o'
                    break
                else:
                    palavra_sem_acento += 'u'
                    break
            else: #Caso o caracter da vez não seja acentuado e estaja no ultimo looping ele irá colocar  carcter, uma vez que ele não é acentuado
                if char == 8:
                    palavra_sem_acento += palavra[caracter]
    return palavra_sem_acento



def filtrarLocalizacao(Endereco, regiao_bairro="Não informado", regiao_ou_bairro="Não informado"):

    if regiao_ou_bairro == "Região":  # Caso seja filtrado por região

        for valores in InfosCG().bairros_CG[regiao_bairro]:  # Precorre todos os bairros da região em questão, chamando as informações contidas no objeto InfosCG
            if tirarAcentos(valores) in tirarAcentos(Endereco):  # Caso o algum dos bairros da região tenha algum elemento igual ao endereço do apartamento
                return True

    elif regiao_ou_bairro == "Bairro":

        if tirarAcentos(regiao_bairro) in tirarAcentos(Endereco):  # Verifica se o bairro em questão é o mesmo que ele recebeu como parâmetro
            return True
    else:
        return False




class Olx():
    def __init__(self):
        # Quando colocamos para o próximo elemento na url é adicionado o ?o= e em seguida o numero da página ex: ?o=2 concatenado com a url vai para a segunda pagina
        self.olx_url = "https://pb.olx.com.br/paraiba/campina-grande-guarabira-e-regiao/campina-grande/imoveis/aluguel"


    def carregar(self, pag=0, filtro=0, regiao_ou_bairro="Não informado", regiao_bairro="Não informado"):

        #Quando recebe um valor em pag entao ele vai formatar a string de forma que ela seja a página em questão
        passeguidas = self.olx_url + f"{'' if pag == 0 else f'?o={pag}'}"

        print(f"\033[1;107m\033[1;30m  CONECTANDO A {passeguidas} \033[0;0m ")

        #Quando estava fazendo o request estava dando um erro 403, isso acontece, pois esta desabilitado a requisição
        #de qualquer coisa que não seja o navegador, para solucionar isso preciso dar outro argumento para o parâmetro
        #do get essse argumento é um dicionário que contém alguns valores que vão representar o navegador


        fingir_navegador =  {"User-Agent": "Mozila/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/50.0.2661.75 Safari/537.36",
                             "X-Requested-With": 'XMLHttpRequest'}


        try:
            olx = get(passeguidas, headers=fingir_navegador)
        except ConnectionAbortedError: #Só que coloqui de uma forma muito genêrica
            print(f"\033[1;31mConecxão cancelado com {passeguidas}\033[0;0m")
        except ConnectionRefusedError:
            print(f"\033[1;31mConecxão recusada com {passeguidas}\033[0;0m")
        except:
            print(f"\033[1;31mErro na conxão com {passeguidas}\033[0;0m")
        else:

            olx_rap = BeautifulSoup(olx.text, "html.parser")



            # Fazendo a extração
            Endereco = olx_rap.find_all("span", class_="sc-7l84qu-1 ciykCV sc-ifAKCX dpURtf")
            Titulos = olx_rap.find_all("h2", class_="sc-1mbetcw-0 fKteoJ sc-ifAKCX jyXVpA")
            Precos = olx_rap.find_all("span", class_="sc-ifAKCX eoKYee")
            Infos_adc = olx_rap.find_all("span", class_="sc-1j5op1p-0 lnqdIU sc-ifAKCX eLPYJb")
            Link = olx_rap.find_all('a', class_="fnmrjs-0 fyjObc")


            precos = str()
            preco = str()
            tabela = list()


            #Quando uma das listas é maior que as outras, é possível que aconteça um erro

            for iten in range(0, len(Titulos)):

                #Esse primeiro if statment acontecerá quando não for informado o filtro de preço menor que,
                # mais for informado a localidade do apartamento
                if filtro == 0: #Sem filtro de preco

                    if regiao_bairro != "Não informado": #Com filtro de localização

                        if filtrarLocalizacao(Endereco[iten].text, regiao_bairro, regiao_ou_bairro): #Essa função
                            # retonr True caso os argumentos dados estejam atendam o filtro e false se não
                            tabela.append([Endereco[iten].text, Titulos[iten].text,
                                   Precos[iten].text, Infos_adc[iten].text, Link[iten].get("href")])



                    else:#Sem filtro de preco, e sem filtro de localização

                        tabela.append([Endereco[iten].text, Titulos[iten].text,
                                   Precos[iten].text, Infos_adc[iten].text, Link[iten].get("href")])

                else: #Para fazer o filtro é necessário formatar o texte recebido, pois ele contem alguns caracteres
                    # especias alem dos número e por isso não pode ser diretamente convertido em um número inteiro
                    precos = Precos[iten].text
                    preco = ''


                    for letra in range(0, len(precos)):
                        if precos[letra] in "1234567890":#Formata a string para ele conter apenas numeros
                            preco += precos[letra]

                    if preco == '': #Existe um apartamento que não tem preço e isso estava dando um erro, para isso
                                    #verifico se o preco esta vazio, depois uso operador continue que interrompe a
                                    #instrução atual e começa a aproxima assim ele não dará erro
                       continue

                    if int(preco) <= filtro: #Verifica se o float passará pelo filtro, entrando na variável que
                # retornará caso passe
                        if regiao_bairro in "Não informado": #filtro de preço sem localidade, adiciona direto
                            tabela.append([Endereco[iten].text, Titulos[iten].text, preco, Infos_adc[iten].text,
                                           Link[iten].get("href")])


                        else: #Filtro de preço com localidade
                            if filtrarLocalizacao(Endereco[iten].text, regiao_bairro, regiao_ou_bairro):
                                tabela.append([Endereco[iten].text, Titulos[iten].text, Precos[iten].text,
                                                       Infos_adc[iten].text, Link[iten].get("href")])



                    preco = "" #Tira os valore da variável

            print(f"\033[1;32m Página {passeguidas} Extraida com sucesso!\033[0;0m")
            return tabela


    def variasPaginsa(self, paginas=1, filtro=0, regiao_ou_bairro = "Sem filtro", regiao_bairro="Sem filtro"):
        lista_a_retornar = list()
        if paginas == 1: #Caso só seja uma página, necessitei fazer isso para tirar o argumento de dentro do método
                         #carregar assim ele ira na primera página dos apartamentos
            lista_a_retornar += self.carregar(filtro=filtro, regiao_ou_bairro=regiao_ou_bairro,
                                                  regiao_bairro=regiao_bairro)
        else:
            for numero in range(0, paginas):
                try:
                    lista_a_retornar += self.carregar(pag=numero, filtro=filtro, regiao_ou_bairro=regiao_ou_bairro,
                                                          regiao_bairro=regiao_bairro)
                except:
                    print(f"Não foi possível baixar a página {numero}")
                else:
                    continue

        return lista_a_retornar


class VivaReal:
    def __init__(self):
        self.url = "https://www.vivareal.com.br/aluguel/paraiba/campina-grande/apartamento_residencial/"
        #Quando mudamos de página a url muda adicinando um ?pagina= e depois do sinal de igualdade colocamos
        # a identificação do site ex:?pagina=2 vai para a página 2


    def carregar(self, pag=0, filtro=0, regiao_ou_bairro="Não informado", regiao_bairro="Não informado"):
        """

        :param pag: Recebe como argumento um número inteiro que será a pagina a qual desejamos faz a raspagem da dados
        :return: Retorna  uma lista com todos os apartamentos da pagina como: rua, titulo, metros quadrados, quanditadede
        quartos, banheiros, vagas na garagem, preço e link para acesarmos a pagina. Tudo isso dividindo os apartamentos
        em uma lista.



        """
        link = f"{self.url}{f'?pagina={pag}' if pag != 0 else ''}"
        print(f"\033[1;107m\033[1;30m Requisitando a {link}...\033[0;0m  ")#Mostrando dados ao usuário
        try:
            requisicao  = get(link)
        except:
            print(f"\033[1;31mErro ao tetar conectarse ao {link}\033[0;0m ")
        else:
            bs = BeautifulSoup(requisicao.text, "html.parser")


            Ruas = bs.find_all("span",
            class_="property-card__address")
            Titulos = bs.find_all("span",
            class_="property-card__title js-cardLink js-card-title")
            Metros_quadrados = bs.find_all("li",
        class_="property-card__detail-item property-card__detail-area")
            Quartos = bs.find_all("li",
            class_="property-card__detail-item property-card__detail-room js-property-detail-rooms")
            #Faz parte de uma lista é a quandtidade de quartos
            Banheiros = bs.find_all("li",
            class_="property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom")
            #Faz parte de uma lista é a quantidade de banheiros
            Vagas = bs.find_all("li",
            class_="property-card__detail-item property-card__detail-garage js-property-detail-garages")
            #Faz parte de uma lista é a quantidade de vagas na garagem
            Preco = bs.find_all("div",
            class_="property-card__price js-property-card-prices js-property-card__price-small")
            #Há hierarquia aqui prestar atenção
            """Preco_condominio = bs.find_all("div",   Nem sempre os apartamentos terão o preco do condominio 
            class_="property-card__price-details--condo")"""
            #Há hierarquia aqui prestar atenção
            Links = bs.find_all("a",
            class_="property-card__content-link js-card-title")

            preco = str()
            preco_correto = str()

            tabela_principal = list()
            for valor in range(0, len(Titulos)):
                preco = Preco[valor].text

                for caracter in range(0, len(preco)): #Para fazer o filtro seria necessário o número inteiro,
                    # porém quando retornava o valor tinha alguns caracteres que não apareciam no print, por isso
                    # tive que fazer essa foratação
                    if preco[caracter] in "1234567890":
                        preco_correto = preco_correto + preco[caracter]

                if filtro == 0: # Faz a verificação do filtro de preço

                    if regiao_ou_bairro != "Não informado":

                        if filtrarLocalizacao(Endereco=Ruas[valor].text, regiao_bairro=regiao_bairro,
                                              regiao_ou_bairro=regiao_ou_bairro ):
                            tabela_principal.append([Ruas[valor].text,
                                         Titulos[valor].text,
                                         preco_correto,
                                         [Metros_quadrados[valor].text,Quartos[valor].text, Banheiros[valor].text],
                                         #Preco_condominio[valor].find("strong").text,
                                         f"https://www.vivareal.com.br{Links[valor].get('href')}"])
                    else:
                        tabela_principal.append([Ruas[valor].text,
                                         Titulos[valor].text,
                                         preco_correto,
                                         [Metros_quadrados[valor].text,Quartos[valor].text, Banheiros[valor].text],
                                         #Preco_condominio[valor].find("strong").text,
                                         f"https://www.vivareal.com.br{Links[valor].get('href')}"])
                else:
                    if int(preco_correto) <= filtro:#Filtra os valores, se no caso forem menores serão adicionado a lista
                        if regiao_ou_bairro != "Não informado":
                            if filtrarLocalizacao(Endereco=Ruas[valor].text, regiao_bairro=regiao_bairro,
                                                  regiao_ou_bairro=regiao_ou_bairro):
                                tabela_principal.append([Ruas[valor].text, Titulos[valor].text, preco_correto,
                                                                                        [Metros_quadrados[valor].text,
                                                                                       Quartos[valor].text,
                                                                                       Banheiros[valor].text],
                                                                f"https://www.vivareal.com.br{Links[valor].get('href')}"])
                        else:
                            tabela_principal.append([Ruas[valor].text, Titulos[valor].text, preco_correto,
                                                                                        [Metros_quadrados[valor].text,
                                                                                       Quartos[valor].text,
                                                                                       Banheiros[valor].text],
                                                                f"https://www.vivareal.com.br{Links[valor].get('href')}"])
                preco_correto = ''
            print(f"\033[1;32mPagina {pag if pag != 0 else 1} Baixada e formatada  com sucesso! \033[0;0m  ")
            return tabela_principal


    def variasPaginas(self, quantidade_pag=1, caso_filtro=0, regiao_ou_bairro="Não informado", regiao_bairro="Não informado"):
        """

        :param quantidade_pag: Recebe como argumento um número inteiro que sera a quantidade de páginas as quais
        será feito a rapasgem de dados
        :param caso_filtro: Se receber algum argumento, ele ira colocar na funcionalidade carregar no parâmetro filtro
        o que ele recebeu como argumento assim sera feito a verificacação de preço.
        :return: retornará uma lista com o os apartamentos
        """
        todas_pags = list()
        print("Conectando...")
        sleep(1)
        for vezes in range(1, quantidade_pag + 1):
            if vezes == 1:
                todas_pags += self.carregar(pag=vezes, filtro=caso_filtro, regiao_ou_bairro=regiao_ou_bairro,
                                                regiao_bairro=regiao_bairro)
            else:
                try:
                    todas_pags += self.carregar(pag=vezes, filtro=caso_filtro, regiao_ou_bairro=regiao_ou_bairro,
                                                    regiao_bairro=regiao_bairro)
                except Exception: #Caso aconteça algum erro de solicitação ou de indicie, poderia colocar um IndexError,
                    # mais asssim abrage bem mais Sem falar que para que o programa não pare de funcionar essa é um boa
                    #solução
                    break
                else:
                    continue
        return todas_pags


