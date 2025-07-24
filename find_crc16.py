def crc16(data, poly, init, xor_out, reflect_in, reflect_out):
    """
    计算CRC16校验码
    :param data: 输入数据列表
    :param poly: 多项式
    :param init: 初始值
    :param xor_out: 结果异或值
    :param reflect_in: 输入是否翻转
    :param reflect_out: 输出是否翻转
    :return: 计算得到的CRC16值
    """
    crc = init
    for byte in data:
        if reflect_in:
            byte = int('{:08b}'.format(byte)[::-1], 2)  # 翻转输入字节
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # 保持16位
        
    if reflect_out:
        # 翻转输出
        crc = int('{:016b}'.format(crc)[::-1], 2) & 0xFFFF
    
    return crc ^ xor_out

# 输入数据
data = [0x17, 0x00, 0x43, 0x05, 0x91, 0x10, 0x33, 0x23, 0x02, 0x25, 
        0x0B, 0xA0, 0xA2, 0x05, 0x01, 0x2C, 0x20, 0x00, 0x02, 0x00, 0x00]

# 目标校验码
target_crc = 0x710A

# 初始值
initial_value = 0xFFFF

# 常见的CRC16参数组合
crc16_params = [
    {"name": "CRC-16/IBM", "poly": 0x8005, "init": 0x0000, "xor_out": 0x0000, "reflect_in": True, "reflect_out": True},
    {"name": "CRC-16/CCITT", "poly": 0x1021, "init": 0x0000, "xor_out": 0x0000, "reflect_in": False, "reflect_out": False},
    {"name": "CRC-16/CCITT-FALSE", "poly": 0x1021, "init": 0xFFFF, "xor_out": 0x0000, "reflect_in": False, "reflect_out": False},
    {"name": "CRC-16/Modbus", "poly": 0x8005, "init": 0xFFFF, "xor_out": 0x0000, "reflect_in": True, "reflect_out": True},
    {"name": "CRC-16/X25", "poly": 0x1021, "init": 0xFFFF, "xor_out": 0xFFFF, "reflect_in": True, "reflect_out": True},
    {"name": "CRC-16/USB", "poly": 0x8005, "init": 0xFFFF, "xor_out": 0xFFFF, "reflect_in": True, "reflect_out": True},
    {"name": "CRC-16/MODBUS", "poly": 0x8005, "init": 0xFFFF, "xor_out": 0x0000, "reflect_in": True, "reflect_out": True},
    {"name": "CRC-16/DNP", "poly": 0x3D65, "init": 0x0000, "xor_out": 0xFFFF, "reflect_in": True, "reflect_out": True},
    {"name": "CRC-16/TMS37157", "poly": 0x1021, "init": 0x89EC, "xor_out": 0x0000, "reflect_in": True, "reflect_out": True},
]

# 测试所有参数组合，使用指定的初始值
print(f"目标校验码: 0x{target_crc:04X}")
print(f"使用初始值: 0x{initial_value:04X}\n")

found = False
for params in crc16_params:
    # 使用指定的初始值替换参数中的初始值
    test_params = params.copy()
    test_params["init"] = initial_value
    
    result = crc16(
        data,
        test_params["poly"],
        test_params["init"],
        test_params["xor_out"],
        test_params["reflect_in"],
        test_params["reflect_out"]
    )
    
    print(f"{test_params['name']} (多项式 0x{test_params['poly']:04X}): 0x{result:04X} {'✓' if result == target_crc else ''}")
    
    if result == target_crc:
        found = True
        matched_params = test_params

if found:
    print(f"\n找到匹配的CRC16参数: {matched_params['name']}")
    print(f"多项式: 0x{matched_params['poly']:04X}")
    print(f"初始值: 0x{matched_params['init']:04X}")
    print(f"结果异或值: 0x{matched_params['xor_out']:04X}")
    print(f"输入翻转: {matched_params['reflect_in']}")
    print(f"输出翻转: {matched_params['reflect_out']}")
else:
    print("\n未找到匹配的CRC16参数组合")
