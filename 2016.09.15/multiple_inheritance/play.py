from libs import concrete_buffered

temp = concrete_buffered.ShiftRegWrapper(1, 2, 3, 4)

print(temp.buffer)
print(temp.get_buffer())

print(temp.capacity)
print(temp.get_capacity())

temp.write_data(1)

print(temp.get_buffer())
