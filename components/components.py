import flet as ft
import sqlite3
import clipboard
import os

# IMAGEM
img = ft.Container(content=ft.Row([ft.Image(src='.\\assets\\ELEPHANT.svg',width=125,height=125,fit=ft.ImageFit.CONTAIN)], alignment="center"))

# ESTILOS DE BUTÃO 
estiloDoButao=ft.ButtonStyle(color="WHITE",bgcolor="TRANSPARENTE",side=ft.BorderSide(2,"#00B9D2"),shape=ft.RoundedRectangleBorder(radius=10))

estiloDoButao02=ft.ButtonStyle(color="#021627",bgcolor=ft.Colors(value="white"), shape=ft.RoundedRectangleBorder(radius=10))

# ESTILO DE LABEL
label_style_title=ft.TextStyle(color=ft.Colors(value="white"),size=18,weight=ft.FontWeight.W_800,letter_spacing=1)

# ESTILO DE HINT
hint_style_title=ft.TextStyle(color=ft.Colors(value="white"),size=14,weight=ft.FontWeight.W_500,letter_spacing=1)

# ESTILO DE TEXTO
text_field_style = ft.TextStyle(color=ft.Colors(value="white"),size=14,weight=ft.FontWeight.W_500,letter_spacing=1)

# TÍTULO DO PROJETO
titleProject=ft.Text(value="GERÊNCIADOR DE CONTAS", color=ft.Colors(value="white"), size=23, weight=ft.FontWeight.BOLD)

#==============
# Class dos campós de preenchimento
class Info_contas(ft.TextField):
     def __init__(self,label, hint_text, autofocus):
          super().__init__()
          self.label=label
          self.hint_text=hint_text
          self.label_style = label_style_title
          self.hint_style = hint_style_title
          self.border="#00B9D2"
          self.border_width=2,
          self.border_radius=10
          self.color=ft.Colors(value="white")
          self.autofocus=True
          self.border_color = "white"
          self.width=300
          
     def info_contas(self):
          return ft.TextField(value=self.label, hint_text=self.hint_text)

# Variáveis dos campos de preenchimentos
campo_tipo_conta= Info_contas("Tipo da conta *", "Exemplos: Facebook, Gmail, Instagram...", True)
campo_login = Info_contas("Login da conta *","Exemplo: mario@gmail.com",False)
campo_senha = Info_contas("Senha *","Exemplo: senha1234", False)
# Container que vai concentrar os campos
campo_container = ft.Container(content=ft.Column([campo_tipo_conta,campo_login,campo_senha]), padding=ft.Padding(0,80,0,40))

#==============
table=[]

path_bd=".\\data\\meu_banco_de_dados.db"
# Verificar se o arquivo existe
try:
     if os.path.isfile(path_bd):
          # CONEXÃO COM O BANCO DE DADOS
          con = sqlite3.connect(path_bd,check_same_thread=False)
          cursor = con.cursor()
     else:
          
          con = sqlite3.connect(path_bd,check_same_thread=False)
          cursor = con.cursor()
          cursor.execute(
               """CREATE TABLE "Conta" 
               ("conta"	TEXT, "login"	TEXT, "senha"	TEXT)"""
          )
          con.commit()
except TypeError as error:
          print(f"Erro encontrado: {error}")

def consultar_e_atualizar_table():
     try:
          if os.path.isfile(path_bd):
               # CONEXÃO COM O BANCO DE DADOS
               con = sqlite3.connect(path_bd,check_same_thread=False)
               cursor = con.cursor()
          cursor.execute("SELECT conta, login, senha FROM Conta")
          contas=cursor.fetchall()
          table=[]
          for conta in contas:
               table.append(conta)
          return table
     except TypeError as error:
          print(f"Erro encontrado: {error}")
          
          
consultar_e_atualizar_table()
class Msg_aviso():
     def __init__(self,pag,msg):
          self.pag=pag
          self.msg=msg
          self.bgcolor = ft.Colors.GREEN
          self.snack_bar = ft.SnackBar(content=ft.Text(value=f"{self.msg}", font_family="Rajdhani", weight=ft.FontWeight.W_900, text_align="center",size=20, color= ft.Colors("white")), bgcolor=self.bgcolor)

     def open_msg_green(self):
          self.pag.overlay.append(
               self.snack_bar
          )
          self.snack_bar.open=True
          self.pag.update()

     def open_msg_red(self):
          self.snack_bar.bgcolor= ft.Colors.RED
          self.pag.overlay.append(
               self.snack_bar
          )
          self.snack_bar.open=True
          self.pag.update()         


# Função de adicionar uma conta no banco de dados
def funcao_add_na_tabela(event, pag):
     if campo_tipo_conta.value == "":
          msg_aviso = Msg_aviso(pag=pag, msg="Por favor, preencha os campos com (*)")
          msg_aviso.open_msg_red()
          print("Cliquei")
     elif campo_login.value == "":
          msg_aviso= Msg_aviso(pag=pag, msg="Por favor, preencha os campos com (*)")
          msg_aviso.open_msg_red()
          print("Cliquei")
     elif campo_senha.value =="":
          msg_aviso= Msg_aviso(pag=pag, msg="Por favor, preencha os campos com (*)")
          msg_aviso.open_msg_red()
          print("Cliquei")
     elif (campo_tipo_conta.value,campo_login.value,campo_senha.value) != "":
          try: 
               con = sqlite3.connect(path_bd,check_same_thread=False)
               cursor = con.cursor()
               cursor.execute("INSERT INTO Conta (conta, login, senha) VALUES (?,?,?)", (campo_tipo_conta.value, campo_login.value, campo_senha.value))
               con.commit()  #Comitar a transação
          except (NameError) as error:
               print(error)
               msg_aviso= Msg_aviso(pag=pag, msg=f"{error}")
               msg_aviso.open_msg_green()         
          except (TypeError) as error:
               print(error)
               msg_aviso= Msg_aviso(pag=pag, msg=f"{error}")
               msg_aviso.open_msg_green()         
          except (sqlite3.OperationalError) as error:
               print(error)
               msg_aviso= Msg_aviso(pag=pag, msg=f"{error}")
               msg_aviso.open_msg_green()         
          campo_tipo_conta.value=""
          campo_login.value=""
          campo_senha.value=""
          pag.update()
          msg_aviso= Msg_aviso(pag=pag, msg="Conta Salva com sucesso!")
          msg_aviso.open_msg_green()         

#============
# Função de copiar login e senha
def copy_conteudo(data, pagina):
     try:
          clipboard.copy(data)
          print(f"{data}, Copiado com sucesso!")
          aviso=Msg_aviso(pag=pagina,msg="Copiado com sucesso !!")
          aviso.open_msg_green()
     except (TypeError,NameError):
          print(f"Erro encontrado - TypeError: {TypeError}")
          print(f"Erro encontrado - NameError: {NameError}")
     


def deletar_da_tabela(item,pag):
     def handle_close(e):
          pag.close(dlg_modal)
          if e.control.text == "Sim":
               cursor.execute("DELETE FROM Conta WHERE conta = ?", (item,))
               con.commit()
               pag.update()
               msg_aviso= Msg_aviso(pag=pag, msg=f"Conta {item}, deletada com sucesso!")
               msg_aviso.open_msg_green()
               consultar_e_atualizar_table()
          else:
               pass

     dlg_modal = ft.AlertDialog(
          modal=True,
          title=ft.Text("Por favor confirme."),
          content=ft.Text("Você realmente deseja excluir essa conta do seu banco de dados?"),
          actions=[
               ft.TextButton("Sim", on_click=handle_close),
               ft.TextButton("Não", on_click=handle_close),
          ],
          actions_alignment=ft.MainAxisAlignment.END
     )
     pag.open(dlg_modal)
     


def editar_login_tabela(item1, item2, pag):   
     cursor.execute("""UPDATE Conta SET login = ? WHERE login = ? """, (item2, item1))
     con.commit()
     pag.update()
     aviso=Msg_aviso(pag=pag,msg="Login editado com sucesso !!")
     aviso.open_msg_green()
     consultar_e_atualizar_table()
     

def editar_senha_tabela(item1, item2, pag):   
     cursor.execute("UPDATE Conta SET senha = ? WHERE senha = ? ", (item2, item1))
     con.commit()
     pag.update()
     aviso=Msg_aviso(pag=pag,msg="Senha editado com sucesso !!")
     aviso.open_msg_green()
     consultar_e_atualizar_table()

# Classe base para todos os botões do app
class Btn_base():
     def __init__(self,texto,icone,style,on_click):
          self.texto  = texto
          self.icone = icone
          self.style = style
          self.on_click = on_click
          
     def btn_home(self):
          var_btn= ft.TextButton(content=ft.Row([ft.Icon(name
          = self.icone, color="#00B9D2"),ft.Text(value=self.texto, size=24, weight=ft.FontWeight.BOLD)]),
          style=self.style, 
          height=50,width=250, 
          on_click= self.on_click)
          return var_btn
     
     def btn_contas(self,width):
          var_btn= ft.TextButton(content=ft.Row([ft.Icon(name
          = self.icone, color="#021627"),ft.Text(value=self.texto, size=24, weight=ft.FontWeight.BOLD)]),
          style=self.style, 
          height=50,width=width, 
          on_click= self.on_click)
          return var_btn
     
     def btn_save(self,width):
          var_btn= ft.TextButton(content=ft.Row([ft.Icon(name
          = self.icone, color="#021627"),ft.Text(value=self.texto, size=24, weight=ft.FontWeight.W_900)]),
          style=self.style, 
          height=50,width=width, 
          on_click= self.on_click)
          return var_btn


# Variáveis de botões
btn_home = Btn_base(texto="Inicio", icone="HOUSE", style=estiloDoButao, on_click= any).btn_home()
btn_ver_contas = Btn_base(texto="Minhas contas", icone="LIST", style=estiloDoButao02, on_click= any).btn_contas(250)
btn_add = Btn_base(texto="Salvar dados", icone="SAVE", style=estiloDoButao02, on_click= any).btn_save(300)

#============
# Variável de título
title_home_page = ft.Text("NOVA CONTA?", color="WHITE", size=52, weight= ft.FontWeight.W_900)

title_my_aconts_page = ft.Text("MINHAS CONTAS", color="WHITE", size=52, weight= ft.FontWeight.W_900)

# Variável de informação
informacao= ft.Text("SE DESEJA SALVAR UMA NOVA CONTA PARA LEMBRAR DEPOIS, PREENCHA OS CAMPOS ABAIXO E SALVE OS DADOS.",color="WHITE", size=15, width=300,)

# Container que recbe títlo da página de início 
titulo_infomacao = ft.Container(content=ft.Column([title_home_page,informacao]))

#=============
class List_contas():
     def __init__(self,conta,login,senha,pag):
          self.conta=conta
          self.login=login
          self.senha=senha
          self.pag=pag
          

     def lista_conta_retorno(self):
          ft_text_login=ft.TextField(label="Login", value= f"{self.login}", label_style=label_style_title, hint_style= hint_style_title, expand=True, border_color=ft.Colors(value="white"))

          ft_text_senha=ft.TextField(label="Senha", value= f"{self.senha}", label_style=label_style_title, hint_style= hint_style_title, expand=True, border_color=ft.Colors(value="white"))

          content_login = ft.Row([ft_text_login,
               ft.IconButton(icon=ft.Icons.COPY, icon_color= "#A2BBCA", on_click=lambda e: copy_conteudo(data=self.login,pagina=self.pag)), 
               ft.IconButton(icon=ft.Icons.EDIT, icon_color= "#A2BBCA", on_click=lambda e: editar_login_tabela(item1=self.login,item2=ft_text_login.value,pag=self.pag))])

          content_senha = ft.Row([ft_text_senha, 
               ft.IconButton(icon=ft.Icons.COPY, icon_color= "#A2BBCA", on_click=lambda e: copy_conteudo(data=self.senha,pagina=self.pag)), 
               ft.IconButton(icon=ft.Icons.EDIT, icon_color= "#A2BBCA", on_click=lambda e: editar_senha_tabela(item1=self.senha,item2=ft_text_senha.value,pag=self.pag))]) 

          content_delete = ft.IconButton(icon=ft.Icons.DELETE, icon_color= "#A2BBCA", on_click=lambda e:deletar_da_tabela(item=self.conta, pag=self.pag))

          content_list=ft.Column([content_login, content_senha, content_delete], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
          return content_list

class Item_conta(ft.ExpansionPanelList):
     def __init__(self, pag):
          super().__init__()
          self.bgcolor = ft.Colors(value="transparent")
          self.spacing = 5
          self.divider_color= "#A2BBCA"
          self.elevation=0
          self.controls = []
          self.pag = pag     

          try:
               
               for item in consultar_e_atualizar_table():
                    list_contas=List_contas(conta=item[0],login=item[1],senha=item[2],pag = self.pag).lista_conta_retorno()
                    exp = ft.ExpansionPanel(
                         bgcolor=ft.Colors(value="transparent"),
                         can_tap_header=True,
                         header= ft.Text(value = f"{item[0]}", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=24, weight= ft.FontWeight.W_900)),
                         content= ft.Container(ft.Column([list_contas]), alignment=ft.alignment.bottom_center,padding=ft.Padding(20,15,5,15),border=ft.Border(left=ft.BorderSide(1,ft.Colors(value="white")),bottom=ft.BorderSide(1,ft.Colors(value="white"))), border_radius=15) 
                         )
                    self.controls.append(exp)
               
          except TypeError as error:
               print(f"erro encontrado: {error}")
     
     def atualizando_conteudo_lista(self):
          try:
               self.controls = []
               for item in consultar_e_atualizar_table():
                    list_contas=List_contas(conta=item[0],login=item[1],senha=item[2],pag = self.pag).lista_conta_retorno()
                    exp = ft.ExpansionPanel(
                         bgcolor=ft.Colors(value="transparent"),
                         can_tap_header=True,
                         header= ft.Text(value = f"{item[0]}", text_align=ft.TextAlign.CENTER, style=ft.TextStyle(size=24, weight= ft.FontWeight.W_900)),
                         content= ft.Container(ft.Column([list_contas]), alignment=ft.alignment.bottom_center,padding=ft.Padding(20,15,5,15),border=ft.Border(left=ft.BorderSide(1,ft.colors.WHITE),bottom=ft.BorderSide(1,ft.colors.WHITE)), border_radius=15) 
                         )
                    self.controls.append(exp)
          except TypeError as error:
               print(f"erro encontrado: {error}")
     
     def baco_de_dados_vazio(self):
          listaDeContas = ft.Column([ft.Text("Ops!...", size=30, weight=ft.FontWeight.BOLD),ft.Text("Não há contas em seu banco de dados no momento.", size=20),ft.Text("Volte ao 'Início' e adicione uma conta.", size=18)])
          return listaDeContas

          

# listas de contas
#=================
def my_home_pages(pagina):
     btn_add.on_click = lambda e: funcao_add_na_tabela(event=e,pag= pagina)
     page_home=ft.Column([titulo_infomacao,campo_container, btn_add])
     return page_home



def my_aconts_pages(pagina):

     var_listaDeContas = Item_conta(pag=pagina)
     var_bd_vazio = ft.Column([ft.Text("Ops!...", size=30, weight=ft.FontWeight.BOLD),ft.Text("Não há contas em seu banco de dados no momento.", size=20),ft.Text("Volte ao 'Início' e adicione uma conta.", size=18)])
     cont_var_lista_de_contas=ft.Column([var_listaDeContas], height=550, scroll= "ALWAYS")
     if len(consultar_e_atualizar_table()) == 0:
          var_listaDeContas.visible=True
          cont_var_lista_de_contas.height=0
          pagina.update()
     else:
          var_bd_vazio.visible=False
          pagina.update()

     def lista_up(e):
          if len(consultar_e_atualizar_table()) > 0:
               var_listaDeContas.atualizando_conteudo_lista()
               var_bd_vazio.visible=False
               var_listaDeContas.visible=True
               cont_var_lista_de_contas.height=550
               pagina.update()
          else:
               var_bd_vazio.visible=True
               cont_var_lista_de_contas.visible=False
               cont_var_lista_de_contas.height=0
               pagina.update()

     btn_recarregar = ft.Row([ft.Text("ATUALIZAR LISTA DE CONTAS", size= 18, weight=ft.FontWeight.BOLD),ft.IconButton(ft.Icons.REFRESH_OUTLINED, icon_size=30,on_click=lista_up)],vertical_alignment=ft.CrossAxisAlignment.CENTER)

     my_aconts_page= ft.Column([title_my_aconts_page,btn_recarregar,cont_var_lista_de_contas,var_bd_vazio])

     return my_aconts_page