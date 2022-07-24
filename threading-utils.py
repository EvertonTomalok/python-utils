import os

from threading import Semaphore, Thread
from typing import Any, Callable, List, Tuple, Union

import nest_asyncio

nest_asyncio.apply()

CPU_NUMBER = os.cpu_count()


class TaskAsWorkers:
    def __init__(self, function: Callable, num_workers: int = CPU_NUMBER):
        self.function = function
        self.threads = []

        if num_workers < 1:
            raise ValueError("'num_workers' must be greater than 1.")
        self.num_workers = num_workers

    def execute(self):
        if self.num_workers == 1:
            self.function()
        else:
            self._execute_function_in_threads()

    def _execute_function_in_threads(self):
        for i in range(1, self.num_workers + 1):
            thread = Thread(target=self.function)
            self.threads.append(thread)
            thread.start()


class TaskParallelRunner:
    def __init__(self, list_function: List[Callable], max_workers: int = CPU_NUMBER):
        """
        It receives a list of functions to be called in parallel.
        :param list_function: List[callable]
        :param max_workers: Integer
        """
        self.list_function = list_function
        self.max_workers = max_workers

    def execute(self):
        available = Semaphore(self.max_workers)

        def worker(execute_function):
            execute_function()
            available.release()

        threads = []

        for function in self.list_function:
            available.acquire()
            thread = Thread(target=worker, args=(function,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


class TaskWithArgsParallelRunner:
    def __init__(
        self,
        function: Callable,
        list_args: List[Union[List[Any], Tuple[Any]]],
        max_workers: int = CPU_NUMBER,
    ):
        """
        It receives a function to be called in parallel with a list of
        arguments.
        :param function: Callable
        :param list_args: List[Union[List[Any], Tuple[Any]]]
        :param max_workers: Integer
        EXAMPLE of usage:
                from time import sleep
                def print_it(value: str, sleep_time=0):
                    sleep(sleep_time)
                    print(value, end="\n")
                arguments = [["Thread 1", .2], ("Thread 2", 0), ("Thread 3", .1)]
                TaskWithArgsParallelRunner(
                    function=print_it,
                    list_args=arguments,
                ).execute()
                # EXIT in console called in threads:
                # ->  "Thread 2"
                # ->  "Thread 3"
                # ->  "Thread 1"
        """
        self.function = function
        self.list_args = list_args
        self.max_workers = max_workers

    def execute(self):
        available = Semaphore(self.max_workers)

        def worker(*list_of_arguments):
            self.function(*list_of_arguments)
            available.release()

        threads = []

        for args in self.list_args:
            available.acquire()
            thread = Thread(target=worker, args=(*args,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
   
