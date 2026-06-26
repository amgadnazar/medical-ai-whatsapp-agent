from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto("https://web.whatsapp.com")

    input("Scan QR then press Enter...")

    page.wait_for_timeout(5000)

    spans = page.locator("header span")

    print("Spans:", spans.count())

    for i in range(spans.count()):

        try:

            text = spans.nth(i).inner_text()

            if text.strip():

                print(f"[{i}] {text}")

        except:
            pass