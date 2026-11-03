import pytest


@pytest.mark.parametrize("path", ["/", "/how-it-works", "/pricing", "/thanks"])
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
