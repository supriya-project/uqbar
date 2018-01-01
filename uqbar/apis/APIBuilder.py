import pathlib
import shutil
import uqbar.io
from uqbar.apis.ClassDocumenter import ClassDocumenter
from uqbar.apis.FunctionDocumenter import FunctionDocumenter
from uqbar.apis.MemberDocumenter import MemberDocumenter
from uqbar.apis.ModuleDocumenter import ModuleDocumenter
from uqbar.apis.RootDocumenter import RootDocumenter
from uqbar.apis.ModuleNode import ModuleNode
from uqbar.apis.PackageNode import PackageNode


class APIBuilder(object):
    """
    A builder of reStructuredText API documentation for Python packages.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        initial_source_paths,
        target_directory,
        document_private_members=False,
        document_private_modules=False,
        member_documenter_classes=None,
        module_documenter_class=None,
        root_documenter_class=None,
        ):
        assert initial_source_paths
        assert target_directory

        self._initial_source_paths = frozenset(
            pathlib.Path(_).resolve().absolute() for _ in initial_source_paths
            )
        self._target_directory = pathlib.Path(target_directory).absolute()

        self._document_private_members = bool(document_private_members)
        self._document_private_modules = bool(document_private_modules)

        if member_documenter_classes is None:
            member_documenter_classes = [ClassDocumenter, FunctionDocumenter]
        for _ in member_documenter_classes:
            assert issubclass(_, MemberDocumenter), _
        self._member_documenter_classes = tuple(member_documenter_classes)

        if module_documenter_class is None:
            module_documenter_class = ModuleDocumenter
        assert issubclass(module_documenter_class, ModuleDocumenter)
        self._module_documenter_class = module_documenter_class

        if root_documenter_class is None:
            root_documenter_class = RootDocumenter
        assert issubclass(root_documenter_class, RootDocumenter)
        self._root_documenter_class = root_documenter_class

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Generate documentation.
        """
        # What files to document?
        source_paths = self.collect_source_paths(self._initial_source_paths)
        # Build the node tree
        node_tree = self.build_node_tree(source_paths)
        # Get the documenters, in depth-first order.
        documenters = self.collect_module_documenters(node_tree)
        # Execute each documenter, writing to the target directory.
        visited_paths = self.write(documenters)
        # Iterate the target directory, removing un-touched files.
        self.prune(visited_paths)
        return documenters

    ### PRIVATE METHODS ###

    def _print(self, message, path):
        print('{} {}'.format(
            (message + ':').ljust(11),
            path.relative_to(pathlib.Path.cwd()),
            ))

    ### PUBLIC METHODS ###

    def build_node_tree(self, source_paths):
        """
        Build a node tree.
        """
        root = PackageNode()
        # Build node tree, top-down
        for source_path in sorted(source_paths):
            package_path = self.source_path_to_package_path(source_path)
            parts = package_path.split('.')
            if (
                not self.document_private_modules and
                any(part.startswith('_') for part in parts)
                ):
                continue
            # Find parent node.
            parent_node = root
            if len(parts) > 1:
                parent_package_path = '.'.join(parts[:-1])
                try:
                    parent_node = root[parent_package_path]
                except KeyError:
                    parent_node = root
                try:
                    if parent_node is root:
                        # Backfill missing parent node.
                        grandparent_node = root
                        if len(parts) > 2:
                            grandparent_node = root[
                                parent_package_path.rpartition('.')[0]
                                ]
                        parent_node = PackageNode(name=parent_package_path)
                        grandparent_node.append(parent_node)
                        grandparent_node[:] = sorted(
                            grandparent_node,
                            key=lambda x: x.package_path,
                            )
                except KeyError:
                    parent_node = root
            # Create or update child node.
            node_class = ModuleNode
            if source_path.name == '__init__.py':
                node_class = PackageNode
            try:
                # If the child exists, it was previously backfilled.
                child_node = root[package_path]
                child_node.source_path = source_path
            except KeyError:
                # Otherwise it needs to be created and appended to the parent.
                child_node = node_class(
                    name=package_path,
                    source_path=source_path,
                    )
                parent_node.append(child_node)
                parent_node[:] = sorted(
                    parent_node,
                    key=lambda x: x.package_path,
                    )
        # Build documenters, bottom-up.
        # This allows parent documenters to easily aggregate their children.
        for node in root.depth_first(top_down=False):
            kwargs = dict(
                document_private_members=self.document_private_members,
                member_documenter_classes=self.member_documenter_classes,
                )
            if isinstance(node, ModuleNode):
                node.documenter = self.module_documenter_class(
                    node.package_path,
                    **kwargs
                    )
            else:
                # Collect references to child modules and packages.
                node.documenter = self.module_documenter_class(
                    node.package_path,
                    module_documenters=[
                        child.documenter for child in node
                        if child.documenter is not None
                        ],
                    **kwargs
                    )
        return root

    def collect_module_documenters(self, root_node):
        # Yield root documenter.
        yield self.root_documenter_class(
            module_documenters=[node.documenter for node in root_node],
            )
        # Yield module documenters, top-down.
        for node in root_node.depth_first():
            if node is not root_node:
                yield node.documenter

    @classmethod
    def collect_source_paths(cls, initial_source_paths):
        visited_paths = set()
        path_stack = []
        for source_path in initial_source_paths:
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
            elif current_path.suffix in ('.py', '.pyx'):
                visited_paths.add(current_path)
        return sorted(visited_paths)

    @classmethod
    def source_path_to_package_path(cls, path):
        path = pathlib.Path(path)
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

    def write(self, documenters):
        visited_paths = set()
        for documenter in documenters:
            new_documentation = str(documenter)
            path = self._target_directory.joinpath(
                documenter.documentation_path
                ).relative_to(pathlib.Path.cwd())
            uqbar.io.write(new_documentation, path, verbose=True)
            visited_paths.add(path.absolute())
        return visited_paths

    def prune(self, visited_paths):
        generator = uqbar.io.walk(self._target_directory, top_down=False)
        for root_path, directory_paths, file_paths in generator:
            for file_path in file_paths[:]:
                if file_path.suffix != '.rst':
                    continue
                if file_path not in visited_paths:
                    file_paths.remove(file_path)
                    file_path.unlink()
                    self._print('pruned', file_path)
            if not file_paths and not directory_paths:
                if root_path == self._target_directory:
                    continue
                shutil.rmtree(str(root_path))
                self._print('pruned', root_path)

    ### PUBLIC PROPERTIES ###

    @property
    def document_private_members(self):
        return self._document_private_members

    @property
    def document_private_modules(self):
        return self._document_private_modules

    @property
    def initial_source_paths(self):
        return self._initial_source_paths

    @property
    def member_documenter_classes(self):
        return self._member_documenter_classes

    @property
    def module_documenter_class(self):
        return self._module_documenter_class

    @property
    def target_directory(self):
        return self._target_directory

    @property
    def root_documenter_class(self):
        return self._root_documenter_class
