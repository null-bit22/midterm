
from ddgs import DDGS


def web_search(query, max_results=5):
    """
    Search the internet and return structured results.

    Args:
        query: Search phrase.
        max_results: Maximum number of results.

    Returns:
        List of dictionaries containing search results.
    """

    print(f"\nSearching: {query}")

    try:
        results = DDGS().text(
            query,
            region="us-en",
            max_results=max_results,
            backend="auto"
        )

        formatted_results = []

        for result in results:
            formatted_results.append({
                "title": result.get("title"),
                "url": result.get("href"),
                "snippet": result.get("body"),
                "search_query": query
            })

        print(f"Found {len(formatted_results)} results.")

        return formatted_results

    except Exception as error:
        print(f"Search failed: {error}")
        return []


if __name__ == "__main__":

    query = (
        "Washington State DOT traffic camera "
        "open data API"
    )

    results = web_search(query)

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Snippet:", result["snippet"])