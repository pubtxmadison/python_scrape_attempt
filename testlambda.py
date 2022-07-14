from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import os


def save_screenshot_to_script_folder(screenshot, filename):
    full_path = f"{os.path.dirname(os.path.abspath(__file__))}/screenshots/"
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    with open(f"{full_path}{filename}", "wb") as f:
        f.write(screenshot)

def write_file_to_s3(bucket, filename, content):
    import boto3
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=filename, Body=content)
    return filename

# with sync_playwright() as p:
#     for browser_type in [p.chromium, p.firefox, p.webkit]:
#         browser = browser_type.launch()
#         page = browser.new_page()
#         page.goto('http://whatsmyuseragent.org/')
#         ss = page.screenshot(full_page=True)
#         save_screenshot_to_script_folder(ss,f"example-{browser_type.name}")
#         browser.close()

def scrape_page(url,id):
  # Originally I just used the default args, I only switched to the below in an attempt to try to fix errors when trying to run as a lambda 
  # without this, and with the original default args it ran locally fine, it runs locally fine like it is, but errors out deployed as a lambda
    browser_args = [
  '--disable-background-networking',
  '--enable-features=NetworkService,NetworkServiceInProcess',
  '--disable-background-timer-throttling',
  '--disable-backgrounding-occluded-windows',
  '--disable-breakpad',
  '--disable-client-side-phishing-detection',
  '--disable-component-extensions-with-background-pages',
  '--disable-default-apps',
  '--disable-dev-shm-usage',
  '--disable-extensions',
  # BlinkGenPropertyTrees disabled due to crbug.com/937609
  '--disable-features=TranslateUI,BlinkGenPropertyTrees,ImprovedCookieControls,SameSiteByDefaultCookies,LazyFrameLoading',
  '--disable-hang-monitor',
  '--disable-ipc-flooding-protection',
  '--disable-popup-blocking',
  '--disable-prompt-on-repost',
  '--disable-renderer-backgrounding',
  '--disable-sync',
  '--force-color-profile=srgb',
  '--metrics-recording-only',
  '--no-first-run',
  '--enable-automation',
  '--password-store=basic',
  '--use-mock-keychain',
  '--disable-zygote',
  '--no-sandbox',
  '--headless',
  '--disable-gpu',
  '--disable-gpu-sandbox',
  '--disable-setuid-sandbox',
  '--single-process',
]
    with sync_playwright() as p:
        for browser_type in [p.chromium]:
            if os.getenv("proxy_address"):
                browser = browser_type.launch(args=browser_args,ignore_default_args = True, proxy={
  "server": os.getenv("proxy_address"),
  "username": os.getenv("proxy_username"),
  "password": os.getenv("proxy_password")
})
            browser = browser_type.launch()
            page = browser.new_page()
            stealth_sync(page)
            page.goto(url, wait_until="networkidle", timeout=None)
            ss = page.screenshot(full_page=True)
            if os.getenv("pmlambda") == "true":
                write_file_to_s3(bucket="polmods", filename=f"{id}.png", content=ss)
            else:
                save_screenshot_to_script_folder(screenshot=ss, filename=f"{id}.png")
            browser.close()
        return id


def handler(event, context):
    if not event:
        return {"error": "No event data"}
    if not event["url"]:
        return {"error": "No url"}
    if not event["id"]:
        return {"error": "No id"}
    scrape_page(url=event["url"],id=event["id"])
    return {"success": "true"}
