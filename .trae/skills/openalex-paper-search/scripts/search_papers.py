#!/usr/bin/env python3
"""
OpenAlex Paper Search Script

Search for academic papers using the OpenAlex API.

Usage:
    python search_papers.py --email "you@example.com" --query "machine learning" --limit 5
    python search_papers.py --email "you@example.com" --query "crispr gene editing" --format json
"""

import argparse
import json
import sys
from typing import List, Dict, Any, Optional

import requests


class OpenAlexScholar:
    """Client for the OpenAlex scholarly works API."""

    def __init__(self, email: str):
        """Initialize OpenAlex client.

        Args:
            email: Email address for polite pool access (required)
        """
        if not email:
            raise ValueError("Email address is required for OpenAlex polite pool access")
        self.base_url = "https://api.openalex.org"
        self.email = email

    def _get_request_url(self, endpoint: str) -> str:
        """Construct full request URL."""
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        return f"{self.base_url}/{endpoint}"

    @staticmethod
    def _get_abstract_from_index(abstract_inverted_index: Optional[Dict]) -> str:
        """Reconstruct abstract text from OpenAlex inverted index.

        Args:
            abstract_inverted_index: OpenAlex API inverted index (word -> positions)

        Returns:
            Reconstructed abstract string
        """
        if not abstract_inverted_index:
            return ""

        # Find the maximum position across all words
        max_position = 0
        for positions in abstract_inverted_index.values():
            if positions and max(positions) > max_position:
                max_position = max(positions)

        # Create word array and fill in positions
        words = [""] * (max_position + 1)
        for word, positions in abstract_inverted_index.items():
            for position in positions:
                words[position] = word

        return " ".join(words).strip()

    @staticmethod
    def _format_citation(work: Dict[str, Any]) -> str:
        """Format a paper citation string.

        Args:
            work: Paper work dict from OpenAlex API

        Returns:
            Formatted citation like "Authors (Year). Title. DOI: ..."
        """
        # Get all author names
        authors = [
            authorship.get("author", {}).get("display_name")
            for authorship in work.get("authorships", [])
            if authorship.get("author", {}).get("display_name")
        ]

        # Format author list
        if len(authors) > 3:
            authors_str = f"{authors[0]} et al."
        else:
            authors_str = ", ".join(authors)

        title = work.get("display_name") or work.get("title", "")
        year = work.get("publication_year", "")
        doi = work.get("doi", "")

        citation = f"{authors_str} ({year}). {title}."
        if doi:
            citation += f" DOI: {doi}"

        return citation

    def search_papers(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """Search for papers using OpenAlex API.

        Args:
            query: Search query string
            limit: Maximum number of results (default 8, max 200)

        Returns:
            List of papers with details
        """
        base_url = self._get_request_url("works")

        params = {
            "search": query,
            "per_page": min(limit, 200),
            "select": "id,title,display_name,authorships,cited_by_count,doi,publication_year,biblio,abstract_inverted_index",
            "mailto": self.email,
        }

        headers = {
            "User-Agent": f"OpenAlexScholar/1.0 (mailto:{self.email})"
        }

        try:
            print(f"Searching OpenAlex: \"{query}\" (limit={limit})", file=sys.stderr)
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}", file=sys.stderr)
            if response.status_code == 403:
                print(
                    "Tip: A 403 error typically means you need a valid email for the polite pool.",
                    file=sys.stderr,
                )
            if hasattr(response, "text"):
                print(f"Response body: {response.text[:500]}", file=sys.stderr)
            raise
        except Exception as e:
            print(f"Request error: {e}", file=sys.stderr)
            raise

        papers = []
        for work in results.get("results", []):
            # Reconstruct abstract from inverted index
            abstract = self._get_abstract_from_index(
                work.get("abstract_inverted_index")
            )

            # Extract authors
            authors = []
            for authorship in work.get("authorships", []):
                author = authorship.get("author", {})
                if author:
                    institution = None
                    institutions = authorship.get("institutions", [])
                    if institutions:
                        institution = institutions[0].get("display_name")

                    author_info = {
                        "name": author.get("display_name"),
                        "position": authorship.get("author_position"),
                        "institution": institution,
                    }
                    authors.append(author_info)

            # Extract bibliographic info
            biblio = work.get("biblio", {})
            citation_info = {
                "volume": biblio.get("volume"),
                "issue": biblio.get("issue"),
                "first_page": biblio.get("first_page"),
                "last_page": biblio.get("last_page"),
            }

            paper = {
                "title": work.get("display_name") or work.get("title", ""),
                "abstract": abstract,
                "authors": authors,
                "citations_count": work.get("cited_by_count"),
                "doi": work.get("doi"),
                "publication_year": work.get("publication_year"),
                "citation_info": citation_info,
                "citation_format": self._format_citation(work),
            }
            papers.append(paper)

        return papers

    @staticmethod
    def papers_to_str(papers: List[Dict[str, Any]]) -> str:
        """Format papers list into a human-readable string."""
        lines = []
        for paper in papers:
            lines.append("\n" + "=" * 80)
            lines.append(f"Title: {paper['title']}")
            lines.append(f"Abstract: {paper['abstract']}")
            lines.append("Authors:")
            for author in paper["authors"]:
                institution_str = f" ({author['institution']})" if author.get("institution") else ""
                position_str = f" [{author.get('position', '')}]" if author.get("position") else ""
                lines.append(f"  - {author['name']}{position_str}{institution_str}")
            lines.append(f"Citations: {paper['citations_count']}")
            lines.append(f"Year: {paper['publication_year']}")
            if paper.get("doi"):
                lines.append(f"DOI: {paper['doi']}")
            lines.append(f"Citation: {paper['citation_format']}")
            lines.append("=" * 80)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search for academic papers using the OpenAlex API"
    )
    parser.add_argument(
        "--email", required=True,
        help="Email address for OpenAlex polite pool access"
    )
    parser.add_argument(
        "--query", required=True,
        help="Search query string"
    )
    parser.add_argument(
        "--limit", type=int, default=8,
        help="Maximum number of results (default: 8, max: 200)"
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="Output format: text (human-readable) or json (default: text)"
    )
    parser.add_argument(
        "--titles-only", action="store_true",
        help="Only output paper titles"
    )

    args = parser.parse_args()

    try:
        scholar = OpenAlexScholar(email=args.email)
        papers = scholar.search_papers(query=args.query, limit=args.limit)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not papers:
        print(f"No papers found for query: \"{args.query}\"", file=sys.stderr)
        sys.exit(0)

    if args.titles_only:
        for i, paper in enumerate(papers, 1):
            print(f"{i}. {paper['title']}")
    elif args.format == "json":
        print(json.dumps(papers, ensure_ascii=False, indent=2))
    else:
        print(f"Found {len(papers)} results for: \"{args.query}\"")
        print(OpenAlexScholar.papers_to_str(papers))


if __name__ == "__main__":
    main()
