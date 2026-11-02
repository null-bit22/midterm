
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import ipaddress
import socket

USER_AGENT = "CameraResearchAgent/0.1"
MAX_BYTES = 2_000_000


def safe_url(url):
    """Reject unsupported, local, or private network URLs."""
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return False

    if not parsed.hostname or parsed.username or parsed.password:
        return False

    try:
        addresses = socket.getaddrinfo(parsed.hostname, None)
        return bool(addresses) and all(
            ipaddress.ip_address(info[4][0]).is_global
            for info in addresses
        )
    except (socket.gaierror, ValueError):
        return False


def web_fetch(url, max_characters=12000):
    """
    Fetch a public webpage and extract readable text.

    Returns a dictionary with the result or error.
    """

    print(f"\nFetching: {url}")

    if not safe_url(url):
        return {"url": url, "status": "error",
                "error": "Unsafe or invalid URL"}

    try:
        # Best-effort robots.txt check.
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        robots = RobotFileParser()
        robots.set_url(robots_url)

        try:
            robots.read()
            if not robots.can_fetch(USER_AGENT, url):
                return {"url": url, "status": "blocked",
                        "error": "Disallowed by robots.txt"}
        except Exception:
            pass

        # No automatic redirects: inspect each redirect destination.
        session = requests.Session()
        session.trust_env = False

        for _ in range(5):
            response = session.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=(5, 15),
                stream=True,
                allow_redirects=False
            )

            if response.is_redirect:
                destination = urljoin(
                    url, response.headers.get("Location", "")
                )
                response.close()

                if not safe_url(destination):
                    raise ValueError("Unsafe redirect")

                url = destination
                continue

            break
        else:
            raise ValueError("Too many redirects")

        try:
            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if not any(t in content_type for t in
                       ("text/html", "text/plain", "application/json")):
                return {
                    "url": url,
                    "status": "unsupported",
                    "content_type": content_type
                }

            chunks = []
            total_bytes = 0

            for chunk in response.iter_content(chunk_size=8192):
                total_bytes += len(chunk)

                if total_bytes > MAX_BYTES:
                    raise ValueError("Response exceeds size limit")

                chunks.append(chunk)

            raw = b"".join(chunks)
            encoding = response.encoding or "utf-8"
            body = raw.decode(encoding, errors="replace")

        finally:
            response.close()
            session.close()

        if "text/html" in content_type:
            soup = BeautifulSoup(body, "html.parser")

            title = (
                soup.title.get_text(" ", strip=True)
                if soup.title else ""
            )

            for element in soup(
                ["script", "style", "nav", "footer", "header"]
            ):
                element.decompose()

            text = soup.get_text(separator=" ", strip=True)

        else:
            title = ""
            text = body

        result = {
            "url": url,
            "title": title,
            "status": "success",
            "content_type": content_type,
            "content": text[:max_characters],
            "truncated": len(text) > max_characters
        }

        print(f"Retrieved {len(result['content'])} characters.")
        return result

    except (requests.RequestException, ValueError) as error:
        print(f"Fetch failed: {error}")

        return {
            "url": url,
            "status": "error",
            "error": str(error)
        }


if __name__ == "__main__":
    result = web_fetch("https://example.com")
    print(result)