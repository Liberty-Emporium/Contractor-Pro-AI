"""
Tests for Contractor Pro AI
Covers: health, auth, slug utils, trial flow, public routes, security headers
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('DATABASE_URL', '')

import app as cpa


@pytest.fixture
def client(tmp_path):
    cpa.app.config['TESTING'] = True
    cpa.app.config['SECRET_KEY'] = 'test-secret-key'
    cpa.DATA_DIR = str(tmp_path)
    cpa.DB_PATH = str(tmp_path / 'test.db')
    with cpa.app.test_client() as c:
        with cpa.app.app_context():
            cpa.init_db()
        yield c


# ── Health ────────────────────────────────────────────────────────────────────

def test_healthz_returns_ok(client):
    res = client.get('/healthz')
    assert res.status_code == 200
    assert b'ok' in res.data.lower()

def test_health_returns_json(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data is not None
    assert 'status' in data or 'db' in data


# ── Public pages ──────────────────────────────────────────────────────────────

def test_index_returns_200(client):
    res = client.get('/')
    assert res.status_code == 200

def test_login_page_returns_200(client):
    res = client.get('/login')
    assert res.status_code == 200

def test_pricing_page_returns_200(client):
    res = client.get('/pricing')
    assert res.status_code == 200

def test_about_page_returns_200(client):
    res = client.get('/about', follow_redirects=True)
    assert res.status_code == 200

def test_wizard_page_returns_200(client):
    res = client.get('/wizard')
    assert res.status_code == 200


# ── Auth ──────────────────────────────────────────────────────────────────────

def test_dashboard_requires_login(client):
    res = client.get('/dashboard', follow_redirects=False)
    assert res.status_code in (302, 401)

def test_bids_requires_login(client):
    res = client.get('/bids', follow_redirects=False)
    assert res.status_code in (302, 401)

def test_settings_requires_login(client):
    res = client.get('/settings', follow_redirects=False)
    assert res.status_code in (302, 401)

def test_login_wrong_credentials(client):
    res = client.post('/login', data={
        'username': 'nobody',
        'password': 'badpass'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'invalid' in res.data.lower() or b'incorrect' in res.data.lower() or b'wrong' in res.data.lower()


# ── Slug utilities ────────────────────────────────────────────────────────────

def test_slugify_basic():
    assert cpa.slugify('Hello World') == 'hello-world'

def test_slugify_special_chars():
    assert cpa.slugify('Jay\'s Contracting!') == 'jay-s-contracting'

def test_slugify_max_length():
    long = 'a' * 100
    assert len(cpa.slugify(long)) <= 40

def test_slugify_empty_string():
    result = cpa.slugify('')
    assert isinstance(result, str)

def test_validate_slug_valid():
    # _validate_slug returns cleaned slug string, not bool
    result = cpa._validate_slug('hello-world')
    assert result == 'hello-world'

def test_validate_slug_strips_special_chars():
    # Spaces and special chars are removed (not replaced with hyphens)
    result = cpa._validate_slug('Hello World!')
    assert isinstance(result, str)
    assert result == result.lower()
    assert ' ' not in result and '!' not in result

def test_validate_slug_rejects_empty():
    with pytest.raises(ValueError):
        cpa._validate_slug('')

def test_validate_slug_rejects_reserved_words():
    with pytest.raises(ValueError):
        cpa._validate_slug('admin')


# ── Security headers ──────────────────────────────────────────────────────────

def test_x_content_type_header_present(client):
    res = client.get('/')
    assert 'X-Content-Type-Options' in res.headers

def test_x_frame_options_present(client):
    res = client.get('/')
    assert 'X-Frame-Options' in res.headers


# ── Sitemap / robots ──────────────────────────────────────────────────────────

def test_sitemap_returns_xml(client):
    res = client.get('/sitemap.xml')
    assert res.status_code == 200

def test_robots_returns_200(client):
    res = client.get('/robots.txt')
    assert res.status_code == 200
