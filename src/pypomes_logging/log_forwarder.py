import copy
import logging


class LogForwarder(logging.Handler):
    """
    A handler that forwards records to a preconfigured target logger.
    When forwarding, all target logger's properties, such as formatting and logging level, are kept.
    The target logger's own handlers, levels, and filters are preserved and applied.
    """

    def __init__(self,
                 target: logging.Logger):
        """
        Initialize the log forwarder.

        :param target: the logger that will handle all activities of the logger being forwarded to.
        """
        # let target decide about filtering (no extra filtering here)
        super().__init__(level=0)

        # initialize the instance variable
        self.target: logging.Logger = target

    def emit(self,
             record: logging.LogRecord):
        """
        Make the forwarder handle the log output.

        :param record: the log record to output
        """
        # prevent potential re-entrancy loops if the std_logger ends up causing logs that flow back here
        if not hasattr(record,
                       "_forwarded_to_target"):
            # copy to avoid mutating the original record for other handlers
            new_record: logging.LogRecord = copy.copy(record)
            new_record._forwarded_to_target = True

            self.target.handle(new_record)
