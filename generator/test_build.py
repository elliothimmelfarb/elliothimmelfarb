import glob, os, re, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
import build

CONTENT = {"live": [], "games": [], "work": [], "drops": 129}


class Build(unittest.TestCase):
    def test_private_repo_never_gets_a_card(self):
        repos = [{"name": "a", "private": False}, {"name": "b", "private": True}]
        self.assertEqual([r["name"] for r in build.public_cards(["b", "a", "c"], repos)], ["a"])

    def test_cards_keep_the_chosen_order(self):
        repos = [{"name": "a"}, {"name": "b"}]
        self.assertEqual([r["name"] for r in build.public_cards(["b", "a"], repos)], ["b", "a"])

    def test_readme_has_no_em_dash(self):
        self.assertNotIn("—", build.readme(CONTENT, [], 1))

    def test_a_wide_site_gets_a_phone_version(self):
        c = dict(CONTENT, live=[{"id": "x", "name": "X", "url": "https://x.test", "line": "y", "wide": True}])
        self.assertIn("live-x-phone-dark.svg", build.readme(c, [], 1))

    def test_blurb_stops_at_the_first_sentence(self):
        self.assertEqual(build.blurb("One tag. The rest."), "One tag")

    def test_blurb_drops_em_dashes(self):
        self.assertNotIn("\u2014", build.blurb("a \u2014 b"))

    def test_every_generated_style_block_balances(self):
        for name in glob.glob(os.path.join(build.ROOT, "assets/*.svg")):
            with open(name) as f:
                for css in re.findall(r"<style>(.*?)</style>", f.read(), re.S):
                    self.assertEqual(css.count("{"), css.count("}"), name)

    def test_card_escapes_a_description(self):
        svg = build.card(build.THEMES["dark"], {"name": "a", "description": "x < y & z"})
        self.assertIn("x &lt; y &amp; z", svg)


if __name__ == "__main__":
    unittest.main()
