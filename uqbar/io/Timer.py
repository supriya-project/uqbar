import time
import typing


class Timer:
    """
    A context manager for timing blocks of code.

    This context manager is not reentrant. Use a separate instance when nesting
    multiple timers.

    :param exit_message: message to print on entering the context
    :param enter_message: message to print on exiting the context
    :param verbose: whether to print output

    ::

        >>> import math
        >>> from uqbar.io import Timer
        >>> timer = Timer("Elapsed time:", "Looping!")
        >>> with timer:
        ...     for i in range(10000):
        ...         z = i ** math.pi
        ...
        Looping!
        Elapsed time: 0.0...

    """

    def __init__(
        self, exit_message: str = None, enter_message: str = None, verbose: bool = True
    ) -> None:
        if enter_message is not None:
            enter_message = str(enter_message)
        self._enter_message = enter_message
        if exit_message is not None:
            exit_message = str(exit_message)
        self._exit_message = exit_message
        self._start_time: typing.Optional[float] = None
        self._stop_time: typing.Optional[float] = None
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self) -> "Timer":
        if self.enter_message and self.verbose:
            print(self.enter_message)
        self._stop_time = None
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._stop_time = time.time()
        if self.exit_message and self.verbose:
            print(self.exit_message, self.elapsed_time)

    ### PUBLIC PROPERTIES ###

    @property
    def elapsed_time(self) -> typing.Union[float, None]:
        if self.start_time is not None:
            if self.stop_time is not None:
                return self.stop_time - self.start_time
            return time.time() - self.start_time
        return None

    @property
    def enter_message(self) -> typing.Union[str, None]:
        return self._enter_message

    @property
    def exit_message(self) -> typing.Union[str, None]:
        return self._exit_message

    @property
    def start_time(self) -> typing.Union[float, None]:
        return self._start_time

    @property
    def stop_time(self) -> typing.Union[float, None]:
        return self._stop_time

    @property
    def verbose(self) -> bool:
        return self._verbose
