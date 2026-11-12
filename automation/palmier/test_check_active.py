import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import check_active


class CheckActiveTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / 'project.palmier'
        self.project.mkdir()
        self.alias = self.root / 'old.palmier'
        self.alias.symlink_to(self.project, target_is_directory=True)
        self.other = self.root / 'other.palmier'
        self.other.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_physical_identity_including_broken_and_relative_paths(self):
        self.assertTrue(check_active.same_project(str(self.alias), str(self.project)))
        self.assertFalse(check_active.same_project(str(self.other), str(self.project)))
        self.assertFalse(check_active.same_project(str(self.root / 'missing'), str(self.project)))
        self.assertFalse(check_active.same_project('project.palmier', str(self.project)))
        self.assertFalse(check_active.same_project(None, str(self.project)))

    def invoke(self, projects, inventory, timeline):
        connection = mock.Mock()
        connection.read_tool.side_effect = [projects, inventory, timeline]
        with mock.patch.object(check_active, 'PalmierConnection', return_value=connection), \
             mock.patch('sys.argv', ['check_active', '--project-path', str(self.project), '--timeline-id', 'T1']), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return check_active.main()

    def test_project_and_timeline_guards_still_apply(self):
        project = {'id': 'P1', 'path': str(self.alias), 'isAccessible': True, 'isOpen': True}
        projects = {'projects': [project]}
        inventory = {'timelines': [{'timelineId': 'T1'}]}
        timeline = {'timelineId': 'T1'}
        self.assertEqual(self.invoke(projects, inventory, timeline), 0)
        project['path'] = str(self.other)
        self.assertEqual(self.invoke(projects, inventory, timeline), 1)
        project['path'] = str(self.project)
        timeline['timelineId'] = 'T2'
        self.assertEqual(self.invoke(projects, inventory, timeline), 1)
        timeline['timelineId'] = 'T1'
        inventory['timelines'].append({'timelineId': 'T1'})
        self.assertEqual(self.invoke(projects, inventory, timeline), 1)


if __name__ == '__main__':
    unittest.main()
