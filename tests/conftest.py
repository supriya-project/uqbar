import shutil
from pathlib import Path

import pytest

pytest_plugins = "sphinx.testing.fixtures"


collect_ignore = ["roots"]


@pytest.fixture(scope="session")
def remove_sphinx_projects(sphinx_test_tempdir) -> None:
    # Even upon exception, remove any directory from temp area
    # which looks like a Sphinx project. This ONLY runs once.
    roots_path = Path(sphinx_test_tempdir)
    for path in roots_path.iterdir():
        if path.is_dir():
            if (Path(path) / "_build").exists():
                # This directory is a Sphinx project, remove it
                shutil.rmtree(path)


@pytest.fixture()
def rootdir(remove_sphinx_projects) -> Path:
    return Path(__file__).parent / "roots"
