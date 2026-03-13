#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from textwrap import dedent

REPO_NAME = "arar-collection-14-scraper"
REPO_DESCRIPTION = (
    "Scraper and dataset for ARAR Collection 14 (Publications of the Institute of Oriental Studies of NAS RA), "
    "created as part of the Open Data Armenia project documenting Armenian heritage worldwide."
)

MAIN_SCRIPT = "main.py"
CSV_FILE = "arar_collection_14.csv"
JSONL_FILE = "arar_collection_14.jsonl"

README_MD = dedent("""
# ARAR Collection 14 Scraper

This repository contains a Python scraper designed to extract **metadata from the Pan-Armenian Digital Library (ARAR)**.

The target source is:

**Collection 14 — Publications of the Institute of Oriental Studies of NAS RA**

The project is part of **Open Data Armenia**, an initiative that aims to collect, organize, and document **Armenian cultural heritage around the world**.

---

## Open Data Armenia

**Open Data Armenia** is a digital humanities initiative focused on building structured datasets about Armenian cultural heritage preserved in institutions worldwide.

The initiative aims to:

- document Armenian heritage across global archives, libraries, museums, and digital collections
- make Armenian cultural data more discoverable
- support digital humanities and historical research
- create reusable open datasets for scholars, students, and developers
- improve visibility of Armenian historical collections around the world

Repositories in this initiative collect **metadata only**, while original materials remain hosted by their custodial institutions and rights holders.

---

## Project Goals

This repository aims to:

- collect structured metadata about Armenian cultural heritage materials
- improve discoverability of publications preserved in ARAR
- support digital humanities research
- document Armenian heritage preserved in global and Armenian digital collections

The project focuses on **metadata extraction only**, not copying or redistributing original materials.

---

## Data Source

**Platform:** Pan-Armenian Digital Library (ARAR)  
**Website:** https://arar.sci.am  
**Collection:** Publications of the Institute of Oriental Studies of NAS RA  
**Collection URL:** https://arar.sci.am/dlibra/collectiondescription/14

ARAR contains hundreds of thousands of digitized objects, including:

- books
- manuscripts
- periodicals
- maps
- posters
- archival publications

---

## What the Scraper Does

The script:

1. accesses ARAR collection result pages
2. retrieves item links
3. visits each item page
4. extracts structured metadata
5. cleans and normalizes fields
6. exports structured datasets

The scraper collects **metadata only** and links back to the original records.

---

## Exported Data Fields

The dataset contains the following fields when available:

| Field | Description |
|------|-------------|
| id | Item identifier |
| publication_id | ARAR publication ID |
| edition_id | ARAR edition ID |
| title | Item title |
| author_creator | Author or creator |
| corporate_creators | Institutional creator |
| contributors | Additional contributors |
| description_abstract | Description or abstract |
| date_period | Publication date |
| year | Extracted year |
| type | Object type |
| place_of_publishing | Publication location |
| publisher | Publisher |
| format | Format description |
| extent | Physical description |
| other_physical_description | Additional physical details |
| call_number | Library call number |
| language | Language |
| general_note | Notes |
| subject_keywords | Keywords |
| url_original_object | Link to the original record |

---

## Repository Structure

main.py  
arar_collection_14.csv  
arar_collection_14.jsonl  
README.md  
LICENSE  
DATA_RIGHTS.md  
requirements.txt  
.gitignore  
CITATION.cff  

---

## Installation

Clone the repository:

git clone REPOSITORY_URL

Create a virtual environment:

python -m venv .venv

Activate the environment:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

---

## Usage

Run the scraper:

python main.py

The script will automatically collect metadata and export:

arar_collection_14.csv  
arar_collection_14.jsonl

If partial saving is enabled in the scraper, temporary partial files may also be created during runtime.

---

## Dataset

The repository includes structured datasets exported in:

- CSV format
- JSONL format

The dataset contains **metadata only** and links back to the original ARAR records.

---

## License

The **code in this repository** is released under the **MIT License**.

See the `LICENSE` file for details.

---

## Rights Notice

This repository is part of **Open Data Armenia**.

All copyrights to the original collection materials,
including books, manuscripts, scans, images, institutional descriptions,
and metadata records belong to **their respective owners and custodial institutions**.

This repository **does not claim ownership over the original materials**.

The project only collects and structures publicly available metadata.

Users wishing to reuse original materials should consult the source institution's policies and the relevant rights holders.

For additional details, see `DATA_RIGHTS.md`.

---

## Disclaimer

This project is an independent research effort.

It is **not officially affiliated with the Pan-Armenian Digital Library (ARAR)**, the **Institute of Oriental Studies of NAS RA**, or any holding institution unless explicitly stated.

---

## Author

**Open Data Armenia**

---

## Suggested GitHub Description

Scraper and dataset for ARAR Collection 14 (Publications of the Institute of Oriental Studies of NAS RA), part of the Open Data Armenia project documenting Armenian heritage worldwide.
""")

LICENSE_TXT = dedent("""
MIT License

Copyright (c) 2026 Open Data Armenia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

DATA_RIGHTS_MD = dedent("""
# Data Rights and Ownership

This repository is part of **Open Data Armenia**, an initiative aimed at collecting and organizing information about Armenian heritage around the world.

## Important Rights Statement

The code in this repository is released under the MIT License.

However:

- **All copyrights in the original digital objects, scans, images, texts, and source records belong to their respective owners**
- Rights to the source platform content remain with the original institutions, archives, libraries, museums, publishers, or other rights holders
- This repository does **not** transfer, replace, or override any rights attached to the original materials

## What This Repository Contains

This repository primarily contains:

- scraper code
- extracted metadata
- links back to original records
- documentation for reuse

## Reuse

Before reusing original content beyond metadata, users should verify:

- the rights status of the source material
- the source institution's terms of use
- whether additional permission is required

## Attribution

When possible, please attribute:

- the original source platform
- the holding institution or rights holder
- this repository as a derived metadata collection created within the Open Data Armenia project
""")

GITIGNORE = dedent("""
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# Virtual environments
.venv/
venv/
env/

# IDE
.idea/
.vscode/

# macOS
.DS_Store

# Jupyter
.ipynb_checkpoints/

# Logs
*.log

# Build / dist
build/
dist/
*.egg-info/

# Local temp files
*.tmp
*.bak
""")

REQUIREMENTS_TXT = dedent("""
requests
beautifulsoup4
tqdm
urllib3
""")

CITATION_CFF = dedent("""
cff-version: 1.2.0
title: "arar-collection-14-scraper"
message: "If you use this repository, please cite it as part of the Open Data Armenia project."
type: software
authors:
  - family-names: "Open Data Armenia"
    given-names: "Project"
abstract: "Scraper and dataset for ARAR Collection 14 (Publications of the Institute of Oriental Studies of NAS RA), created as part of the Open Data Armenia project documenting Armenian heritage worldwide."
license: "MIT"
keywords:
  - Armenia
  - Armenian heritage
  - digital humanities
  - metadata
  - scraping
  - ARAR
  - oriental studies
""")

def write_file(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")
    print(f"Created: {path}")

def main():
    write_file("README.md", README_MD)
    write_file("LICENSE", LICENSE_TXT)
    write_file("DATA_RIGHTS.md", DATA_RIGHTS_MD)
    write_file(".gitignore", GITIGNORE)
    write_file("requirements.txt", REQUIREMENTS_TXT)
    write_file("CITATION.cff", CITATION_CFF)

    print()
    print("Done.")
    print("Suggested repo name:", REPO_NAME)
    print("Suggested repo description:", REPO_DESCRIPTION)

if __name__ == "__main__":
    main()