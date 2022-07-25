import logging
import signal
import sys
from typing import Callable

from termcolor import colored


logger = logging.getLogger(__name__)


class LoopRunner:
    def __init__(self):
        self.stopped = False

    def run(self, task: Callable, *args, **kwargs):
        while not self.stopped:
            task(*args, **kwargs)

    def stop(self, signal_received, frame):
        if self.stopped:
            logger.warning(
                colored("Force exiting!!!!", "red", attrs=["bold"])
            )
            sys.exit(0)

        logger.warning(
            colored(
                "Graceful exiting ... Type ctrl + C again to force exit.",
                "green",
                attrs=["bold"],
            )
        )
        self.stopped = True


def create_loop_runner_with_signal_to_stop() -> LoopRunner:
    loop_runner = LoopRunner()

    signal.signal(signal.SIGINT, loop_runner.stop)
    signal.signal(signal.SIGTERM, loop_runner.stop)

    return loop_runner
  
  
  
def func(arg1, kwarg):
    print(arg1, kwarg)
    
    
runner = create_loop_runner_with_signal_to_stop()

# func(arg, *args, kwarg, **kwarg)
runner.run(func, "arg", kwarg="kwarg")
