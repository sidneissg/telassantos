from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
import os
from functools import partial
from myfirebase import MyFireBase
import cgi

GUI = Builder.load_file("main.kv")
class MainApp(App):


    def build(self):
        self.firebase = MyFireBase()
        return GUI


    def on_start(self):
        #carregar as fotos de perfil
        arquivos = os.listdir("icones/perfil")
        pagina_foto_perfil = self.root.ids["mudarfoto"]
        lista_fotos = pagina_foto_perfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)
        #carrega as info do usuário    
        self.carregar_infos_usuario()

    def carregar_infos_usuario(self):

        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            #pegar informações
            requisicao = requests.get(f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()
            #preencher foto de perfil
            avatar = requisicao_dic["avatar"]
            nome = requisicao_dic["nome"]
            telefone = requisicao_dic["telefone"]
            endereco = requisicao_dic["endereco"]
            pagina_homepage = self.root.ids["homepage"]
            nome_cliente = pagina_homepage.ids["nome_cliente"]
            nome_cliente.text = f"Bem vindo, {nome}"
            pagina_conta = self.root.ids["conta"]
            nome_cliente = pagina_conta.ids["nome"]
            nome_cliente.text = nome
            telefone_cliente = pagina_conta.ids["telefone"]
            telefone_cliente.text = telefone
            endereco_cliente = pagina_conta.ids["endereco"]
            endereco_cliente.text = endereco
            # foto_perfil = pagina_homepage.ids["foto_perfil"]
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/perfil/{avatar}"
            self.mudar_tela("homepage")
        except:
            pass


    def pegar_tela(self):
        requisicao = requests.get(f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}.json")
        requisicao_dic = requisicao.json()
        return requisicao_dic["tela_anterior"]

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela
        info = f'{{"tela_anterior": "{id_tela}"}}'
        requests.patch(f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}.json", data=info)


    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/perfil/{foto}"
        info = f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}.json", data=info)
        self.mudar_tela("conta")


    def calcular_preco(self,tela, cor, altura, largura):
        pagina_tela = self.root.ids[f"{tela}"]
        mensagem = pagina_tela.ids["mensagem"]
        if altura == "":
            altura = 60
        if largura == "":
            largura = 90
        # altura = altura.replace(",",".")
        # largura = largura.replace(",",".")
        if cor == "branca":
            preco = float(altura)/ 100 * float(largura)/ 100 * 90 
        elif cor == "inox":
            preco = float(altura)/ 100 * float(largura)/ 100 * 90
        
        total = pagina_tela.ids["id_total"]
        preco = f"{preco:.2f}"
        preco = str(preco.replace(".",","))
        total.text = f"R$ {preco}"
    
        if mensagem != "":
            self.mudar_tela(tela)
            mensagem.text = "Os campos são obrigatórios"
            
            
            
    
    def enviar_pedido(self, cor, produto, quantidade):
        quantidade = quantidade.replace(",",".")
        if cor == "branca":
            total = float(quantidade) * 90
        elif cor == "inox":
            total = float(quantidade) * 90
        info = f'{{"produto": "{produto}", "quantidade": "{quantidade}", "total": "{total:.2f}"}}'
        requests.patch(f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}/pedidos.json", data=info)
        self.mudar_tela("homepage")
        
        
MainApp().run()