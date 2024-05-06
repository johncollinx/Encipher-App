import os
import pickle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from time import time
from kivy.uix.label import Label
from AesFiles import encrypt, decrypt
from kivy.core.window import Window


class EncodedButton(Button):
    def on_release(self):
        app = App.get_running_app()
        app.encode_text() if self.text == "Encode" else app.decode_text()

class CipherApp(App):
    def build(self):
        # Layout
        layout = BoxLayout(orientation='vertical', size_hint=(None, None))

        # Get the screen dimensions
        width, height = Window.size

        # Calculate the size for a mobile view
        mobile_width = width * 0.8
        mobile_height = height * 0.8
        
        # Adjust the layout size and position
        layout.size = (mobile_width, mobile_height)
        layout.pos = (width/2 - mobile_width/2, height/2 - mobile_height/2)

        # Cipher Text Input
        cipher_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        cipher_layout.add_widget(Label(text="Cipher Text:", size_hint=(0.3, 1)))
        self.cipher_text_input = TextInput(multiline=False, size_hint=(0.7, 1), background_color=(1, 1, 1, 1))
        cipher_layout.add_widget(self.cipher_text_input)
        layout.add_widget(cipher_layout)
        
        # Key Text Input
        key_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        key_layout.add_widget(Label(text="Key:", size_hint=(0.3, 1)))
        self.key_text_input = TextInput(multiline=False, size_hint=(0.7, 1), background_color=(1, 1, 1, 1))
        key_layout.add_widget(self.key_text_input)
        layout.add_widget(key_layout)
        
        # Labels
        layout.add_widget(Label(text="Encoded/Decoded Text:", font_size='20sp', size_hint=(1, None), height=40))  
        self.encoded_decoded_text_label = TextInput(multiline=True, size_hint=(1, 1), readonly=True, background_color=(1, 1, 1, 1))
        layout.add_widget(self.encoded_decoded_text_label)
        
        # Button Row
        button_layout = BoxLayout(padding=10, spacing=10, size_hint=(1, None), height=50)
        
        btn_encode = EncodedButton(text="Encode", size_hint=(0.5, 1))
        button_layout.add_widget(btn_encode)
        
        btn_decode = EncodedButton(text="Decode", size_hint=(0.5, 1))
        button_layout.add_widget(btn_decode)
        
        layout.add_widget(button_layout)
        
        return layout
    
    def encode_text(self):
        # Clear the screen
        self.clear_screen()
        
        cipher_text = self.cipher_text_input.text
        if cipher_text:
            enc_test = cipher_text.encode(encoding="utf-8")
            t = time()
            e = encrypt(data=enc_test)
            # Write initialization vector and encryption key to a file
            with open("encryption_data.dat", "wb") as f:
                pickle.dump((e.iv, e.key), f)
            self.update_output_labels(e.data, time() - t)
        
    def decode_text(self):
        # Clear the screen
        self.clear_screen()
        
        cipher_text = self.cipher_text_input.text
        key = self.key_text_input.text
        if cipher_text and key:
            t = time()
            # Read initialization vector and encryption key from file
            with open("encryption_data.dat", "rb") as f:
                iv, _  = pickle.load(f)
            d = decrypt(
                key= key,
                iv=iv,
                data=cipher_text
            )
            self.update_output_labels(d.decode("utf-8"), time() - t)
        
    def clear_screen(self):
        self.encoded_decoded_text_label.text = ''
        
    def update_output_labels(self, encoded_decoded_text, time_taken):
        # Set background color
        self.encoded_decoded_text_label.background_color = (1, 1, 1)  # White color
        # Set text color
        self.encoded_decoded_text_label.foreground_color = (0, 0, 0, 1)  # Black color
        
        # Update label
        self.encoded_decoded_text_label.text = f"Encoded/Decoded Text:\n{encoded_decoded_text}\nTime Taken: {time_taken:.4f} seconds"

if __name__ == "__main__":
    CipherApp().run()
