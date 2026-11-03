import pytest


@pytest.mark.parametrize("path", ["/", "/how-it-works", "/pricing", "/changelog", "/thanks"])
def test_pages_render(client, path):
    res = client.get(path)
    assert res.status_code == 200
    assert "deleg" in res.text


def test_pricing_lists_all_plans(client):
    html = client.get("/pricing").text
    for name in ("Starter", "Team", "Enterprise"):
        assert name in html


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_pricing_faq_present_and_below_plans(client):
    from app.content import FAQ

    html = client.get("/pricing").text
    for question, answer in FAQ:
        assert question in html
        assert answer in html
    assert html.index('class="faq"') > html.index('id="plan-enterprise"')


def test_faq_text_pinned_to_wiki():
    from app.content import FAQ

    assert len(FAQ) == 4
    assert (
        "No. Database and warehouse access is read-only. "
        "Changes ship only through pull requests and your CI."
    ) in [a for _, a in FAQ]


def test_pricing_has_exactly_one_most_popular_badge(client):
    html = client.get("/pricing").text
    assert html.count("Most popular") == 1


def test_most_popular_badge_is_inside_team_plan(client):
    html = client.get("/pricing").text
    start = html.index('id="plan-team"')
    team = html[start : html.index("</article>", start)]
    assert "Most popular" in team
    assert "plan--popular" in html[html.rindex("<article", 0, start) : start]


def test_exactly_one_popular_plan_and_it_is_team():
    from app.content import PLANS

    popular = [p["id"] for p in PLANS if p["popular"]]
    assert popular == ["team"]


def test_changelog_public_entries_newest_first(client):
    html = client.get("/changelog").text
    for title in (
        "Jira adapter",
        "AI code review",
        "Warehouse research tools",
        "pi harness support",
        "Private beta",
    ):
        assert title in html
    assert html.index("Jira adapter") < html.index("Private beta")
    assert "28 Oct 2026" in html
    assert "Seed round" not in html
    assert "Company founded" not in html


@pytest.mark.parametrize("path", ["/", "/how-it-works", "/pricing", "/thanks", "/changelog"])
def test_changelog_linked_from_nav_and_footer(client, path):
    html = client.get(path).text
    assert html.count('href="/changelog"') >= 2
    nav = html[html.index("<nav>") : html.index("</nav>")]
    assert nav.index("Pricing") < nav.index("Changelog") < nav.index("Join waitlist")
    footer = html[html.index('<footer class="footer">') :]
    assert 'class="footer-links"' in footer
    assert 'href="/changelog"' in footer
    assert "&copy; 2026 deleg8 · AI employees, delegated." in footer


def test_url_global_applies_base_path():
    from app.main import templates

    assert templates.env.globals["url"]("/changelog") == "/changelog"
