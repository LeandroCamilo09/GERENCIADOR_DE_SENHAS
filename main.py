import flet as ft
from components.components import img,my_home_pages, my_aconts_pages

class Main(ft.Page):
     def __init__(self):
          self.page
          
     def main(self):
          self.title = "LembreMe.2.0.App"
          self.window.width = 962
          self.window.height = 962
          self.window.center()
          self.window.shadow=True
          self.bgcolor = "#021627"
          self.fonts = {"Rajdhani":'.\\fonts\\Rajdhani-Regular.ttf'}
          self.theme = ft.Theme(font_family="Rajdhani")
          self.padding=0
          height_window = self.window.width
          

          content=[my_home_pages(self), ft.Column([my_aconts_pages(self)])]

          conteudo_lateral=ft.Container(content=content[0],padding=ft.Padding(100,100,200,0), gradient=ft.RadialGradient(radius=.8,center=ft.Alignment(1.0, 1.0),colors=[
          "#A2BBCA", "#021627"]), expand=True, height=(height_window))

          def mudando_pages(e):
               selected_index = int(e.control.selected_index)
               conteudo_lateral.content = content[selected_index]
               self.update()

          menu2 = ft.Container(ft.Column(controls=[ft.NavigationRail(
               bgcolor=ft.Colors(value="transparent"),
               height=height_window,
               selected_index=0,
               label_type=ft.NavigationRailLabelType.SELECTED,
               min_width=250,
               min_extended_width=350,
               leading=img,
               group_alignment=-0.9,
               selected_label_text_style=ft.TextStyle(size=15),
               destinations=[
                    ft.NavigationRailDestination(
                         icon=ft.Icons.HOME, 
                         selected_icon=ft.Icons.HOME,
                         label="Início"
                    ),
                    ft.NavigationRailDestination(
                         icon=ft.Icons.LIST,
                         selected_icon=ft.Icons.LIST,
                         label="Minhas contas"
                    ),
               ],
               on_change=mudando_pages,
          )]),border=ft.Border(right=ft.BorderSide(1, color="#A2BBCA")), gradient=ft.RadialGradient(center=ft.Alignment(-1.0, -1.0),colors=[
               "#A2BBCA", "#021627"
          ]), padding=ft.Padding(0,200,0,0))

          programa= ft.Row(
               [menu2,ft.VerticalDivider(width=1),conteudo_lateral])

          self.add(programa)

     ft.app(target=main)