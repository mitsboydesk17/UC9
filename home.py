from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDRoundFlatIconButton, MDRoundFlatButton
from kivymd.uix.card import MDCard
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import RoundedRectangle, Color
from kivy.animation import Animation

class RoundedImage(MDCard):
    def __init__(self, source, radius=16, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.elevation = 0
        self.md_bg_color = (0, 0, 0, 0)
        self.radius = [radius, radius, radius, radius]
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(radius)])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.image = Image(source=source, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class HomeScreen(Screen):
    slide_atual = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.slides = [
            {
                "imagem": "img/parque_banner.webp",
                "titulo": "Terra da Alegria",
                "subtitulo": "Onde a magia e a diversão nunca acabam"
            },
            {
                "imagem": "img/montanha_russa.jpg",
                "titulo": "Aventura sem Limites",
                "subtitulo": "Adrenalina garantida para todas as idades"
            },
            {
                "imagem": "img/piupiu.webp",
                "titulo": "Diversão Aquática",
                "subtitulo": "Mergulhe em momentos refrescantes"
            }
        ]

        self.root_layout = MDBoxLayout(orientation='vertical')
        self.add_widget(self.root_layout)

        self.construir_navbar()
        self.construir_banner()
        self.atualizar_slide(0)

        Clock.schedule_interval(self.proximo_slide, 6)

        self.bind(size=self.on_window_resize)

    def construir_navbar(self):
        topo_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            padding=[dp(15), dp(10)],
            spacing=20,
            md_bg_color=(1, 1, 1, 1)
        )

       
        logo = Image(source='img/parque_logo.png', size_hint_x=None, width=100, allow_stretch=True)
        topo_layout.add_widget(logo)

        
        espacador = MDBoxLayout(size_hint_x=1)
        topo_layout.add_widget(espacador)

  
        botoes_layout = MDBoxLayout(
            spacing=12,
            size_hint_x=None,
            width=dp(350)
        )

        botoes = [
            ("Sobre", "information-outline", self.ir_para_sobre),
            ("Brinquedos", "ride", self.ir_para_brinquedos),
            ("Contato", "email-outline", self.ir_para_contato)
        ]

        for texto, icone, funcao in botoes:
            botao = MDRoundFlatIconButton(
                icon=icone,
                text=texto,
                theme_text_color="Custom",
                text_color=(0, 0, 0, 1),
                icon_color=(.44, .5, 1, 1),
                line_color=(.44, .5, 1, 1),
                on_release=funcao
            )
            botoes_layout.add_widget(botao)

        topo_layout.add_widget(botoes_layout)

        # Botão de Gerenciar 
        self.btn_gerenciar = MDRaisedButton(
            text="Gerenciar",
            md_bg_color=(0.2, 0.6, 0.2, 1), 
            text_color=(1, 1, 1, 1),
            elevation=4,
            on_release=self.ir_para_gerente
        )
        topo_layout.add_widget(self.btn_gerenciar)

        # Botão de Login 
        self.btn_login = MDRaisedButton(
            text="Login",
            md_bg_color=(.44, .5, 1, 1),
            text_color=(1, 1, 1, 1),
            elevation=4,
            on_release=self.ir_para_login
        )
        topo_layout.add_widget(self.btn_login)

        self.root_layout.add_widget(topo_layout)

        separador = MDBoxLayout(size_hint_y=None, height=1, md_bg_color=(0.85, 0.85, 0.85, 1))
        self.root_layout.add_widget(separador)

    def construir_banner(self):
        banner_padding = MDBoxLayout(
            padding=[dp(20), dp(10), dp(20), dp(20)],
            orientation='vertical'
        )
        self.root_layout.add_widget(banner_padding)

        self.banner_layout = FloatLayout()
        banner_padding.add_widget(self.banner_layout)

        self.banner_img = RoundedImage(source='', radius=18)
        self.banner_layout.add_widget(self.banner_img)

        overlay = MDCard(md_bg_color=(0, 0, 0, 0.35), size_hint=(1, 1), elevation=0, radius=[18, 18, 18, 18])
        self.banner_layout.add_widget(overlay)

        self.texto_layout = MDCard(
            orientation='vertical',
            padding=[25, 25],
            spacing=15,
            size_hint=(0.5, None),
            height=220,
            md_bg_color=(0, 0, 0, 0.4),
            radius=[16, 16, 16, 16],
            elevation=3
        )

        self.titulo_label = MDLabel(
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        )
        self.subtitulo_label = MDLabel(
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.9)
        )

        botoes_acao_layout = MDBoxLayout(orientation='horizontal', spacing=12, size_hint_y=None, height=50)

        btn_conhecer = MDRaisedButton(
            text="Conhecer",
            md_bg_color=(.44, .5, 1, 1),
            text_color=(1, 1, 1, 1),
            elevation=3,
            on_release=self.ir_para_conhecer
        )

        btn_mapa = MDRoundFlatIconButton(
            icon="map-marker",
            text="Localização",
            icon_color=(1, 1, 1, 1),
            text_color=(1, 1, 1, 1),
            line_color=(1, 1, 1, 1),
            on_release=self.ir_para_localizacao
        )

        botoes_acao_layout.add_widget(btn_conhecer)
        botoes_acao_layout.add_widget(btn_mapa)

        self.texto_layout.add_widget(self.titulo_label)
        self.texto_layout.add_widget(self.subtitulo_label)
        self.texto_layout.add_widget(botoes_acao_layout)

        self.banner_layout.add_widget(self.texto_layout)

        self.circulos_layout = MDBoxLayout(
            size_hint=(None, None),
            spacing=8,
            pos_hint={'center_x': 0.5, 'y': 0.02},
            orientation='horizontal'
        )

        self.botao_circulos = []
        for i in range(len(self.slides)):
            btn = MDRoundFlatButton(
                text=str(i + 1),
                font_size=14,
                size_hint=(None, None),
                size=(40, 40),
                text_color=(0, 0, 0, 1),
                md_bg_color=(0.9, 0.9, 0.9, 0.7),
                on_release=lambda inst, idx=i: self.atualizar_slide(idx)
            )
            self.botao_circulos.append(btn)
            self.circulos_layout.add_widget(btn)

        total_botoes = len(self.slides)
        largura_total = (40 * total_botoes) + (8 * (total_botoes - 1))
        self.circulos_layout.size = (largura_total, 40)

        self.banner_layout.add_widget(self.circulos_layout)

    def atualizar_slide(self, indice):
        self.slide_atual = indice
        slide = self.slides[indice]

        anim_out = Animation(opacity=0, duration=0.3)
        anim_in = Animation(opacity=1, duration=0.3)

        def trocar_img(*args):
            self.banner_img.image.source = slide["imagem"]
            anim_in.start(self.banner_img.image)

        anim_out.bind(on_complete=trocar_img)
        anim_out.start(self.banner_img.image)

        self.titulo_label.text = slide["titulo"]
        self.subtitulo_label.text = slide["subtitulo"]

        for idx, btn in enumerate(self.botao_circulos):
            if idx == indice:
                btn.md_bg_color = (.44, .5, 1, 1)
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.md_bg_color = (0.9, 0.9, 0.9, 0.7)
                btn.text_color = (0, 0, 0, 1)

    def proximo_slide(self, dt=None):
        prox_indice = (self.slide_atual + 1) % len(self.slides)
        self.atualizar_slide(prox_indice)

    def on_window_resize(self, *args):
        largura = self.width
        if largura < 700:
            self.texto_layout.size_hint = (0.9, None)
            self.texto_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        else:
            self.texto_layout.size_hint = (0.5, None)
            self.texto_layout.pos_hint = {'x': 0.05, 'center_y': 0.5}

    def ir_para_sobre(self, instance):
        self.manager.current = 'sobre'

    def ir_para_contato(self, instance):
        self.manager.current = 'contato'

    def ir_para_brinquedos(self, instance):
        self.manager.current = 'brinquedos'

    def ir_para_login(self, instance):
        self.manager.current = 'cadastro'

    def ir_para_conhecer(self, instance):
        self.manager.current = 'conhecer'

    def ir_para_localizacao(self, instance):
        self.manager.current = 'localizacao'

    def ir_para_gerente(self, instance):
        self.manager.current = 'gerente'
