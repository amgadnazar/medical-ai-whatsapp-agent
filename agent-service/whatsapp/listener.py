from playwright.sync_api import sync_playwright
import time


def listen():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto("https://web.whatsapp.com")

        input("Scan QR then press Enter...")

        print("Listening...")

        seen_messages = set()

        while True:

            try:

                messages = page.locator("span.selectable-text")

                count = messages.count()

                for i in range(count):

                    text = messages.nth(i).inner_text()

                    if text and text not in seen_messages:

                        seen_messages.add(text)

                        print("NEW MESSAGE:")
                        print(text)
                        print("-" * 50)

            except Exception as e:

                print(e)

            time.sleep(3)


if __name__ == "__main__":
    listen()