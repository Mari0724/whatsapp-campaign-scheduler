from pathlib import Path
import json
import re
from datetime import datetime
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

        self.logs_path = (
            Path(__file__).parent.parent / "logs"
        )
        self.logs_path.mkdir(exist_ok=True)

        self.debug_log_path = (
            self.logs_path
            / f"{datetime.now().strftime('%Y-%m-%d')}-debug.log"
        )

    def debug(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}"

        print(line)

        try:
            with open(
                self.debug_log_path,
                "a",
                encoding="utf-8"
            ) as file:
                file.write(line + "\n")
        except Exception:
            pass

    def start(self, campaign):
        try:
            self.open_browser()
            self.open_whatsapp()

            self.debug("✅ Chrome abierto.")
            self.debug("✅ WhatsApp listo.")

            self.find_chat()

            message = self.get_message(campaign)
            image = self.get_image(campaign)

            # Primero se adjunta la imagen. Al hacerlo, WhatsApp reemplaza
            # el compose box original por el editor de imagen.
            self.attach_image(image)

            self.write_caption(message)

            self.send()

            self.debug("\n✅ Campaña enviada correctamente. Cerrando...")

            self.page.get_by_test_id(
                "media-caption-input-container"
            ).wait_for(
                state="hidden",
                timeout=30000
            )
            self.debug("✅ El editor desapareció.")
            self.page.wait_for_timeout(1000)


        finally:
            
            self.close()

    def open_browser(self):
        self.debug("🚀 Iniciando Playwright...")
        self.playwright = sync_playwright().start()
        self.debug("🌐 Abriendo Google Chrome...")
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_path),
            channel="chrome",
            headless=False,
        )
        self.debug("✅ Chrome iniciado.")
        self.page = None

        for page in self.context.pages:
            if "web.whatsapp.com" in page.url:
                self.page = page
                break

        if self.page is None:
            if self.context.pages:
                self.page = self.context.pages[0]
            else:
                self.page = self.context.new_page()

    def open_whatsapp(self):

        self.debug("🌐 Abriendo WhatsApp Web...")

        last_error = None

        for attempt in range(1, 4):

            try:

                self.debug(f"\n========== Intento {attempt}/3 ==========")
                self.debug(f"URL actual: {self.page.url}")

                if "web.whatsapp.com" not in self.page.url:

                    self.debug("➡️ Navegando a WhatsApp Web...")

                    self.page.goto(
                        "https://web.whatsapp.com",
                        wait_until="domcontentloaded",
                        timeout=120000
                    )

                    self.debug("✅ goto terminó correctamente.")

                else:

                    self.debug("✅ Ya estaba en WhatsApp.")

                self.debug("⏳ Esperando barra de búsqueda...")

                self.page.get_by_placeholder(
                    "Buscar un chat o iniciar uno nuevo"
                ).wait_for(
                    state="visible",
                    timeout=60000
                )

                self.debug("✅ WhatsApp cargó correctamente.")

                return

            except PlaywrightTimeoutError as e:

                last_error = e

                self.debug("⏰ Timeout esperando WhatsApp.")
                self.debug(str(e))

            except Exception as e:

                last_error = e

                self.debug(f"❌ {type(e).__name__}: {e}")
                self.debug(type(e).__name__)
                self.debug(str(e))

            self.page.reload()

        raise Exception(
            f"No fue posible abrir WhatsApp.\n{last_error}"
        )

    def find_chat(self):
        chat_name = (
            config.TEST_CHAT
            if config.TEST_MODE
            else config.PRODUCTION_CHAT
        )

        self.debug(f"🔍 Buscando chat: {chat_name}")

        search_box = self.page.get_by_placeholder(
            "Buscar un chat o iniciar uno nuevo"
        )

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

        self.debug("✅ Chat abierto.")

    def get_message(self, campaign):
        self.debug("📄 Leyendo plantilla...")

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

        self.debug("✅ Mensaje cargado.")

        return message

    def get_image(self, campaign):
        image = (
            self.images_path
            / campaign["image"]
        )

        self.debug(f"🖼️ Imagen: {image.name}")

        return image

    def attach_image(self, image, max_attempts=3):
        self.debug("📎 Adjuntando imagen...")

        last_error = None

        for attempt in range(1, max_attempts + 1):
            try:
                self.debug(f"Intento {attempt}/{max_attempts}...")

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

                self.debug("✅ Imagen adjuntada.")
                return

            except (PlaywrightTimeoutError, Exception) as e:
                last_error = e
                self.debug(f"Intento {attempt} falló: {e}")

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
        self.debug("⌨️ Escribiendo mensaje...")

        caption_container = self.page.get_by_test_id(
            "media-caption-input-container"
        )
        caption_container.wait_for(state="visible", timeout=10000)

        caption_box = caption_container.get_by_role("textbox")

        if caption_box.count() == 0:
            caption_box = caption_container

        caption_box.click()
        caption_box.fill(message)

        self.debug("✅ Mensaje escrito.")

    def send(self):
        self.debug("📤 Enviando mensaje...")

        messages = self.page.locator(
            "[data-testid='msg-container']"
        )

        send_button = self.page.locator(
            '[role="button"][aria-label*="seleccionad"]'
        )

        send_button.first.click()

        self.debug("✅ Click realizado.")
        self.debug("⏳ Esperando confirmación de envío...")

        last = messages.last

        while True:

            pending = last.locator(
                "span[aria-label*='Pendiente']"
            )

            if pending.count() == 0:
                self.debug("✅ Mensaje enviado por WhatsApp.")
                return

            self.debug("⏳ Mensaje todavía pendiente...")

            self.page.wait_for_timeout(200)

    def close(self):

        try:

            if self.context:
                self.context.close()

        except Exception:
            pass

        try:

            if self.playwright:
                self.playwright.stop()

        except Exception:
            pass