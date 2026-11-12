import unittest
import xml.etree.ElementTree as ET
from main import app


class TestLoqinSeoAndRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_canonical_routes_return_200(self):
        canonical_routes = [
            ('/', 'Loqin | VIT Hostel Wi-Fi Auto Login for Windows & macOS'),
            ('/download', 'Download Loqin | VIT Hostel Wi-Fi Client for Windows & macOS'),
            ('/windows', 'Loqin for Windows | VIT Hostel Wi-Fi Auto Login Setup Guide'),
            ('/macos', 'Loqin for macOS | VIT Hostel Wi-Fi Client Setup Guide'),
            ('/troubleshooting', 'Loqin Troubleshooting | Fix VIT Hostel Wi-Fi & Captive Portal Issues'),
            ('/faq', 'Loqin FAQ | VIT Hostel Wi-Fi Client Frequently Asked Questions'),
            ('/privacy', 'Privacy Policy | Loqin Client'),
            ('/license', 'GNU GPLv3 License | Loqin Open Source Project'),
        ]

        for route, expected_title in canonical_routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200, f"{route} failed with status {response.status_code}")
                html = response.get_data(as_text=True)
                self.assertIn('<link rel="canonical" href="https://loqin.aayushsrivastava.com', html)
                self.assertIn(f'<title>{expected_title}</title>', html)
                self.assertIn('name="description"', html)
                self.assertIn('property="og:image"', html)
                self.assertIn('name="twitter:card"', html)

    def test_download_thanks_page(self):
        response = self.client.get('/download/thanks')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('content="noindex, follow"', html)
        self.assertIn('name="loqin-installer"', html)

    def test_legacy_thank_you_redirects(self):
        response = self.client.get('/thank-you?os=windows')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/download/thanks', response.headers.get('Location', ''))

    def test_installer_redirects_to_github(self):
        win_resp = self.client.get('/installer?os=windows')
        self.assertEqual(win_resp.status_code, 302)
        self.assertIn('Install_Loqin.exe', win_resp.headers.get('Location', ''))

        mac_resp = self.client.get('/installer?os=mac')
        self.assertEqual(mac_resp.status_code, 302)
        self.assertIn('Install_Loqin_macOS.dmg', mac_resp.headers.get('Location', ''))

    def test_not_found_returns_404(self):
        response = self.client.get('/nonexistent-test-route-404')
        self.assertEqual(response.status_code, 404)
        html = response.get_data(as_text=True)
        self.assertIn('404', html)
        self.assertIn('That page has wandered off the network.', html)

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.content_type)
        text = response.get_data(as_text=True)
        self.assertIn('User-agent: *', text)
        self.assertIn('Allow: /', text)
        self.assertIn('Disallow: /download/thanks', text)
        self.assertIn('Disallow: /installer', text)
        self.assertIn('Sitemap: https://loqin.aayushsrivastava.com/sitemap.xml', text)

    def test_sitemap_xml(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn('xml', response.content_type)

        xml_data = response.get_data()
        root = ET.fromstring(xml_data)

        # XML namespace for sitemaps
        namespace = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('sm:url/sm:loc', namespace)]

        expected_canonical_urls = [
            'https://loqin.aayushsrivastava.com/',
            'https://loqin.aayushsrivastava.com/download',
            'https://loqin.aayushsrivastava.com/windows',
            'https://loqin.aayushsrivastava.com/macos',
            'https://loqin.aayushsrivastava.com/troubleshooting',
            'https://loqin.aayushsrivastava.com/faq',
            'https://loqin.aayushsrivastava.com/privacy',
            'https://loqin.aayushsrivastava.com/license',
        ]

        self.assertEqual(len(urls), len(expected_canonical_urls))
        for url in expected_canonical_urls:
            self.assertIn(url, urls)

    def test_jsonld_schemas(self):
        # Homepage should contain SoftwareApplication schema
        home_resp = self.client.get('/')
        self.assertIn('"@type": "SoftwareApplication"', home_resp.get_data(as_text=True))

        # FAQ page should contain FAQPage schema
        faq_resp = self.client.get('/faq')
        self.assertIn('"@type": "FAQPage"', faq_resp.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
