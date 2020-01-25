import hashlib, sys, argparse, random, time


def create_parser():
    new_parser = argparse.ArgumentParser()
    new_parser.add_argument('mode')
    new_parser.add_argument('-l', '--length', type=int, default=30)
    new_parser.add_argument('-r', '--random', default=False)
    new_parser.add_argument('-m', '--message', default=False)
    new_parser.add_argument('-s', '--sign')
    new_parser.add_argument('-p', '--public')

    return new_parser


def keygen(count):
    random.seed()
    s_key = [[], []]
    p_key = [[], []]
    for i in range(2):
        for j in range(count):
            key = random.randint(0, 999999999)
            s_key[i].append(key)
            h = hashlib.sha256(bytes(str(key), encoding='utf-8')).hexdigest()
            p_key[i].append(h)

    return [s_key, p_key]


def sign(message):
    msg_len = len(message)
    s_key, p_key = keygen(msg_len)
    signature = []
    for i in range(msg_len):
        if message[i] == '0':
            signature.append(s_key[0][i])
        elif message[i] == '1':
            signature.append(s_key[1][i])
    save(message, signature, p_key)

    return signature


def save(message, signature, p_key):
    f = open(namespace.sign, 'w')
    f.write(str(message) + '\n')
    for i in signature:
        f.write(str(i) + ' ')
    f.close()
    f = open(namespace.public, 'w')
    for i in range(len(message)):
        f.write(str(p_key[0][i]) + ' ' + str(p_key[1][i]) + '\n')
    f.close()


def load():
    f = open(namespace.sign, 'r')
    message = f.readline()
    signature = f.readline().split(' ')
    f.close()
    f = open(namespace.public, 'r')
    public = f.read().split('\n')

    return [message, signature, public]


def verify():
    message, signature, public = load()
    calc_sign = []
    public_sign = []
    for i in range(len(message) - 1):
        h = hashlib.sha256(bytes(str(signature[i]), encoding='utf-8')).hexdigest()
        calc_sign.append(h)
        public_sign.append(public[i].split(' ')[int(message[i])])

    if len(list(set(calc_sign) - set(public_sign))) == 0:
        return True
    else:
        return False


def get_rand_msg():
    res = ""
    for i in range(namespace.length):
        res = res + str((random.randint(0, 1)))
    return res


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    start_time = time.time()
    if namespace.mode == 'sign':
        if namespace.message:
            sign(namespace.message)
        else:
            sign(get_rand_msg())
    elif namespace.mode == 'verify':
        ref = verify()
        print(ref)
    end_time = time.time()
    print(end_time - start_time)
