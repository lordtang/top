import struct
fmt = 'i'
header  = struct.Struct(fmt)
pack_data = header.pack(1)
print(header.unpack(pack_data,)[0])
