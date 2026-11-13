import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('repository_check', Path(__file__).resolve().parents[1] / 'scripts/check_repository.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class RepositoryCheckTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ('.agent', '.agents/skills', 'docs', 'channels/example', '.codex/agents'):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        for name in checker.ENTRIES:
            self.write(name, '# Entry\n')
        self.write('docs/development.md', '# Git и совместная работа\n')
        for name in checker.ENTRIES:
            if name in checker.REDIRECTS:
                self.write_redirect(name)
        self.catalog = {'schema_version': 1, 'skills': []}
        self.save_catalog()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def save_catalog(self):
        self.write('.agent/skill-catalog.json', json.dumps(self.catalog))
        self.write('.agent/skill-catalog.md', checker.render_catalog(self.catalog))

    def write_redirect(self, name):
        owner, _, fragment = checker.REDIRECTS[name].partition('#')
        parent = (self.root / name).parent
        root_link = os.path.relpath(self.root / 'AGENTS.md', parent)
        owner_link = os.path.relpath(self.root / owner, parent) + ('#' + fragment if fragment else '')
        return self.write(name, f'# Entry\n\n[Start]({root_link}) · [Owner]({owner_link}).\n')

    def add_skill(self, name='ytv-test'):
        entry = {'name': name, 'path': f'.agents/skills/{name}/SKILL.md',
                 'description': 'Test a documented route.', 'stages': [], 'intents': []}
        self.catalog['skills'].append(entry)
        self.write(entry['path'], f'---\nname: {name}\ndescription: "{entry["description"]}"\n---\n\n# Test\n')
        self.save_catalog()
        return entry

    def errors(self, **kwargs):
        return checker.check(self.root, **kwargs)[0]

    def test_valid_current_entries_and_skill_catalog(self):
        self.add_skill()
        errors, documents, skills = checker.check(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(documents, 9)
        self.assertEqual(skills, 1)

    def test_historical_agent_notes_are_not_inputs_but_current_channel_links_are_checked(self):
        self.write('.agent/old-ledger.md', '[historical](missing.md)\n')
        self.write('archive/old.md', '[historical](missing.md)\n')
        self.write('channels/example/episodes/old.md', '[historical](missing.md)\n')
        self.write('channels/example/AGENTS.md', '[current](missing.md)\n')
        errors = self.errors()
        self.assertEqual(len(errors), 1)
        self.assertIn('channels/example/AGENTS.md', errors[0])

    def test_current_entrypoints_include_onboarding_profiles_and_channel_portals(self):
        for name in ('ONBOARDING.md', '.agent/README.md', '.agent/documentation-index.md',
                     'channels/example/PROFILE.md',
                     'channels/lowercase/profile.md', 'channels/example/README.md', 'channels/README.md'):
            with self.subTest(name=name):
                original = (self.root / name).read_text() if (self.root / name).exists() else '# Entry\n'
                path = self.write(name, '[missing](missing.md)\n')
                errors = self.errors()
                self.assertTrue(any(name in error and 'missing link' in error for error in errors))
                path.write_text(original, encoding='utf-8')

    def test_all_legacy_entrances_are_checked_as_navigation_only(self):
        for name, target in checker.REDIRECTS.items():
            with self.subTest(name=name):
                owner, _, fragment = target.partition('#')
                if not (self.root / owner).exists():
                    self.write(owner, '# ' + (fragment or 'Owner') + '\n')
                elif fragment and fragment not in checker.markdown_anchors((self.root / owner).read_text()):
                    with (self.root / owner).open('a') as stream:
                        stream.write('\n# ' + fragment + '\n')
                path = self.write_redirect(name)
                self.assertEqual(self.errors(), [])
                original = path.read_text()
                path.write_text(original + '\nShort may omit the narrative loop.\n')
                self.assertTrue(any('compatibility entry' in error for error in self.errors()))
                path.write_text(original)

    def test_redirect_cannot_point_at_a_competing_existing_owner(self):
        path = self.root / '.agent/README.md'
        path.write_text('# Entry\n\n[Start](../AGENTS.md) · [Old rules](../README.md).\n')
        self.assertTrue(any('compatibility entry' in error for error in self.errors()))

    def test_profile_case_variants_follow_actual_filesystem_identity(self):
        upper = self.write('channels/example/PROFILE.md', '[missing](upper-missing.md)\n')
        lower = upper.with_name('profile.md')
        case_insensitive = lower.exists() and upper.samefile(lower)
        if not case_insensitive:
            self.write('channels/example/profile.md', '[missing](lower-missing.md)\n')
        errors = self.errors()
        self.assertEqual(len(errors), 1 if case_insensitive else 2)
        self.assertTrue(any('PROFILE.md' in error and 'upper-missing.md' in error for error in errors))
        if not case_insensitive:
            self.assertTrue(any('profile.md' in error and 'lower-missing.md' in error for error in errors))

    def test_missing_same_page_and_cross_page_anchors_fail(self):
        self.write('README.md', '# Entry\n[here](#absent) [there](AGENTS.md#absent)\n')
        errors = self.errors()
        self.assertEqual(len(errors), 2)
        self.assertTrue(all('missing heading anchor' in error for error in errors))

    def test_unicode_repeated_and_explicit_anchors(self):
        self.write('docs/guide.md', '# Git и совместная работа\n\n## Repeat\n\n## Repeat\n\n'
                   'Setext title\n------------\n\n<a id="manual"></a>\n')
        self.write('README.md', '[Unicode](docs/guide.md#git-и-совместная-работа)\n'
                   '[duplicate](docs/guide.md#repeat-1) [setext](docs/guide.md#setext-title)\n'
                   '[explicit](docs/guide.md#manual)\n')
        self.assertEqual(self.errors(), [])
        self.write('README.md', '[missing duplicate](docs/guide.md#repeat-2)\n')
        self.assertEqual(len(self.errors()), 1)

    def test_fenced_examples_and_inline_code_are_not_links_or_headings(self):
        self.write('README.md', '# Entry\n\n```markdown\n# Hidden\n[example](absent.md)\n```\n'
                   '~~~markdown\n[example](other.md)\n~~~\n'
                   '`[inline](missing.md)` and ``[inline](missing.md)``\n')
        self.assertEqual(self.errors(), [])
        with (self.root / 'README.md').open('a', encoding='utf-8') as stream:
            stream.write('[real](#hidden)\n')
        errors = self.errors()
        self.assertEqual(len(errors), 1)
        self.assertIn('README.md:11:', errors[0])

    def test_fences_close_only_with_matching_marker_and_sufficient_width(self):
        self.write('README.md', '# Entry\n````markdown\n```\n~~~\n[example](missing.md)\n````\n')
        self.assertEqual(self.errors(), [])

    def test_full_collapsed_and_shortcut_reference_links_check_the_target(self):
        self.write('README.md', '# Entry\n[full][guide]\n[guide][]\n[guide]\n'
                   '[guide]: docs/missing.md "title"\n')
        self.assertEqual(len(self.errors()), 3)
        self.write('docs/missing.md', '# Found\n')
        self.assertEqual(self.errors(), [])

    def test_encoded_paths_parentheses_titles_and_external_urls(self):
        self.write('docs/with space(1).md', '# Heading\n')
        self.write('README.md', '[encoded](docs/with%20space(1).md#heading "Title")\n'
                   '[angle](<docs/with space(1).md#heading>)\n'
                   '[external](https://example.invalid/absent#heading) [cdn](//example.invalid/file)\n')
        self.assertEqual(self.errors(), [])

    def test_snapshot_inventory_proves_path_existence_but_not_anchor(self):
        self.write('README.md', '[path](docs/remote.md) [heading](docs/remote.md#chapter)\n')
        errors = self.errors(known_paths=['docs/remote.md'])
        self.assertEqual(len(errors), 1)
        self.assertIn('unverified anchor', errors[0])
        self.write('docs/remote.md', '# Chapter\n')
        self.assertEqual(self.errors(known_paths=['docs/remote.md']), [])

    def test_links_cannot_leave_repository_even_with_known_paths(self):
        self.write('README.md', '[escape](../private.md)\n')
        errors = self.errors(known_paths=['../private.md'])
        self.assertEqual(len(errors), 1)
        self.assertIn('leaves repository', errors[0])

    def test_stale_catalog_is_rejected_without_rewriting_it(self):
        self.add_skill()
        path = self.write('.agent/skill-catalog.md', '# Unrelated catalog\n')
        before = path.read_bytes()
        self.assertEqual(len(self.errors()), 1)
        self.assertEqual(path.read_bytes(), before)
        self.save_catalog()
        self.assertEqual(self.errors(), [])

    def test_declared_channel_context_references_are_checked_without_traversing_archives(self):
        self.write('channels/example/channel.json', json.dumps({'context_references': [
            {'path': 'Shared/Recipes/current.md', 'stages': ['render']},
        ]}))
        self.write('Shared/Recipes/current.md', '[bad](absent.md) [history](old.md)\n')
        self.write('Shared/Recipes/old.md', '[historical](missing.md)\n')
        errors = self.errors()
        self.assertEqual(len(errors), 1)
        self.assertIn('Shared/Recipes/current.md', errors[0])
        self.write('Shared/Recipes/absent.md', '# Found\n')
        self.assertEqual(self.errors(), [])

    def test_declared_reference_requires_local_markdown_for_content_verification(self):
        self.write('channels/example/channel.json', json.dumps({'context_references': [
            {'path': 'Shared/current.md'},
        ]}))
        errors = self.errors(known_paths=['Shared/current.md'])
        self.assertEqual(len(errors), 1)
        self.assertIn('Shared/current.md', errors[0])
        self.write('channels/example/channel.json', json.dumps({'context_references': [{'path': 'image.png'}]}))
        self.assertEqual(len(self.errors()), 1)

    def test_description_drift_is_detected_even_with_fresh_catalog_view(self):
        entry = self.add_skill()
        self.catalog['skills'][0]['description'] = 'Use a different route.'
        self.save_catalog()
        errors = self.errors()
        self.assertEqual(len(errors), 1)
        self.assertIn(entry['path'], errors[0])
        self.assertIn('description', errors[0])

    def test_body_cannot_supply_missing_frontmatter(self):
        entry = self.add_skill()
        self.write(entry['path'], '# Skill\nname: ytv-test\ndescription: Test a documented route.\n')
        errors = self.errors()
        self.assertEqual(len(errors), 2)

    def test_duplicate_skills_fail_even_when_names_and_paths_match(self):
        entry = self.add_skill()
        self.catalog['skills'].append(entry.copy())
        self.save_catalog()
        errors = self.errors()
        self.assertEqual(len(errors), 1)
        self.assertIn('duplicate', errors[0])

    def test_invalid_catalog_returns_failure_instead_of_traceback(self):
        for content in ('{', '{}', '{"skills": null}', '{"skills": [{}]}'):
            with self.subTest(content=content):
                self.write('.agent/skill-catalog.json', content)
                self.assertEqual(len(self.errors()), 1)


if __name__ == '__main__':
    unittest.main()
