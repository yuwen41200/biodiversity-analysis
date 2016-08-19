#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import inspect
import ctypes


# noinspection PyPep8Naming
class TerminatableThread(threading.Thread):
    """
    A thread class that supports raising exception in the thread from another thread. |br|
    Source: http://stackoverflow.com/q/323972 by Bluebird75 and Tshepang.
    """

    @staticmethod
    def asyncRaise(tid, excType):
        """
        Asynchronously raise an exception in a thread.

        :param tid: The thread ID of the target thread.
        :param excType: The exception type to be raised.
        :return: None.
        """

        if not inspect.isclass(excType):
            raise TypeError("Only types can be raised (not instances).")

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(excType))

        if res == 0:
            raise ValueError("Invalid thread ID.")
        elif res != 1:
            # If something goes wrong, call it again with exc=NULL to revert the effect.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc() failed.")

    # noinspection PyProtectedMember, PyAttributeOutsideInit
    def getTid(self):
        """
        Determine this (self's) thread ID.

        WARNING: This method is executed in the context of the caller thread,
        to get the identity of the thread represented by this instance.

        :return: Thread ID.
        """

        if not self.is_alive():
            raise AssertionError("The thread is not active.")

        # Do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # If not, look for it in ``threading._active`` dictionary.
        for tid, tObj in threading._active.items():
            if tObj is self:
                self._thread_id = tid
                return tid

        raise RuntimeError("Could not determine the thread's ID.")

    # noinspection PyBroadException
    def terminate(self, excType=RuntimeWarning):
        """
        Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(), socket.accept(), etc.),
        the exception is simply ignored.

        WARNING: This method is executed in the context of the caller thread,
        to raise an exception in the context of the thread represented by this instance.

        :param excType: The exception type to be raised.
        :return: None.
        """

        try:
            TerminatableThread.asyncRaise(self.getTid(), excType)
        except Exception:
            # Don't care !!
            pass
