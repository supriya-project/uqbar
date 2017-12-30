import time


class Timer:
    """
    A context manager for timing blocks of code.

    This context manager is not reentrant. Use a separate instance when nesting
    multiple timers.
    """

    def __init__(
        self,
        exit_message=None,
        enter_message=None,
        verbose=True,
        ):
        if enter_message is not None:
            enter_message = str(enter_message)
        self._enter_message = enter_message
        if exit_message is not None:
            exit_message = str(exit_message)
        self._exit_message = exit_message
        self._start_time = None
        self._stop_time = None
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self):
        if self.enter_message and self.verbose:
            print(self.enter_message)
        self._stop_time = None
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stop_time = time.time()
        if self.exit_message and self.verbose:
            print(self.exit_message, self.elapsed_time)

    ### PUBLIC PROPERTIES ###

    @property
    def elapsed_time(self):
        if self.start_time is not None:
            if self.stop_time is not None:
                return self.stop_time - self.start_time
            return time.time() - self.start_time
        return None

    @property
    def enter_message(self):
        return self._enter_message

    @property
    def exit_message(self):
        return self._exit_message

    @property
    def start_time(self):
        return self._start_time

    @property
    def stop_time(self):
        return self._stop_time

    @property
    def verbose(self):
        return self._verbose
