import thread


class AsyncTask:
    """
    Asynchronous tasks. An extremely lightweight implementation of Thread which is designed to only
    execute a single task or worker function and then exit. The high level threading.py module has
    been avoided to preserve space.

    Example:
    >>> task = AsyncTask(self.print, 'Hello world!')
    >>> task.start()
    >>> task.join()
    >>> try:
    >>>    res = task.result()
    >>>    print('Result was {}'.format(res))
    >>> except e:
    >>>    print('Exception caught during execution')
    """
    def __init__(self, target, args=(), kwargs=None):
        # Initialization copied from start_new_thread. We need to do the exact same thing but
        # we also want to capture return values and exceptions, hence our own class.
        if kwargs is None:
            kwargs = {}

        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._tid = None
        self._result = None
        self._exception = None
        self.is_alive = False

    def start(self):
        """
        Start asynchronous task. If the task has already been started (whether or not it has finished
        doesn't matter) this will do nothing.
        """
        if not self._tid:
            self.is_alive = True
            self._tid = thread.start_new_thread(self._run, ())

    def join(self):
        """
        Wait for task to finish indefinitely.
        """
        while self._tid and self.is_alive:
            pass

    def result(self):
        """
        Get the result of the task. If an exception was thrown in the task's worker function it will be rethrown here.
        @return: Result from work function.
        @raise: Any exception thrown in the work function.
        """
        if self._exception:
            raise self._exception[1], None, self._exception[2]
        return self._result

    def _run(self):
        """
        Thread worker function.
        """
        try:
            if self._target:
                self._result = self._target(*self._args, **self._kwargs)
        except:
            import sys
            self._exception = sys.exc_info()
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
            self.is_alive = False
