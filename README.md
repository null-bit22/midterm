# CSBS 431 Midterm
Patrick Neill - AI Agent Exploration

## Project Purpose
Research AI agents and begin developing my own AI agent to help me source traffic camera data for my Capstone project.

## Learning Goal
Develop my own AI agent to execute search queries, analyze different sources for relevant data, and formtat the data into JSON/CSV.

## Scope

### Project title and path
Intro to AI agents connecting with Capstone project

### Starting point
I know what AI agents are and what they do, such as analyzing user prompts, and executing functions to return useful data for the user.

### Learning goal: What will you practice, understand more deeply, or learn
I will prioritize understanding how AI agents operate under the hood. I want to learn about different tools, different ways to incorprorate different models, and begin creating my own AI agent to help with my Capstone project.

### Minimum result: List two or three specific outcomes you will demonstrate.
Create an AI agent to choose and execute various internet searches to find possible candidate websites for traffic camera data, possibly formatting the data into JSON or CSV format.

### Tools and data: What do you need, and where will it come from?
- **Python:** Primary programming language used to develop the research workflow and integrate the different components.
- **Ollama:** Allows large language models to run locally without requiring a paid API.
- **Qwen3:8b:** Local language model used to generate search queries and analyze potential sources.
- **DuckDuckGo (`ddgs`):** Provides internet search functionality without requiring an API key.
- **Requests:** Python library used to retrieve webpage content.
- **BeautifulSoup:** Parses HTML and extracts readable text from websites.
- **JSON:** Used to store structured research findings.

### Verification: How will you check your result or explanation?
AI agent results will be verified through cross referencing, ensuring the links or data that the model returns are accurate and up-to-date.

## File Descriptions
```text
.
├── agent/
│   └── researcher.py
├── tools/
│   ├── web_search.py
│   └── web_fetch.py
├── exports/
│   ├── discovered_sources.json
│   ├── cameras.json
│   └── cameras.csv
├── database/
├── main.py
├── requirements.txt
└── README.md
```
**`agent/researcher.py`**

Contains the main research workflow. Uses Qwen through Ollama to generate search queries, analyze search results, identify candidate websites, and examine downloaded webpage content.

**`tools/web_search.py`**

Uses DuckDuckGo to perform internet searches. Returns structured search results containing titles, URLs, snippets, and the original search queries.

**`tools/web_fetch.py`**

Retrieves webpage content using Requests and extracts readable text using BeautifulSoup.

**`exports/discovered_sources.json`**

Stores research results, including the research location, search queries, candidate websites, and webpage inspection findings.

**`exports/cameras.json` and `exports/cameras.csv`**

Reserved for future exports of actual camera data. The current implementation does not populate these files.

**`database/`**

Reserved for future storage and management of collected camera information.

**`main.py`**

Entry point for the program. Specifies the research location and starts the workflow.

**`requirements.txt`**

Lists the required Python packages.

## Instructions

Install dependencies using:

```bash
pip install -r requirements.txt
```
### Ollama Setup

Install Ollama from https://ollama.com.

Download the Qwen3:8b model:

```bash
ollama pull qwen3:8b
```

Ensure Ollama is running before executing the research program.

### Running the Program

Open `main.py` and specify a research location:

```python
from agent.researcher import run_research

if __name__ == "__main__":
    run_research(
        state="Washington",
        county="Clark"
    )
```

Run the program from the project root:

```bash
python main.py
```

The program will generate searches for the selected location, identify potentially useful websites, inspect selected pages, and save its findings.

### Output

Research findings are saved to:

```text
exports/discovered_sources.json
```

The JSON file contains:
- Research location and date.
- Generated search queries.
- Number of search results and candidate sources.
- Selected source names and URLs.
- Source descriptions and confidence ratings.
- Webpage inspection results, where available.
- Indications of whether datasets, APIs, coordinates, or camera headings are mentioned.

## How the Research Workflow Operates

The current implementation consists of five stages.

### Stage 1 — Query Generation
The program sends the research location and camera categories to Qwen. The model generates eight targeted search queries intended to discover relevant government resources, datasets, and APIs.

### Stage 2 — Internet Search
Python executes each generated query using DuckDuckGo, retrieving up to five results per query. Duplicate URLs are removed.

Each result contains the webpage title, URL, search snippet, and associated query.

### Stage 3 — Source Analysis
Qwen receives the search results and evaluates which websites appear potentially useful based on their titles, URLs, and snippets.

The model returns a list of candidate sources. Python validates these URLs against the original search results to prevent the model from introducing unsupported links.

### Stage 4 — Webpage Inspection
The program selects up to five candidate sources and retrieves their webpage contents.

Qwen then analyzes the extracted text to determine whether the webpages provide evidence of camera data, datasets, APIs, camera coordinates, or viewing directions.

### Stage 5 — Export Results
The program saves the collected findings and webpage inspection results into `discovered_sources.json`.

## Current Results and Verification

| Check | Expected Result | Observed Result | Conclusion |
| :--- | :--- | :--- | :--- |
| **Normal: Generate search queries** | Qwen generates 8 relevant search queries for Clark County, Washington. | Qwen generated 8 queries targeting transportation departments, public CCTV, GIS portals, and ALPR cameras. | **Pass:** All 8 queries were generated. |
| **Normal: Execute internet searches** | DuckDuckGo returns relevant search results and duplicate URLs are removed. | The program collected 22 unique search results from 8 queries. | **Pass:** Search results were collected and deduplicated. |
| **Normal: Identify candidate sources** | Qwen analyzes search result metadata and identifies potentially useful sources. | Qwen identified 5 candidate websites from the 22 search results. | **Pass:** Candidate sources were generated, but their relevance requires further verification. |
| **Normal: Inspect webpages** | The program retrieves webpage contents and analyzes them using Qwen. | Several webpages returned readable text, including one with 4,223 characters. | **Pass:** Webpage retrieval and inspection worked for supported pages. |
| **Edge case: Search returns no results** | The program handles an unsuccessful search without stopping the workflow. | One search returned "Search failed: No results found." The program continued executing subsequent searches. | **Pass:** The workflow continued despite the unsuccessful search. |
| **Failure: Website retrieval error** | The program handles connection errors without crashing. | One website returned an SSL error (`WRONG_VERSION_NUMBER`). The program continued inspecting other sources. | **Pass:** The error was handled, although the website could not be inspected. |
| **Limitation: Limited webpage content** | The program retrieves enough content for meaningful inspection. | An ArcGIS open-data portal returned only 34 characters. | **Limitation:** Some websites do not expose useful content through basic HTML retrieval. |
| **Normal: Export findings** | Research findings and inspection results are saved to a JSON file. | `discovered_sources.json` was generated and contained the new inspection objects. | **Pass:** Research findings were exported successfully. |
