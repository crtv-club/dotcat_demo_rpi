OUT = "out"
LOW = "low"
HIGH = "high"


def setup(*args, **kwargs):
    print("gpio setup, {0}, {1}".format(args, kwargs))


def cleanup(*args, **kwargs):
    print("gpio cleanup, {0}, {1}".format(args, kwargs))


def output(*args, **kwargs):
    print("gpio output, {0}, {1}".format(args, kwargs))

