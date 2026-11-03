import re
from datetime import date

from app.content import CHANGELOG


def test_changelog_has_five_public_entries():
    assert len(CHANGELOG) == 5


def test_changelog_dates_valid_and_strictly_descending():
    dates = [date.fromisoformat(e["date"]) for e in CHANGELOG]
    assert all(a > b for a, b in zip(dates, dates[1:], strict=False))


def test_changelog_excludes_internal_items():
    for e in CHANGELOG:
        assert "Seed round" not in e["title"]
        assert "Company founded" not in e["title"]


def test_changelog_brand_voice():
    for e in CHANGELOG:
        for text in (e["title"], e["summary"]):
            assert "!" not in text
            assert not re.search(r"\b(bot|robot)\b", text, re.IGNORECASE)


def test_changelog_fields_non_empty():
    for e in CHANGELOG:
        for key in ("date", "title", "summary"):
            assert e[key].strip()
