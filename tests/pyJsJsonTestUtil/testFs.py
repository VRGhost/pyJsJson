"""Virtual filesystem overlay to mock file access."""

import json
import os

import mock_open

ORIG_OS_PATH = {
    'isdir': os.path.isdir,
    'isfile': os.path.isfile,
}

orig_builtins_open = open


class TestFs:
    """Unittest filesystem overlay.

    Always specify a 'root' folder that is NOT normally present on the system.
    Otherwise, the pytest will fail as the real filesystem access is required to run the test process.
    """

    def __init__(self, root: str):
        self.root = FakeDir(parent=None, name=root)
        self._mockOpen = mock_open.MockOpen()

    def activate(self, mocker):
        mocker.patch.object(os.path, 'isdir', side_effect=self._mockedOsPathIsdir)
        mocker.patch.object(os.path, 'isfile', side_effect=self._mockedOsPathIsfile)
        mocker.patch('builtins.open', self._mockOpen)

    def _mockedOsPathIsdir(self, path):
        if self.root.isParentOf(path):
            # Perform the mocked op. Otherwise just use the sytem original implementation
            out = self.root.isDir(path)
        else:
            out = ORIG_OS_PATH['isdir'](path)
        return out

    def _mockedOsPathIsfile(self, path):
        if self.root.isParentOf(path):
            # Perform the mocked op. Otherwise just use the sytem original implementation
            out = self.root.getFile(path) is not None
        else:
            out = ORIG_OS_PATH['isfile'](path)
        return out

    def mockFile(self, file_path, file_data):
        if isinstance(file_data, bytes):
            file_bin_payload = file_data
        else:
            # Either a raw bytes are provided OR a json encoding is performed.
            file_bin_payload = json.dumps(file_data).encode('utf8')

        file_mock = self._mockOpen[file_path]
        file_mock.read_data = file_bin_payload
        return self.root.addFile(file_path, file_mock)


class FakeDir:
    """Fake directory object."""

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.subDirs = {}
        self.files = {}

    def addFile(self, file_path, mockObj):
        assert self.isParentOf(file_path), file_path
        if os.path.dirname(file_path) == self.abspath:
            self._addFile(os.path.basename(file_path), mockObj)
        else:
            # A sub-dir
            subDir = self.addSubDir()
            1/0

    def isParentOf(self, fs_path):
        return (fs_path == self.abspath) or fs_path.startswith(os.path.join(self.abspath, os.sep))

    def isDir(self, path):
        """Return 'True' if 'relPath' is a directory."""
        if self.abspath == path:
            return True
        _subDir = self._findParentOf(path)
        if _subDir:
            out = _subDir.isDir(path)
        else:
            out = None
        return out

    def getFile(self, path):
        dirname = os.path.dirname(path)
        if dirname == self.abspath:
            out = self.files.get(os.path.basename(path))
        else:
            _subDir = self._findParentOf(path)
            if _subDir:
                out = _subDir.getFile(path)
            else:
                out = None
        return out

    def _findParentOf(self, path):
        """Find a subdir that may contain 'path'."""
        _maybeParent = [
            el for el in self.subDirs.values()
            if el.isParentOf(path)
        ]
        if not _maybeParent:
            out = None  # None found
        elif len(_maybeParent) == 1:
            out = _maybeParent[0]
        else:
            raise NotImplementedError('Too many possible parents: {}'.format(_maybeParent))
        return out

    def _addFile(self, fname, mockObj):
        """Actually add a file as direct child."""
        assert os.sep not in fname, 'Only filename is allowed'
        self.files[fname] = mockObj
        return mockObj

    @property
    def abspath(self):
        if self.parent:
            root = self.parent.abspath
        else:
            root = os.sep
        return os.path.join(root, self.name)

    def __repr__(self):
        return "<{} parent={} name={}>".format(
            self.__class__.__name__,
            self.parent, self.name,
        )
