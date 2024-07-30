from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from pyngrok import ngrok

KV = '''
Screen:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'

        MDTextField:
            id: token_field
            hint_text: "Enter Token"
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.8
            multiline: False
            required: True
            disabled: app.is_token_saved

        MDTextField:
            id: ip_field
            hint_text: "Enter IP Address"
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.8
            multiline: False
            required: True

        MDTextField:
            id: port_field
            hint_text: "Enter Port"
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.8
            multiline: False
            required: True

        MDRaisedButton:
            id: tunnel_button
            text: app.button_text
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.5
            on_release: app.toggle_tunnel()
            md_bg_color: app.button_color

        MDLabel:
            id: url_label
            text: "Public URL: Not Available"
            halign: "center"

        MDRaisedButton:
            text: "Copy URL"
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.5
            on_release: app.copy_url()
'''

class TunnelApp(MDApp):
    button_text = StringProperty("START TUNNEL")
    button_color = StringProperty("green")
    is_tunnel_active = BooleanProperty(False)
    public_url = StringProperty("")
    is_token_saved = BooleanProperty(False)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.screen = Builder.load_string(KV)
        self.store = JsonStore('auth_token.json')

        # Check if token is already saved
        if self.store.exists('token'):
            self.is_token_saved = True
            self.screen.ids.token_field.text = self.store.get('token')['value']
            self.screen.ids.token_field.disabled = True

        return self.screen

    def toggle_tunnel(self):
        if not self.is_tunnel_active:
            token = self.screen.ids.token_field.text
            ip = self.screen.ids.ip_field.text
            port = self.screen.ids.port_field.text

            if not token:
                self.show_dialog("Error", "Please enter a token.")
                return
            if not ip or not port:
                self.show_dialog("Error", "Please enter IP and Port.")
                return

            if not self.is_token_saved:
                # Save the token for future use
                self.store.put('token', value=token)
                self.is_token_saved = True
                self.screen.ids.token_field.disabled = True

            ngrok.set_auth_token(token)
            self.public_url = ngrok.connect(port, "tcp").public_url
            self.screen.ids.url_label.text = f"Public URL: {self.public_url}"
            self.button_text = "STOP TUNNEL"
            self.is_tunnel_active = True
            self.button_color = "red"
        else:
            ngrok.disconnect(self.public_url)
            self.screen.ids.url_label.text = "Public URL: Not Available"
            self.button_text = "START TUNNEL"
            self.is_tunnel_active = False
            self.button_color = "green"

    def copy_url(self):
        if self.public_url:
            # Copy URL to clipboard (Kivy doesn't have a direct clipboard API, this would require a platform-specific approach)
            pass

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.8, 1))
        dialog.open()

TunnelApp().run()
