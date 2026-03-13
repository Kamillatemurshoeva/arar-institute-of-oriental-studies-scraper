#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://arar.sci.am"
START_URL = "https://arar.sci.am/dlibra/results?q=&action=SimpleSearchAction&type=-6&p=0&qf1=collections:14"
LIST_URL = "https://arar.sci.am/dlibra/results?q=&action=SimpleSearchAction&type=-6&p={}&qf1=collections:14"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en,hy;q=0.9,ru;q=0.8",
}

DELAY = 1.2
MAX_PAGES = 300


def make_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)
    return session


def clean(text):
    if not text:
        return ""
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_html(session, url, retries=3):
    for attempt in range(1, retries + 1):
        try:
            time.sleep(DELAY)
            r = session.get(url, timeout=(20, 90))
            r.raise_for_status()
            return r.text
        except requests.exceptions.RequestException as e:
            print(f"REQUEST FAILED ({attempt}/{retries}): {url} -> {e}")
            time.sleep(2 * attempt)
    return None


def get_ids(url):
    m = re.search(r"/publication/(\d+)/edition/(\d+)", url)
    if m:
        return m.group(1), m.group(2)
    return "", ""


def get_item_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/dlibra/publication/" in href and "/edition/" in href:
            links.append(urljoin(BASE_URL, href))
    return list(dict.fromkeys(links))


def collect_links(session, max_pages=MAX_PAGES):
    all_links = []
    seen = set()
    no_new_pages = 0

    for page in range(max_pages):
        url = LIST_URL.format(page)
        html = get_html(session, url)
        if not html:
            print("Skipping bad list page:", page)
            continue

        links = get_item_links(html)
        new_count = 0

        for link in links:
            pub_id, ed_id = get_ids(link)
            key = ed_id or pub_id or link
            if key not in seen:
                seen.add(key)
                all_links.append(link)
                new_count += 1

        print(f"Page {page}: +{new_count} links (total: {len(all_links)})")

        if new_count == 0:
            no_new_pages += 1
        else:
            no_new_pages = 0

        if no_new_pages >= 3:
            break

    return all_links


def get_text_lines(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")
    lines = [clean(x) for x in text.split("\n")]
    return [x for x in lines if x]


def slice_object_lines(lines):
    start = None
    for i, line in enumerate(lines):
        if line == "Object":
            start = i
            break

    if start is None:
        return lines

    stop_markers = {
        "Recently viewed",
        "Objects",
        "Collections",
        "Similar",
    }

    result = []
    for line in lines[start:]:
        if line in stop_markers and len(result) > 10:
            break
        result.append(line)

    return result


def first_meta(soup, names):
    for name in names:
        tag = soup.find("meta", attrs={"name": name})
        if tag and tag.get("content"):
            return clean(tag["content"])
        tag = soup.find("meta", attrs={"property": name})
        if tag and tag.get("content"):
            return clean(tag["content"])
    return ""


def build_field_map(lines):
    fields = {}
    current_key = None
    current_value = []

    stop_keys = {
        "Object collections",
        "All available object's versions",
        "Show description in RDF format",
        "Show description in OAI-PMH format",
        "Number of object content hits",
        "Show content",
        "Download",
        "Description",
        "Information",
        "Structure",
        "More",
        "Subscribtion state has been changed.",
        "Error while changing subscribtion state.",
    }

    for line in lines:
        if line in stop_keys:
            continue

        if ":" in line and not line.endswith(":"):
            left, right = line.split(":", 1)
            left = clean(left)
            right = clean(right)
            if left and right and len(left) < 80:
                fields[left] = right
                current_key = None
                current_value = []
                continue

        m = re.match(r"^([A-Za-zԱ-Ֆա-ֆЁёА-Яа-я().'\- /]+):$", line)
        if m:
            if current_key:
                fields[current_key] = clean(" ".join(current_value))
            current_key = m.group(1).strip()
            current_value = []
            continue

        if current_key:
            current_value.append(line)

    if current_key:
        fields[current_key] = clean(" ".join(current_value))

    return fields


def pick_field(fields, names):
    for name in names:
        if name in fields and fields[name]:
            return fields[name]
    return ""


def extract_year(text):
    if not text:
        return None
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", text)
    if m:
        return int(m.group(1))
    return None


def parse_item(session, url):
    html = get_html(session, url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    lines = get_text_lines(html)
    object_lines = slice_object_lines(lines)
    fields = build_field_map(object_lines)

    pub_id, ed_id = get_ids(url)

    title = pick_field(fields, ["Title", "Վերնագիր", "Заглавие", "Название"])
    if not title:
        title = first_meta(soup, ["DC.title", "dc.title", "citation_title", "og:title"])

    creator = pick_field(fields, ["Creator", "Author", "Ստեղծող", "Հեղինակ", "Автор"])
    if not creator:
        creator = first_meta(soup, ["DC.creator", "dc.creator", "citation_author", "author"])

    description = pick_field(fields, ["Abstract", "Description", "Ամփոփում", "Описание", "Table of contents", "Բովանդակություն", "Содержание"])
    if not description:
        description = first_meta(soup, ["DC.description", "dc.description", "description", "og:description"])

    date = pick_field(fields, ["Date of publication", "Date", "Հրատարակության թվական", "Дата"])
    if not date:
        date = first_meta(soup, ["DC.date", "dc.date", "citation_publication_date"])

    place = pick_field(fields, ["Place of publishing", "Place", "Հրատարակման վայր", "Место издания"])
    publisher = pick_field(fields, ["Publisher", "Հրատարակիչ", "Издатель"])
    format_str = pick_field(fields, ["Format", "Ձևաչափ", "Формат"])
    extent = pick_field(fields, ["Extent", "Physical description", "Ծավալ", "Объем"])
    other_physical = pick_field(fields, ["Other physical description", "Другие физические характеристики"])
    call_number = pick_field(fields, ["Call number", "Shelfmark", "Դասիչ", "Շիֆր", "Шифр"])
    language = pick_field(fields, ["Language", "Լեզու", "Язык"])
    note = pick_field(fields, ["General note", "Note", "Ծանոթագրություն", "Примечание"])
    subjects = pick_field(fields, ["Subject and keywords", "Subjects", "Keywords", "Թեմա և հիմնաբառեր", "Ключевые слова"])
    type_value = pick_field(fields, ["Type", "Տեսակ", "Тип"])
    contributor = pick_field(fields, ["Contributor(s)", "Contributor", "Участник", "Ներդրող(ներ)"])
    corporate = pick_field(fields, ["Corporate Creators", "Корпоративный автор"])
    year = extract_year(date)

    record = {
        "id": ed_id or pub_id or url,
        "publication_id": pub_id,
        "edition_id": ed_id,
        "title": title,
        "author_creator": creator,
        "corporate_creators": corporate,
        "contributors": contributor,
        "description_abstract": description,
        "date_period": date,
        "year": year,
        "type": type_value,
        "place_of_publishing": place,
        "publisher": publisher,
        "format": format_str,
        "extent": extent,
        "other_physical_description": other_physical,
        "call_number": call_number,
        "language": language,
        "general_note": note,
        "subject_keywords": subjects,
        "url_original_object": url,
    }

    return record


def save_csv(records, filename):
    if not records:
        return
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def save_jsonl(records, filename):
    if not records:
        return
    with open(filename, "w", encoding="utf-8") as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    session = make_session()

    print("Collecting links...")
    links = collect_links(session)
    print(f"\nTotal links: {len(links)}\n")

    records = []
    for i, url in enumerate(tqdm(links, desc="Scraping"), start=1):
        try:
            record = parse_item(session, url)
            if record:
                records.append(record)
            else:
                print(f"\nWarning: empty metadata for {url}")
        except Exception as e:
            print(f"\nError on {url}: {e}")

        if i % 25 == 0:
            save_csv(records, "arar_collection_14_partial.csv")
            save_jsonl(records, "arar_collection_14_partial.jsonl")

    save_csv(records, "arar_collection_14.csv")
    save_jsonl(records, "arar_collection_14.jsonl")
    print(f"\nSaved {len(records)} records")


if __name__ == "__main__":
    main()