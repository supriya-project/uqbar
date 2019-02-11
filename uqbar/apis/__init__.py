"""
Tools for auto-generating API documention.
"""
import importlib
import pathlib

from .APIBuilder import APIBuilder  # noqa
from .ClassDocumenter import ClassDocumenter  # noqa
from .FunctionDocumenter import FunctionDocumenter  # noqa
from .InheritanceGraph import InheritanceGraph  # noqa
from .MemberDocumenter import MemberDocumenter  # noqa
from .ModuleDocumenter import ModuleDocumenter  # noqa
from .ModuleNode import ModuleNode  # noqa
from .PackageNode import PackageNode  # noqa
from .RootDocumenter import RootDocumenter  # noqa
from .SummarizingClassDocumenter import SummarizingClassDocumenter  # noqa
from .SummarizingModuleDocumenter import SummarizingModuleDocumenter  # noqa
from .SummarizingRootDocumenter import SummarizingRootDocumenter  # noqa


def collect_source_paths(source_paths, recurse_subpackages=True):
    visited_paths = set()
    path_stack = []
    for source_path in source_paths:
        source_path = pathlib.Path(source_path).resolve().absolute()
        assert source_path.exists(), source_path
        path_stack.append(source_path)
    while path_stack:
        current_path = path_stack.pop()
        if current_path in visited_paths:
            continue
        if current_path.is_dir():
            if not (current_path / "__init__.py").exists():
                continue
            if recurse_subpackages:
                for path in current_path.iterdir():
                    if path.is_dir() and (path / "__init__.py").exists():
                        path_stack.append(path)
                    elif path.suffix in (".py", ".pyx"):
                        visited_paths.add(path)
            else:
                visited_paths.add(current_path / "__init__.py")
                for path in current_path.iterdir():
                    if path.is_dir():
                        continue
                    # Permit nominative modules
                    if path.suffix in (".py", ".pyx"):
                        package_path = source_path_to_package_path(path)
                        module = importlib.import_module(package_path)
                        if hasattr(module, path.with_suffix("").name):
                            visited_paths.add(path)
        elif current_path.suffix in (".py", ".pyx"):
            visited_paths.add(current_path)
    return sorted(visited_paths)


def source_path_to_package_path(path):
    path = pathlib.Path(path)
    if not (path.parent / "__init__.py").exists():
        return path.with_suffix("").name
    root = path
    while (root.parent / "__init__.py").exists():
        root = root.parent
    path = path.with_suffix("")
    if path == root:
        return path.name
    parts = (root.name,) + path.relative_to(root).parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)
