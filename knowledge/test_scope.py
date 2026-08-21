from ingest_site import is_same_site_link, normalise_url


def test_allowed_urls():
    assert normalise_url("https://www.ron-jackson.co.uk/projects.html") == "https://www.ron-jackson.co.uk/projects.html"
    assert normalise_url("http://ron-jackson.co.uk/contact.html") == "https://www.ron-jackson.co.uk/contact.html"


def test_external_urls_blocked():
    assert normalise_url("https://github.com/Jaron1978") is None
    assert normalise_url("https://www.linkedin.com/in/ronjackson") is None
    assert normalise_url("https://www.credly.com/users/example") is None


def test_relative_links():
    base = "https://www.ron-jackson.co.uk/projects.html"
    assert is_same_site_link(base, "project-02.html") == "https://www.ron-jackson.co.uk/project-02.html"
    assert is_same_site_link(base, "https://github.com/Jaron1978/RonBot-repo") is None


def test_assets_blocked():
    assert normalise_url("https://www.ron-jackson.co.uk/styles.css") is None
    assert normalise_url("https://www.ron-jackson.co.uk/ronbot.png") is None
