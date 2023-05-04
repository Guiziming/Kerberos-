import random
import datetime
import des_for_rsa as des


# 功能：Miller-Rabin算法，判断是否为素数
# 传入参数：n->需要判断的数;k->判断的循环轮次
# 返回值：是否为素数True/False
def is_prime(n, k):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# 功能：获取一个素数
# 传入参数：无
# 返回值：num->素数
def get_prime_num():
    judge = False
    while not judge:
        num = random.randint(pow(2, 31), pow(2, 32))
        judge = is_prime(num, 10)

    return num


# 扩展欧几里得算法，求逆元，用于计算密钥d
# 传入参数：a->参数，mod->模值
# 传出参数：ax+by=gcd(a,b)的一组整数特解，其中x为a模b的逆元
def ext_gcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = ext_gcd(b, a % b)  # 递归直至余数等于0(需多递归一层用来判断)
        x, y = y, (x - (a // b) * y)  # 辗转相除法反向推导每层a、b的因子使得gcd(a,b)=ax+by成立
        return x, y, gcd


# 获取密钥
# 传入参数：无
# 返回值：密钥对
def getKey():
    p = get_prime_num()
    q = get_prime_num()
    e = 11
    n = p * q
    fyn = (p - 1) * (q - 1)
    d, y, g = ext_gcd(e, fyn)
    if g == 1:
        if d < 0:
            d += fyn
    print("公钥:(", str(n), ",", str(e), ")\n私钥:(", str(n), ",", str(d), ")")
    return n, e, d


# 蒙哥马利快速模幂算法
# 传入参数：num->底数，exp->幂，mod->模
# 返回值：求余结果
def fast_mod_exp(num, exp, mod):
    result = 1
    while exp:
        if exp & 1:
            result = (result * num) % mod
        exp = exp // 2
        num = (num * num) % mod
    return result


# 字符串转换为int，用于处理用户输入的内容
# 传入参数：要转换的字符串
# 返回值：转换后的结果
def change_to_uint(str):
    result = int.from_bytes(str, 'big')
    return result


# 转换为字节，一个数对应32位
# 传入参数：要转换的数
# 返回值：转换后的结果
def change_to_bytes(my_uint):
    if my_uint == 0:
        return bytes(1)
    result = my_uint.to_bytes((my_uint.bit_length() + 7) // 8, 'big')  # 8位划分，尽量少补零
    return result


# 加密函数
# 传入参数：要加密的内容，公钥n,e（加密过程为接收方的公钥nb,eb;签字过程为发送方的na,da）
# 返回值：加密结果
def rsa_encrypt(str, e, n):
    int_data = change_to_uint(str)
    result = fast_mod_exp(int_data, e, n)
    return result


# 解密函数
# 传入参数：要解密的内容，私钥d，公钥n（解密过程为接收方的私钥nb,db;签字识别为过程为发送方的na,ea）
# 返回值：解密结果
def rsa_decrypt(my_int, d, n):
    int_data = fast_mod_exp(my_int, d, n)
    result = change_to_bytes(int_data)
    return result


if __name__ == '__main__':
    na, ea, da = getKey()
    nb, eb, db = getKey()
    while True:
        print("请选择你的身份：A B E")  # E表示结束选择
        iden_choice = input()
        if iden_choice == 'A':
            print("你好A，请选择你要进行的操作：1、加密传输 2、签名 3、带签名的加密传输 4、对称钥传输")
            choice = input()
            print("请输入要加密的内容：")
            plaintext_str = input()  # 明文
            plaintext = bytes(plaintext_str, 'utf-8')
            if choice == '1':
                starttime = datetime.datetime.now()
                ciphertext = rsa_encrypt(plaintext, eb, nb)  # 密文
                trans_ciphertext = ciphertext
                print("加密后的密文为：", ciphertext)
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            elif choice == '2':
                starttime = datetime.datetime.now()
                print("正在进行签名...")
                print("plain",type(plaintext),plaintext)
                signature = rsa_encrypt(plaintext, da, na)
                print("生成的数字签名为：", type(signature),signature)
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            elif choice == '3':
                starttime = datetime.datetime.now()
                print("正在进行带签名的加密传输...")
                tmp_sign = rsa_encrypt(plaintext, da, na)
                tmp_cipher = rsa_encrypt(plaintext, eb, nb)
                print('tmpsign',tmp_sign)#加密后的信息int

                trans_cipher=change_to_bytes(tmp_cipher)
                trans_sign=change_to_bytes(tmp_sign)
                print('transsign',trans_sign)#转换成bytes

                test1=change_to_uint(trans_sign)
                print("trans",test1)#转换回int
                kong = b'000000000'
                cipher_sign = trans_cipher + kong + trans_sign
                print("teas",cipher_sign)#拼接完成
                trans=change_to_uint(cipher_sign)
                print("生成的带数字签名密文为：", trans)
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            elif choice == '4':
                starttime = datetime.datetime.now()
                print("正在进行签名...")
                signature = rsa_encrypt(plaintext, da, na)  # 数字签名
                bytes_sign=change_to_bytes(signature)
                print("请输入8位密钥：")
                key_str = input()  # 用于对称钥加密
                key = bytes(key_str, 'utf-8')
                kkey=rsa_encrypt(key,eb,nb)
                bytes_key=change_to_bytes(kkey)
                trans_des = bytes_key + b'000000000' + bytes_sign
                trans_des_int=change_to_uint(trans_des)
                print("传输的密钥信息为：",trans_des_int)
                print("进行des，请输入要传输的内容：")
                my_str = input()
                k = des.get_key()
                my_cipher = des.encryption(my_str,k)
                print("加密后的内容为：", my_cipher)
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            else:
                print("输入有误，请重新输入")
        elif iden_choice == 'B':
            print("你好B，请选择你要进行的操作：1、传输解密 2、签名解读 3、带签名的加密传输解密 4、对称钥传输解密")
            choices = input()
            if choices == '1':
                starttime = datetime.datetime.now()
                print("要解密的内容为：")
                temp = bytes(input(), 'utf-8')
                b_cipher = int(temp)
                plaintext = rsa_decrypt(b_cipher, db, nb)
                # print("db",db)
                # print("nb",nb)
                print("B读出的消息为：", str(plaintext))
                # print("解读类型",type(plaintext))
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            elif choices == '2':
                starttime = datetime.datetime.now()
                print("要解读的签名为：")
                temp_sign = bytes(input(), 'utf-8')
                b_sign = int(temp_sign)
                signature = rsa_decrypt(b_sign, ea, na)
                print("签名属于A，解读结果为：", signature)
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            elif choices == '3':
                starttime = datetime.datetime.now()
                print("要解密的内容为：")
                temp_cipher_sign = int(input())
                bytes_cipher_sign=change_to_bytes(temp_cipher_sign)
                b_tmp_cipher, b_tmp_sign = bytes_cipher_sign.split(b'000000000')
                #print("cipher",b_tmp_cipher)
                my_cipher=change_to_uint(b_tmp_cipher)
                my_sign=change_to_uint(b_tmp_sign)
                #print("cipher2", my_cipher)
                b_my_cipher=rsa_decrypt(my_cipher,db,nb)
                b_my_sign = rsa_decrypt(my_sign, ea, na)
                print("解密结果为：", b_my_cipher)
                print("签名属于A，解读结果为：", b_my_sign)
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            elif choices == '4':
                starttime = datetime.datetime.now()
                print("请输入rsa传输内容：")
                trans_des = int(input())
                tmp_trans_des = change_to_bytes(trans_des)
                b_key, b_sign = tmp_trans_des.split(b'000000000')
                rsa_sign=change_to_uint(b_sign)
                rsa_cipher=change_to_uint(b_key)
                sign = rsa_decrypt(rsa_sign, ea, na)
                print("签名属于A，解读结果为：", sign)
                key = rsa_decrypt(rsa_cipher,db,nb)
                print("key",type(key),key)
                print("des密钥为：", key)
                print("进行des，请输入要解密的内容：")
                ciphertext = input()
                kk=des.get_key()
                plaintext = des.decrypt(ciphertext, kk)
                print("des解密的内容为：", plaintext)
                endtime = datetime.datetime.now()
                seconds = (endtime - starttime).seconds
                print('加密用时为：', seconds)
            else:
                print("输入有误，请重新输入")
        elif iden_choice == 'E':
            exit()
        else:
            print("输入有误，请重新输入")
