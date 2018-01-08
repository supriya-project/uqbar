import cProfile
import io
import pstats


class Profiler:
    """
    A context manager for profiling blocks of code.
    """

    def __enter__(self) -> 'Profiler':
        self._profiler = cProfile.Profile()
        self._profiler.enable()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._profiler.disable()
        stream = io.StringIO()
        profiler_stats = pstats.Stats(self._profiler, stream=stream)
        profiler_stats = profiler_stats.sort_stats('cumulative')
        profiler_stats.print_stats()
        print(stream.getvalue())
        profiler_stats.dump_stats('stats.profile')
