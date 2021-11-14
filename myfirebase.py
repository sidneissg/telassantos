import requests
from kivy.app import App


class MyFireBase():
    API_KEY = "AIzaSyCHjLLyypnUPXZX10cJHyXU6KiWmNTD-YE"
    
    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        info ={"email": email, "password": senha, "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        
        if requisicao.ok:
            print("usuário criado")
            id_token = requisicao_dic["idToken"]
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)
            link = f"https://telassantos-default-rtdb.firebaseio.com/{local_id}.json"
            info_usuario = f'{{"avatar": "foto.png","email": "{email}"}}'
            requests.patch(link, data=info_usuario)


            meu_aplicativo.carregar_infos_usuario()

            meu_aplicativo.mudar_tela("cadastro")
            
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)
        


    def finalizar_conta(self, nome, telefone, endereco):
        with open("refreshtoken.txt", "r") as arquivo:
            refresh_token = arquivo.read()
        local_id, id_token = self.trocar_token(refresh_token)
        self.local_id = local_id
        self.id_token = id_token
        info = f'{{"nome": "{nome}", "telefone":"{telefone}", "endereco": "{endereco}"}}'
        requisicao = requests.patch(f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}.json", data=info)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        meu_aplicativo = App.get_running_app()
        meu_aplicativo.local_id = local_id
        meu_aplicativo.id_token = id_token

        with open("refreshtoken.txt", "w") as arquivo:
            arquivo.write(refresh_token)



        meu_aplicativo.carregar_infos_usuario()

        meu_aplicativo.mudar_tela("homepage")
        


    def atualizar_conta(self, nome, telefone, endereco):
        with open("refreshtoken.txt", "r") as arquivo:
            refresh_token = arquivo.read()
        local_id, id_token = self.trocar_token(refresh_token)
        self.local_id = local_id
        self.id_token = id_token
        info = f'{{"nome": "{nome}", "telefone":"{telefone}", "endereco": "{endereco}"}}'
        requisicao = requests.patch(f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}.json", data=info)
        requisicao_dic = requisicao.json()
        meu_aplicativo = App.get_running_app()
        meu_aplicativo.local_id = local_id
        meu_aplicativo.id_token = id_token
        meu_aplicativo.carregar_infos_usuario()
        
               
        
        # link = f"https://telassantos-default-rtdb.firebaseio.com/{self.local_id}.json"
        # print(requests.get(link).json)
        
        # info = f'{{"nome":, "{nome}", "telefone":"{telefone}"}}'
        # requests.patch(link, data=info)
        

    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info ={"email": email, "password": senha, "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if requisicao.ok:
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)



            meu_aplicativo.carregar_infos_usuario()

            meu_aplicativo.mudar_tela("homepage")
            
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["login"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

            
    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic["user_id"]
        id_token = requisicao_dic["id_token"]
        return local_id, id_token