from pathlib import Path
import json
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

import config


class WhatsAppSender:

    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

        self.profile_path = (
            Path(__file__).parent.parent / "chrome-profile"
        )

        self.templates_path = (
            Path(__file__).parent.parent
            / "data"
            / "templates.json"
        )

        self.images_path = (
            Path(__file__).parent.parent
            / "images"
        )

    def start(self, campaign):
        try:
            self.open_browser()
            self.open_whatsapp()

            print("✅ Chrome abierto.")
            print("✅ WhatsApp listo.")

            self.find_chat()

            message = self.get_message(campaign)
            image = self.get_image(campaign)

            # Primero se adjunta la imagen. Al hacerlo, WhatsApp reemplaza
            # el compose box original por el editor de imagen Si se escribe el mensaje antes de
            # adjuntar, se pierde al abrirse el editor.
            self.attach_image(image)
            self.write_caption(message)
            self.send()

            print("\n✅ Campaña enviada correctamente. Cerrando...")

            # Pequeña espera para asegurar que WhatsApp termine de procesar el envío 
            self.page.wait_for_timeout(2000)

        except Exception as e:
            print("\n❌ ERROR")
            print(e)

            input("\nPresiona ENTER para cerrar el navegador...")

        finally:
            self.close()

    def open_browser(self):
        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_path),
            channel="chrome",
            headless=False,
        )

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

    def open_whatsapp(self):
        self.page.goto("https://web.whatsapp.com")
        self.page.wait_for_load_state("networkidle")

    def find_chat(self):
        chat_name = (
            config.TEST_CHAT
            if config.TEST_MODE
            else config.PRODUCTION_CHAT
        )

        print(f"🔍 Buscando chat: {chat_name}")

        search_box = self.page.get_by_placeholder(
            "Buscar un chat o iniciar uno nuevo"
        )

        search_box.wait_for(state="visible")

        search_box.click()
        search_box.fill(chat_name)

        results = self.page.get_by_text(
            chat_name,
            exact=True
        )

        results.first.wait_for(state="visible")

        if results.count() > 1:
            results.nth(1).click()
        else:
            results.first.click()

        print("✅ Chat abierto.")

    def get_message(self, campaign):
        print("📄 Leyendo plantilla...")

        with open(
            self.templates_path,
            "r",
            encoding="utf-8"
        ) as file:
            templates = json.load(file)

        template_name = campaign["template"]

        message = templates[template_name]

        if template_name == "weekly":
            message = message.format(
                number=campaign["number"]
            )

        print("✅ Mensaje cargado.")

        return message

    def get_image(self, campaign):
        image = (
            self.images_path
            / campaign["image"]
        )

        print(f"🖼️ Imagen: {image.name}")

        return image

    def attach_image(self, image, max_attempts=3):
        print("📎 Adjuntando imagen...")

        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                print(f"Intento {attempt}/{max_attempts}...")

                attach_button = self.page.get_by_role(
                    "button", name="Adjuntar"
                )
                attach_button.wait_for(state="visible", timeout=5000)
                attach_button.click()

                photos_item = self.page.get_by_role(
                    "menuitem", name="Fotos y videos"
                )
                photos_item.wait_for(state="visible", timeout=5000)

                with self.page.expect_file_chooser(
                    timeout=8000
                ) as fc_info:
                    photos_item.click()

                file_chooser = fc_info.value
                file_chooser.set_files(str(image))

                caption_container = self.page.get_by_test_id(
                    "media-caption-input-container"
                )
                caption_container.wait_for(state="visible", timeout=10000)

                print("✅ Imagen adjuntada.")
                return

            except (PlaywrightTimeoutError, Exception) as e:
                last_error = e
                print(f"Intento {attempt} falló: {e}")

                # Si el menú se cerró o quedó en un estado raro, se
                # presiona Escape para volver a un estado limpio antes
                # de reintentar.
                try:
                    self.page.keyboard.press("Escape")
                except Exception:
                    pass

        raise Exception(
            f"No fue posible adjuntar la imagen tras {max_attempts} "
            f"intentos. Último error: {last_error}"
        )

    def write_caption(self, message):
        print("⌨️ Escribiendo mensaje...")

        caption_container = self.page.get_by_test_id(
            "media-caption-input-container"
        )
        caption_container.wait_for(state="visible", timeout=10000)

        caption_box = caption_container.get_by_role("textbox")

        if caption_box.count() == 0:
            caption_box = caption_container

        caption_box.click()
        caption_box.fill(message)

        print("✅ Mensaje escrito.")

    def send(self):
        print("📤 Enviando mensaje...")

        # El botón del editor de imagen tiene un aria-label que incluye
        # "seleccionado" (ej. "Enviar 1 seleccionado"). Esto lo
        # distingue del botón "Enviar" del compose box normal, que
        # también sigue existiendo (oculto) en el DOM y generaría
        # ambigüedad si se buscara solo por la palabra "Enviar".
        send_button = self.page.locator(
            '[role="button"][aria-label*="seleccionad"]'
        )

        send_button.wait_for(state="visible")
        send_button.click()

        print("✅ Mensaje enviado.")

    def close(self):
        if self.context:
            self.context.close()

        if self.playwright:
            self.playwright.stop()