from playwright.sync_api import sync_playwright


def start_whatsapp():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(
            "https://web.whatsapp.com"
        )

        print("Scan QR Code")

        input("Press Enter after login...")

        print("WhatsApp Connected")

        while True:
            pass


if __name__ == "__main__":
    start_whatsapp()