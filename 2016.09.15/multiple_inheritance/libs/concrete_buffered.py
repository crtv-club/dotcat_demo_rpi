import threading
import logging

from libs.concrete import ShiftRegister
from libs.abstract_buffered import ShiftRegBuffered


class ShiftRegWrapper(ShiftRegBuffered, ShiftRegister):
    """
    ShiftRegWrapper - оболочка для сдвиговорого регистра.
    Содержит дополнительный буфер содержимого и дополнительные методы для работы с ним
    """
    def __init__(self, si, sck, rck, sclr, num_of_slaves=0):
        ShiftRegister.__init__(self, si, sck, rck, sclr, num_of_slaves)
        ShiftRegBuffered.__init__(self, si, sck, rck, sclr, num_of_slaves)
