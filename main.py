"""""
import requests

# Chave da API do Google Maps
API_KEY = 

def geocodificar(endereco):
    """ """
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={API_KEY}'
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        resultado = response.json()
        if resultado['status'] == 'OK':
            localizacao = resultado['results'][0]['geometry']['location']
            return f"{localizacao['lat']},{localizacao['lng']}"
    return None

def criar_link_mapas(pontos):
    """"""
    if len(pontos) < 2:
        return "Número insuficiente de pontos para criar uma rota."

    base_url = "https://www.google.com/maps/dir/"
    pontos_intermediarios = '/'.join(pontos[1:-1]) if len(pontos) > 2 else ''
    rota_url = base_url + pontos[0] + '/' + pontos_intermediarios + '/' + pontos[-1]
    return rota_url

# Exemplo de endereços
enderecos = [
    "R. São carlos, 217, Gravataí - RS, Brasil",
    "R. Dona Idalina, 37, Gravataí - RS, Brasil",
    "R. Pintassilgo, 40 - Chico Mendes, Cachoeirinha - RS, Brasil",
    "R. da Fé, 310 - Rincão da Madalena, Gravataí - RS, Brasil",
    "R. Curumim, 157 - Dona Mercedes, Gravataí - RS, Brasil",
    "Av Borges de Medeiros, 1204 - Colonial, Sapucaia do Sul - RS, Brasil"]

# Obter coordenadas para cada endereço
coordenadas = [geocodificar(endereco) for endereco in enderecos]

# Gerar link para o Google Maps
link_maps = criar_link_mapas(coordenadas)
print("Link da Rota no Google Maps:", link_maps)
""" # API_KEY = 
import tkinter as tk
import requests
import webbrowser

# Substitua pela sua chave de API do Google Maps
API_KEY = ''

def geocodificar(endereco):
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={API_KEY}'
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        resultado = response.json()
        if resultado['status'] == 'OK':
            localizacao = resultado['results'][0]['geometry']['location']
            return f"{localizacao['lat']},{localizacao['lng']}"
    return None

def criar_link_mapas(pontos):
    if len(pontos) < 2:
        return "Número insuficiente de pontos para criar uma rota."
    base_url = "https://www.google.com/maps/dir/"
    pontos_intermediarios = '/'.join(pontos[1:-1]) if len(pontos) > 2 else ''
    return base_url + pontos[0] + '/' + pontos_intermediarios + '/' + pontos[-1]

def buscar_rota():
    enderecos = [endereco.get() for endereco in entradas_endereco]
    coordenadas = [geocodificar(end) for end in enderecos if end]
    link = criar_link_mapas(coordenadas)
    link_rotas.config(text=link)
    webbrowser.open(link)

def adicionar_endereco():
    novo_endereco = tk.Entry(root)
    novo_endereco.pack()
    entradas_endereco.append(novo_endereco)

# Configuração da Janela Tkinter
root = tk.Tk()
root.title("Gerenciador de Rotas")

# Lista para armazenar as entradas de endereço
entradas_endereco = []

# Adicionando entradas para endereços
for i in range(4):
    entry = tk.Entry(root)
    entry.pack()
    entradas_endereco.append(entry)

# Botão para adicionar mais endereços
botao_adicionar = tk.Button(root, text="Adicionar Mais Endereços", command=adicionar_endereco)
botao_adicionar.pack()

# Botão para buscar a rota
botao_buscar = tk.Button(root, text="Buscar Rota", command=buscar_rota)
botao_buscar.pack()

# Label para mostrar o link da rota
link_rotas = tk.Label(root, text="Link da rota aparecerá aqui", wraplength=300)
link_rotas.pack()

# Inicia o loop da interface gráfica
root.mainloop()
