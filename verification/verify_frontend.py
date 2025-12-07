from playwright.sync_api import sync_playwright, expect
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the frontend (using the static server port)
        page.goto("http://localhost:8081")

        # Verify initial state
        try:
            expect(page.get_by_role("heading", name="Image Feature Extraction")).to_be_visible(timeout=5000)
            print("Heading found.")
        except Exception as e:
            print(f"Heading not found: {e}")
            print(page.content()) # Print content for debugging
            browser.close()
            return

        expect(page.get_by_role("button", name="Upload & Process")).to_be_visible()

        # Upload a file
        file_path = os.path.abspath("demo1.jpg")
        page.set_input_files('input[type="file"]', file_path)

        # Click upload button
        page.get_by_role("button", name="Upload & Process").click()

        # Wait for results
        try:
            expect(page.get_by_text("Original Image")).to_be_visible(timeout=30000)
            expect(page.get_by_text("Edges")).to_be_visible()
            expect(page.get_by_text("Contours")).to_be_visible()
            print("Results found.")
        except Exception as e:
             print(f"Results not found: {e}")
             print(page.content())

        # Take screenshot
        page.screenshot(path="verification/verification.png")
        print("Screenshot saved to verification/verification.png")

        browser.close()

if __name__ == "__main__":
    run()
