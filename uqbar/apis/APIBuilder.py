import pathlib
import shutil
from typing import Sequence, Type, Union

import uqbar.io
from uqbar.apis.ClassDocumenter import ClassDocumenter
from uqbar.apis.FunctionDocumenter import FunctionDocumenter
from uqbar.apis.MemberDocumenter import MemberDocumenter
from uqbar.apis.ModuleDocumenter import ModuleDocumenter
from uqbar.apis.ModuleNode import ModuleNode
from uqbar.apis.PackageNode import PackageNode
from uqbar.apis.RootDocumenter import RootDocumenter


class APIBuilder(object):
    """
    A builder of reStructuredText API documentation for Python packages.

    ::

        >>> import uqbar
        >>> import tempfile
        >>> with tempfile.TemporaryDirectory() as target_directory:
        ...     with uqbar.io.DirectoryChange(target_directory):
        ...         builder = uqbar.apis.APIBuilder(
        ...             initial_source_paths=uqbar.apis.__path__,
        ...             target_directory=target_directory,
        ...             )
        ...         visited_paths = builder()
        ...
        wrote index.rst
        wrote uqbar/index.rst
        wrote uqbar/apis/index.rst
        wrote uqbar/apis/APIBuilder.rst
        wrote uqbar/apis/ClassDocumenter.rst
        wrote uqbar/apis/FunctionDocumenter.rst
        wrote uqbar/apis/InheritanceGraph.rst
        wrote uqbar/apis/MemberDocumenter.rst
        wrote uqbar/apis/ModuleDocumenter.rst
        wrote uqbar/apis/ModuleNode.rst
        wrote uqbar/apis/PackageNode.rst
        wrote uqbar/apis/RootDocumenter.rst
        wrote uqbar/apis/SummarizingClassDocumenter.rst
        wrote uqbar/apis/SummarizingModuleDocumenter.rst
        wrote uqbar/apis/SummarizingRootDocumenter.rst
        wrote uqbar/apis/dummy.rst

    :param initial_source_paths: a list of paths to scan for Python sources
    :param target_directory: where to write reStructuredText output
    :param document_private_members: whether to documenter private module members
    :param document_private_modules: whether to document private modules
    :param member_documenter_classes: a list of
        :py:class:`~uqbar.apis.MemberDocumenter` subclasses, defining what classes
        to use to identify and document module members
    :param module_documenter_class: a :py:class:`~uqbar.apis.ModuleDocumenter` subclass
    :param root_documenter_class: a :py:class:`~uqbar.apis.RootDocumenter` subclass
    """

    ### INITIALIZER ###

    def __init__(
        self,
        initial_source_paths: Sequence[Union[str, pathlib.Path]],
        target_directory: Union[str, pathlib.Path],
        document_empty_modules: bool = True,
        document_private_members: bool = False,
        document_private_modules: bool = False,
        member_documenter_classes: Sequence[Type[MemberDocumenter]] = None,
        module_documenter_class: Type[ModuleDocumenter] = None,
        omit_root: bool = False,
        root_documenter_class: Type[RootDocumenter] = None,
        title: str = "API",
        logger_func=None,
    ) -> None:
        assert initial_source_paths
        assert target_directory
        self._initial_source_paths = frozenset(
            pathlib.Path(_).resolve().absolute() for _ in initial_source_paths
        )
        self._target_directory = pathlib.Path(target_directory).absolute()
        self._document_private_members = bool(document_private_members)
        self._document_private_modules = bool(document_private_modules)
        self._document_empty_modules = bool(document_empty_modules)
        if member_documenter_classes is None:
            member_documenter_classes = [ClassDocumenter, FunctionDocumenter]
        for _ in member_documenter_classes:
            assert issubclass(_, MemberDocumenter), _
        self._member_documenter_classes = tuple(member_documenter_classes)
        if module_documenter_class is None:
            module_documenter_class = ModuleDocumenter
        assert issubclass(module_documenter_class, ModuleDocumenter)
        self._module_documenter_class = module_documenter_class
        self._omit_root = bool(omit_root)
        if root_documenter_class is None:
            root_documenter_class = RootDocumenter
        assert issubclass(root_documenter_class, RootDocumenter)
        self._root_documenter_class = root_documenter_class
        self._title = title
        self._logger_func = logger_func

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Generate documentation.
        """
        import uqbar.apis

        # Make sure target directory exists.
        if not self._target_directory.exists():
            self._target_directory.mkdir(parents=True)
        self._target_directory = self._target_directory.resolve()
        # What files to document?
        source_paths = uqbar.apis.collect_source_paths(self._initial_source_paths)
        # Build the node tree
        node_tree = self.build_node_tree(source_paths)
        # Get the documenters, in depth-first order.
        documenters = self.collect_module_documenters(node_tree)
        # Execute each documenter, writing to the target directory.
        visited_paths = self.write(documenters)
        # Iterate the target directory, removing un-touched files.
        self.prune(visited_paths)
        return visited_paths

    ### PRIVATE METHODS ###

    def _print(self, message, path):
        cwd = pathlib.Path.cwd()
        if str(path).startswith(str(cwd)):
            path = path.relative_to(cwd)
        message = "{} {}".format(message, path)
        (self._logger_func or print)(message)

    ### PUBLIC METHODS ###

    def build_node_tree(self, source_paths):
        """
        Build a node tree.
        """
        import uqbar.apis

        root = PackageNode()
        # Build node tree, top-down
        for source_path in sorted(
            source_paths, key=lambda x: uqbar.apis.source_path_to_package_path(x)
        ):
            package_path = uqbar.apis.source_path_to_package_path(source_path)
            parts = package_path.split(".")
            if not self.document_private_modules and any(
                part.startswith("_") for part in parts
            ):
                continue
            # Find parent node.
            parent_node = root
            if len(parts) > 1:
                parent_package_path = ".".join(parts[:-1])
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
                                parent_package_path.rpartition(".")[0]
                            ]
                        parent_node = PackageNode(name=parent_package_path)
                        grandparent_node.append(parent_node)
                        grandparent_node[:] = sorted(
                            grandparent_node, key=lambda x: x.package_path
                        )
                except KeyError:
                    parent_node = root
            # Create or update child node.
            node_class = ModuleNode
            if source_path.name == "__init__.py":
                node_class = PackageNode
            try:
                # If the child exists, it was previously backfilled.
                child_node = root[package_path]
                child_node.source_path = source_path
            except KeyError:
                # Otherwise it needs to be created and appended to the parent.
                child_node = node_class(name=package_path, source_path=source_path)
                parent_node.append(child_node)
                parent_node[:] = sorted(parent_node, key=lambda x: x.package_path)
        # Build documenters, bottom-up.
        # This allows parent documenters to easily aggregate their children.
        for node in root.depth_first(top_down=False):
            kwargs = dict(
                document_private_members=self.document_private_members,
                member_documenter_classes=self.member_documenter_classes,
            )
            if isinstance(node, ModuleNode):
                node.documenter = self.module_documenter_class(
                    node.package_path, **kwargs
                )
            else:
                # Collect references to child modules and packages.
                node.documenter = self.module_documenter_class(
                    node.package_path,
                    module_documenters=[
                        child.documenter
                        for child in node
                        if child.documenter is not None
                    ],
                    **kwargs,
                )
            if (
                not self.document_empty_modules
                and not node.documenter.module_documenters
                and not node.documenter.member_documenters
            ):
                node.parent.remove(node)
        return root

    def collect_module_documenters(self, root_node):
        if not self.omit_root:
            # Yield root documenter.
            yield self.root_documenter_class(
                module_documenters=[node.documenter for node in root_node],
                title=self._title,
            )
        # Yield module documenters, top-down.
        for node in root_node.depth_first():
            if node is not root_node:
                yield node.documenter

    def write(self, documenters):
        visited_paths = set()
        for documenter in documenters:
            new_documentation = str(documenter)
            path = self._target_directory.joinpath(documenter.documentation_path)
            cwd = pathlib.Path.cwd()
            if str(path).startswith(str(cwd)):
                path = path.relative_to(pathlib.Path.cwd())
            uqbar.io.write(
                new_documentation, path, verbose=True, logger_func=self._logger_func
            )
            visited_paths.add(path.absolute())
        return visited_paths

    def prune(self, visited_paths):
        generator = uqbar.io.walk(self._target_directory, top_down=False)
        for root_path, directory_paths, file_paths in generator:
            for file_path in file_paths[:]:
                if file_path.suffix != ".rst":
                    continue
                if file_path not in visited_paths:
                    file_paths.remove(file_path)
                    file_path.unlink()
                    self._print("pruned", file_path)
            if not file_paths and not directory_paths:
                if root_path == self._target_directory:
                    continue
                shutil.rmtree(str(root_path))
                self._print("pruned", root_path)

    ### PUBLIC PROPERTIES ###

    @property
    def document_empty_modules(self):
        return self._document_empty_modules

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
    def omit_root(self):
        return self._omit_root

    @property
    def target_directory(self):
        return self._target_directory

    @property
    def root_documenter_class(self):
        return self._root_documenter_class
