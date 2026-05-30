---
name: openalex-paper-search
description: "Search for academic papers via the OpenAlex API. Use this skill whenever the user asks to search for papers, find academic references, look up research on a topic, find scholarly articles, or needs academic literature. Even if the user doesn't explicitly say \"OpenAlex\" or \"API\", if they want to search for scientific papers or academic publications, this is the skill to use."
---

# OpenAlex Paper Search

Search for academic papers using the OpenAlex API - a free, open catalog of the global research ecosystem with over 250 million scholarly works.

## When to use this skill

Trigger this skill when the user:

- Asks to "search for papers" or "find papers" on a topic
- Wants academic references or citations
- Needs to look up scholarly articles, research papers, or publications
- Says things like "find research about X", "look up Y papers", "what papers exist on Z"
- Mentions OpenAlex, academic search, or literature review
- Asks for latest research, scientific studies, or peer-reviewed articles

## Quick start

The simplest way to search is using the bundled script:

```bash
python scripts/search_papers.py \
  --email "your-email@example.com" \
  --query "your search query" \
  --limit 5
```

**Important:** OpenAlex requires an email address for the polite pool. Without a valid email, requests will be rate-limited or blocked (HTTP 403). The email should be the user's real email.

## How search works

1. **Construct the request** to `https://api.openalex.org/works` with:
   - `search`: the query string
   - `per_page`: number of results (max 200, default 8)
   - `select`: which fields to return (id, title, authorships, cited_by_count, doi, publication_year, biblio, abstract_inverted_index)
   - `mailto`: user's email for polite pool access

2. **Request headers** must include: `User-Agent: OpenAlexScholar/1.0 (mailto:user@example.com)`

3. **Parse results** - for each work, extract:
   - Title from `display_name` or `title`
   - Abstract by reconstructing from `abstract_inverted_index`
   - Authors with name, position, and institution
   - Citation count (`cited_by_count`)
   - DOI, publication year, and bibliographic info
   - Formatted citation string

## Abstract reconstruction

OpenAlex returns abstracts as inverted indexes - word → list of positions. Reconstruct like this:

```python
def _get_abstract_from_index(abstract_inverted_index):
    if not abstract_inverted_index:
        return ""
    max_pos = max(max(positions) for positions in abstract_inverted_index.values() if positions)
    words = [""] * (max_pos + 1)
    for word, positions in abstract_inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words).strip()
```

## Output format

For each paper, present this structure:

```
================================================================================
Title: [paper title]
Abstract: [reconstructed abstract]
Authors:
  - [author1 name] ([position], [institution])
  - [author2 name] ([position], [institution])
Citations: [cited_by_count]
Year: [publication_year]
DOI: [doi]
Citation: [formatted citation string]
================================================================================
```

## Citation formatting

Format citations as:
`Authors (Year). Title. DOI: [doi]`

- If more than 3 authors: use `First Author et al.`
- Otherwise: list all authors separated by commas

## Bundled resources

- `scripts/search_papers.py` - Complete Python script that calls the OpenAlex API and returns formatted results. Use this as the primary implementation. It handles URL construction, API calls, abstract reconstruction, and output formatting.

## Error handling

- **403 Forbidden**: The email is missing or invalid. Ask the user for a valid email address.
- **Rate limiting**: OpenAlex polite pool requires email. Ensure `mailto` parameter is set.
- **Empty results**: Tell the user no papers matched their query and suggest broader search terms.

## Notes

- OpenAlex is free and open - no API key required
- Results are returned as JSON
- The API supports extensive filtering beyond basic search - see https://docs.openalex.org for advanced usage
- Always ask the user for their email address before making requests, if not already known