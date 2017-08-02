import pathlib


class APIBuilder(object):

    def __init__(
        self,
        source_paths=None,
        target_directory=None,
        ):
        assert source_paths
        assert target_directory
        self._source_paths = frozenset(
            pathlib.Path(_).resolve().absolute() for _ in source_paths
            )
        self._target_directory = pathlib.Path(
            target_directory).resolve().absolute()

    ### PUBLIC METHODS ###

    @classmethod
    def collect_paths(cls, source_paths):
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
                    path_stack.append(path)
            elif current_path.suffix == '.py':
                visited_paths.add(current_path)
        return sorted(visited_paths)

    @classmethod
    def source_path_to_root_package_path(cls, path):
        path = pathlib.Path(path)
        assert path.suffix == '.py'
        root = path
        while (root.parent / '__init__.py').exists():
            root = root.parent
        return root

    @classmethod
    def source_path_to_package_path(cls, path):
        path = pathlib.Path(path)
        root = cls.source_path_to_root_package_path(path)
        path = path.with_suffix('')
        if path == root:
            return path.name
        parts = (root.name,) + path.relative_to(root).parts
        if parts[-1] == '__init__':
            parts = parts[:-1]
        return '.'.join(parts)

    @classmethod
    def source_path_to_docs_path_suffix(cls, path):
        root = cls.source_path_to_root_package_path(path)
        if path == root:
            return path.with_suffix('.rst').name
        relative_path = path.relative_to(root)
        if relative_path.name == '__init__.py':
            relative_path = relative_path.parent / 'index.rst'
        else:
            relative_path = relative_path.with_suffix('.rst')
        return root.name / relative_path
