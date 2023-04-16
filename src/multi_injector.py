from typing import Iterable, List, Type, TypeVar, Union

from injector import (
    Binder,
    Injector,
    Scope,
    ScopeDecorator,
    _InstallableModuleType,
    inject,
)

T = TypeVar("T")


class MultiBinder(Binder):
    def bind_several(
        self,
        interfaces: List[Type[T]],
        implementation_type: Type[T],
        scope: Union[None, Type[Scope], ScopeDecorator] = None,
    ):
        """Bind several interfaces to an implementation.
        For instance:
        ::
            class C(A, B):
                ...
            binder.bind_several([A, B], to=C, scope=singleton)
        This will bind both interfaces to the same instance of C.
        """

        def get_implementation(implementation: implementation_type):  # type: ignore
            return implementation

        self.bind(implementation_type, scope=scope)
        for interface in interfaces:
            self.bind(interface, to=inject(get_implementation), scope=scope)


class MultiInjector(Injector):
    binder: MultiBinder

    def __init__(
        self,
        modules: Union[
            _InstallableModuleType, Iterable[_InstallableModuleType]
        ] = None,
        auto_bind: bool = True,
        parent: Injector = None,
    ) -> None:
        super().__init__(modules, auto_bind, parent)

        self.binder = MultiBinder(
            self,
            auto_bind=auto_bind,
            parent=parent.binder if parent is not None else None,
        )
        self.binder.bind(Binder, to=self.binder)