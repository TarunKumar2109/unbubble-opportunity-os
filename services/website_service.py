import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def extract_text_from_website(url: str):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20,
            verify=False,
            allow_redirects=True
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:

        raise Exception(f"Website Error: {e}")

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for tag in soup([
        "script",
        "style",
        "noscript",
        "header",
        "footer",
        "nav",
        "svg",
        "img",
        "iframe"
    ]):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    text = " ".join(text.split())

    return text[:25000]