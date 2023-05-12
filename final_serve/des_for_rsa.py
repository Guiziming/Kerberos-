import binascii
import random
import datetime

# IP置换表
pos_IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

# IP逆变换表
neg_IP = [40, 8, 48, 16, 56, 24, 64, 32, 39,
          7, 47, 15, 55, 23, 63, 31, 38, 6,
          46, 14, 54, 22, 62, 30, 37, 5, 45,
          13, 53, 21, 61, 29, 36, 4, 44, 12,
          52, 20, 60, 28, 35, 3, 43, 11, 51,
          19, 59, 27, 34, 2, 42, 10, 50, 18,
          58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

# E扩展置换表，32->48
E = [32, 1, 2, 3, 4, 5, 4, 5,
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1]

# P置换表。32->32
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# S代换表，48->32
S = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],

]
# 将64位的key变换为56位的key，剔除校验位
key1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# 将56位的key变换为48位的key（生成子密钥）
key2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# key循环左移的位数
move_key = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# 对键入获取内容的处理
# 代换操作，传入参数：table-需要置换的表；changetable-前面定义过的相关标准表
def displace(table, changetable):
    # print("当前处理的内容为",table)
    # print("当前对照的标准表为：",changetable)
    change_result = ""
    for i in changetable:
        change_result += table[i - 1]
    # print("change_result",change_result)
    return change_result


# 明文分割，将其划分为64位一块
# 传入参数是二进制格式的明文
def divide_block(m):
    length = len(m)
    if length % 64 != 0:
        block = m + ("0" * (64 - (length % 64)))  # 当前明文后用0补足64位
        return [block[i:i + 64] for i in range(0, length, 64)]  # 按64位一块的list返回
    else:
        return [m[j:j + 64] for j in range(0, length, 64)]


# 将字符串转换为二进制
def change_str_to_bin(s):
    return ''.join([bin(ord(c)).replace('0b', '').zfill(8) for c in s])


# 键入获取密钥key
def get_key():
    digits = [str(random.randint(1, 9)) for _ in range(8)]
    key = ''.join(digits)
    # bin_key = change_str_to_bin(key)
    return key


# 循环左移操作，支持子密钥获取过程中的位移操作
# str->要进行位移的字符串；num->要位移的移动数目；返回位移后的字符串
def left_turn(str, num):
    left_res = str[num:len(str)]
    left_res = str[0:num] + left_res
    return left_res


# 对key的处理，获取每一轮加密的子钥匙
# 返回存有16组子密钥的list
def get_per_key(k):
    key = displace(k, key1)  # 获取56位密码
    left_key = key[0:28]
    right_key = key[28:56]
    # print("left_key",left_key)
    # print("right_kry",right_key)
    keys = []  # 存储16轮密钥
    # 获取16轮的密钥
    for i in range(0, 16):
        #pianyi = move_key[i]
        lkey = left_turn(left_key, move_key[i])
        rkey = left_turn(right_key, move_key[i])
        new_key = displace(lkey + rkey, key2)
        keys.append(new_key)
    # print("keys", keys)
    return keys


# 轮函数F的实现部分
# 实现异或操作
# 传入参数：str1->异或字符串1；str2->异或字符串2
def my_xor(str1, str2):
    result = ""
    tmp = ""
    for i in range(0, len(str1)):
        if str1[i] == str2[i]:
            tmp = '0'
        else:
            tmp = '1'
        result += tmp
    return result


# s盒子：一个六位的二进制数输入，将第一位和第六位做行号，中间几位做列号
# 传入参数为48位二进制串，就是xor的结果
def s_box(xor_str):
    result = ""
    # 6位一组，分为8组，分别进行s盒运算
    for i in range(0, 8):
        now_block = xor_str[i * 6:(i + 1) * 6]
        line_num = int(now_block[0] + now_block[5], 2)
        column_num = int(now_block[1:4], 2)
        num = bin(S[i][line_num * 16 + column_num])[2:]  # 返回2进制字符串0bxxx,[2:]可以不显示0b
        # 将num按照4位进行划分，不足4位的需要用‘0’补齐
        if len(num) < 4:
            num = num + '0' * (4 - len(num))
        result += num
    return result


# 轮函数F
# 传入参数：right->右侧二进制字符串；key->子密钥列表
def F_function(right, key):
    E_box = displace(right, E)
    xor = my_xor(E_box, key)
    S_box = s_box(xor)
    P_box = displace(S_box, P)
    return P_box


# 16轮操作
# 传入参数：plaintext->二进制明文；keys->子密钥列表
def handle(plaintext, keys):
    left = plaintext[0:32]
    right = plaintext[32:64]
    for i in range(0, 16):
        next_left = right
        F = F_function(right, keys[i])
        next_right = my_xor(left, F)
        left = next_left
        right = next_right
    message = left + right
    result = message[32:] + message[:32]
    return result


# 加密操作
# 传入参数：plaintext->用户键入明文,k->密钥
def encryption(plaintext,key):
    binar_plaintext = change_str_to_bin(plaintext)
    binar_plaintext_block = divide_block(binar_plaintext)
    binar_ciphertext = []
    k=change_str_to_bin(key)
    keys = get_per_key(k)
    for block in binar_plaintext_block:
        pos_ip = displace(block, pos_IP)
        tmp = handle(pos_ip, keys)
        neg_ip = displace(tmp, neg_IP)
        binar_ciphertext.append(neg_ip)
    ciphertext = ''.join(binar_ciphertext)
    my_bin = [ciphertext[i:i + 8] for i in range(0, len(ciphertext), 8)]
    my_int = []
    for num in my_bin:
        my_int.append(int(num, 2))
    result = bytes(my_int).hex().upper()
    return result


# 解密操作
# 传入参数：ciphertext->用户键入密文，kk->密钥
def decrypt(ciphertext,key):
    ciphertext_b = binascii.a2b_hex(ciphertext)
    # print("ciphertext_b:",ciphertext_b,type(ciphertext_b))
    result_bin=[]
    for num in ciphertext_b:
        result_bin.append(bin(num)[2:].zfill(8))
    binar_ciphertext=''.join(result_bin)
    binar_plaintext = []
    kk=change_str_to_bin(key)
    pos_keys = get_per_key(kk)
    neg_keys = pos_keys[::-1]
    binar_ciphertext_block = divide_block(binar_ciphertext)
    for block in binar_ciphertext_block:
        pos_ip = displace(block, pos_IP)
        tmp = handle(pos_ip, neg_keys)
        neg_ip = displace(tmp, neg_IP)
        binar_plaintext.append(neg_ip)
    binar_plaintext = ''.join(binar_plaintext).replace('00000000', '')
    divide_binary = [binar_plaintext[i:i + 8] for i in range(0, len(binar_plaintext), 8)]
    temp = []
    for member in divide_binary:
        temp.append(int(member, 2))
    result1 = list(map(str, temp))
    result = ''.join(result1)
    result3 = bytes(temp).decode()
    # print("******resui*****",result3,type(result3))
    return result3

