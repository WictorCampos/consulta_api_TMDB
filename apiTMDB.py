import os
import requests
from unidecode import unidecode

def obter_dados_tmdb(api_key, total_filmes=1500):
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": api_key,
        "language": "pt-BR",
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "include_video": "false",
        "page": 1
    }

    filmes = []

    try:
        # Iterar sobre páginas até atingir o número desejado de filmes
        while len(filmes) < total_filmes:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                dados = response.json().get("results", [])
                if not dados:
                    break

                filmes.extend(dados)
                params["page"] += 1
            else:
                print(f"Não foi possível obter dados da API. Código de status: {response.status_code}")
                break
    except requests.RequestException as e:
        print(f"Erro durante a solicitação à API: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return filmes[:total_filmes]

def obter_detalhes_filme(api_key, filme_id):
    url = f"https://api.themoviedb.org/3/movie/{filme_id}"
    params = {
        "api_key": api_key,
        "language": "pt-BR"
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            dados = response.json()
            generos = dados.get('genres', [{'name': 'Desconhecido'}])
            primeiro_genero = generos[0]['name'] if generos else 'Desconhecido'
            return primeiro_genero
        else:
            print(f"Não foi possível obter dados da API. Código de status: {response.status_code}")
            return 'Desconhecido'
    except requests.RequestException as e:
        print(f"Erro durante a solicitação à API: {e}")
        return 'Desconhecido'
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return 'Desconhecido'

def salvar_em_arquivo_tmdb(filmes, api_key):
    caminho_pasta = os.path.join(os.path.expanduser("~"), "Documentos")
    caminho_arquivo = os.path.join(caminho_pasta, "lista_filmes_tmdb.txt")

    # Verificar se a pasta existe, criar se não existir
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        for filme in filmes:
            titulo = filme.get('title', 'N/A')
            ano_lancamento = filme.get('release_date', 'N/A')[:4]  # Pegar apenas o ano
            filme_id = filme.get('id', None)

            # Obter detalhes do filme
            genero = obter_detalhes_filme(api_key, filme_id)

            nota = filme.get('vote_average', 'N/A')

            # Salvar no formato desejado
            linha = f"filme(\"{titulo}\", {ano_lancamento}, \"{genero}\", {nota})\n"
            arquivo.write(linha)

    print(f"Os dados foram salvos em: {caminho_arquivo}")

if __name__ == "__main__":
    # Substitua "SuaChaveDeAPIAqui" pela chave de API que você obteve no site do TMDb
    chave_api_tmdb = ""
    
    lista_filmes_tmdb = obter_dados_tmdb(chave_api_tmdb, total_filmes=1500)

    if lista_filmes_tmdb:
        salvar_em_arquivo_tmdb(lista_filems_tmdb, chave_api_tmdb)
    else:
        print("Nenhum dado obtido da API do TMDb.")