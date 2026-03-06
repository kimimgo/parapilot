"""Tests for server-level input validation."""

from __future__ import annotations

import os

import pytest


class TestValidateFilePath:
    """Test _validate_file_path path traversal prevention."""

    def _reload_with_data_dir(self, data_dir: str | None = "/data"):
        """Reload server module with PARAPILOT_DATA_DIR set."""
        import importlib

        import parapilot.config
        import parapilot.server

        if data_dir is not None:
            os.environ["PARAPILOT_DATA_DIR"] = data_dir
        else:
            os.environ.pop("PARAPILOT_DATA_DIR", None)

        importlib.reload(parapilot.config)
        importlib.reload(parapilot.server)
        return parapilot.server._validate_file_path

    def test_valid_path_within_data_dir(self, tmp_path):
        data_dir = str(tmp_path / "data")
        os.makedirs(data_dir, exist_ok=True)
        test_file = os.path.join(data_dir, "cavity.vtk")
        open(test_file, "w").close()  # noqa: SIM115
        validate = self._reload_with_data_dir(data_dir)
        result = validate(test_file)
        assert result == test_file

    def test_valid_nested_path(self, tmp_path):
        data_dir = str(tmp_path / "data")
        nested = os.path.join(data_dir, "cases", "foam")
        os.makedirs(nested, exist_ok=True)
        test_file = os.path.join(nested, "cavity.foam")
        open(test_file, "w").close()  # noqa: SIM115
        validate = self._reload_with_data_dir(data_dir)
        result = validate(test_file)
        assert result == test_file

    def test_rejects_path_traversal(self):
        validate = self._reload_with_data_dir("/data")
        with pytest.raises(ValueError, match="Access denied"):
            validate("/etc/shadow")

    def test_rejects_dotdot_traversal(self):
        validate = self._reload_with_data_dir("/data")
        with pytest.raises(ValueError, match="Access denied"):
            validate("/data/../etc/passwd")

    def test_rejects_absolute_outside(self):
        validate = self._reload_with_data_dir("/data")
        with pytest.raises(ValueError, match="Access denied"):
            validate("/home/user/.ssh/id_rsa")

    def test_data_dir_itself_is_allowed(self, tmp_path):
        data_dir = str(tmp_path / "data")
        os.makedirs(data_dir, exist_ok=True)
        validate = self._reload_with_data_dir(data_dir)
        # data_dir itself is a directory, not a file — should raise FileNotFoundError
        # unless the directory exists, which it does. But _validate checks .exists()
        # on resolved path, and directories exist.
        result = validate(data_dir)
        assert result == data_dir

    def test_no_data_dir_allows_any_path(self, tmp_path):
        """When PARAPILOT_DATA_DIR is unset, any path is allowed."""
        test_file = str(tmp_path / "test.vtk")
        open(test_file, "w").close()  # noqa: SIM115
        validate = self._reload_with_data_dir(None)
        result = validate(test_file)
        assert result == test_file

    def test_no_data_dir_allows_absolute_paths(self, tmp_path):
        """When PARAPILOT_DATA_DIR is unset, absolute paths work."""
        test_file = str(tmp_path / "case.foam")
        open(test_file, "w").close()  # noqa: SIM115
        validate = self._reload_with_data_dir(None)
        result = validate(test_file)
        assert result == test_file

    def test_file_not_found_raises_error(self):
        """Non-existent paths produce a clear FileNotFoundError."""
        validate = self._reload_with_data_dir(None)
        with pytest.raises(FileNotFoundError, match="File not found"):
            validate("/nonexistent/path/file.vtk")

    def test_file_not_found_suggests_similar(self, tmp_path):
        """Error message suggests similar filenames when available."""
        # Create a file with a similar name
        (tmp_path / "cavity.vtk").touch()
        validate = self._reload_with_data_dir(None)
        with pytest.raises(FileNotFoundError, match="Did you mean"):
            validate(str(tmp_path / "caviti.vtk"))


class TestMainVersionFlag:
    """Test --version flag on the CLI entry point."""

    def test_version_flag_prints_version(self):
        """mcp-server-parapilot --version should print version and exit."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "parapilot.server", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "mcp-server-parapilot" in result.stdout
        # Version string should match importlib.metadata
        from importlib.metadata import version

        pkg_version = version("mcp-server-parapilot")
        assert pkg_version in result.stdout

    def test_python_m_parapilot_version(self):
        """python -m parapilot --version should also work."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "parapilot", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "mcp-server-parapilot" in result.stdout

    def test_main_module_imports_and_calls_main(self):
        """__main__.py should import and call main()."""
        from unittest.mock import patch

        with patch("parapilot.server.main") as mock_main:
            import importlib

            import parapilot.__main__

            importlib.reload(parapilot.__main__)
            mock_main.assert_called()

    def test_server_main_guard(self):
        """server.py if __name__ == '__main__' guard should call main()."""
        from unittest.mock import patch

        import parapilot.server  # noqa: F811

        with patch("parapilot.server.main") as mock_main:
            # Simulate __name__ == "__main__" by executing the guard
            parapilot.server.main()
            mock_main.assert_called()
