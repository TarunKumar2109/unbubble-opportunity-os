from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEYWORDS = [
    "seed fund",
    "grant",
    "funding",
    "challenge",
    "competition",
    "hackathon",
    "award",
    "accelerator",
    "incubator",
    "scheme",
    "program",
    "apply",
    "startup",
    "innovation",
    "fellowship",
    "investor",
    "recognition",
]

IGNORE = [
    "facebook",
    "twitter",
    "linkedin",
    "instagram",
    "youtube",
    "dashboard",
    "profile",
    "notification",
    "my-",
    "login",
    "register",
    "contact",
    "faq",
    "newsletter",
    "blog",
    "resource",
    "logo",
    "disclaimer",
    "privacy",
    "terms",
    "sitemap",
    "search",
    "tel",
    "#",
]


def find_opportunity_links(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20,
        verify=False,
        allow_redirects=True
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    seen = set()

    for a in soup.find_all("a", href=True):

        href = urljoin(url, a["href"])
        title = a.get_text(" ", strip=True)

        combined = (title + " " + href).lower()

        # Ignore unwanted links
        if any(word in combined for word in IGNORE):
            continue

        # Keep only opportunity-related links
        if (
            not any(word in combined for word in KEYWORDS)
            or len(title.strip()) < 5
        ):
            continue

        # Remove duplicates
        if href in seen:
            continue

        seen.add(href)

        title = " ".join(title.split())

        # Skip generic buttons
        if title.lower() in [
            "know more",
            "click here",
            "explore",
            "read more"
        ]:
            continue

        links.append(
            {
                "title": title,
                "url": href
            }
        )

    return sorted(
        links,
        key=lambda x: x["title"].lower()
    )