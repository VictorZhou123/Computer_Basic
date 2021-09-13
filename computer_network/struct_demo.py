import struct

bin_str = b'ABCD1234'
print(bin_str)
# 每一字节按字符格式化
result = struct.unpack('>BBBBBBBB', bin_str)
print(result)
# 每两字节按短整型格式化
result = struct.unpack('>HHHH', bin_str)
print(result)
# 每四字节按长整型格式化
result = struct.unpack('>LL', bin_str)
print(result)
# 每四字节按长整型格式化
result = struct.unpack('>LL', bin_str)
print(result)
# 按字符串格式化
result = struct.unpack('>8s', bin_str)
print(result)
# 
result = struct.unpack('>BBHL', bin_str)
print(result)
