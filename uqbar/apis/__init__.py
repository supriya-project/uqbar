"""
Tools for auto-generating API documention.
"""

import pathlib

from .APIBuilder import APIBuilder
from .ClassDocumenter import ClassDocumenter
from .FunctionDocumenter import FunctionDocumenter
from .InheritanceGraph import InheritanceGraph
from .MemberDocumenter import MemberDocumenter
from .ModuleDocumenter import ModuleDocumenter
from .ModuleNode import ModuleNode
from .PackageNode import PackageNode
from .RootDocumenter import RootDocumenter
from .SummarizingClassDocumenter import SummarizingClassDocumenter
from .SummarizingModuleDocumenter import SummarizingModuleDocumenter
from .SummarizingRootDocumenter import SummarizingRootDocumenter


def collect_source_paths(source_paths, recurse_subpackages=True):
    visited_paths = set()
    path_stack = []
    for source_path in source_paths:
        source_path = pathlib.Path(source_path).resolve().absolute()
        assert source_path.exists()
        path_stack.append(source_path)
    while path_stack:
        current_path = path_stack.pop()
        if current_path in visited_paths:
            continue
        if current_path.is_dir():
            if not (current_path / '__init__.py').exists():
                continue
            for path in current_path.iterdir():
                if (
                    not recurse_subpackages and
                    path.is_dir() and
                    (path / '__init__.py').exists()
                    ):
                    continue
                path_stack.append(path)
        elif current_path.suffix in ('.py', '.pyx'):
            visited_paths.add(current_path)
    return sorted(visited_paths)


def source_path_to_package_path(path):
    path = pathlib.Path(path)
    if not (path.parent / '__init__.py').exists():
        return path.with_suffix('').name
    root = path
    while (root.parent / '__init__.py').exists():
        root = root.parent
    path = path.with_suffix('')
    if path == root:
        return path.name
    parts = (root.name,) + path.relative_to(root).parts
    if parts[-1] == '__init__':
        parts = parts[:-1]
    return '.'.join(parts)
