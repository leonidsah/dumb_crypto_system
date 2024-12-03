import math

from my_crypto.prime_generator import generate_primes


# Returns dict {public: public_key, private: private_key}
def generate_keys(key_size):
    def extended_gcd(a, b):
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        bezu = [old_s, old_t]
        gcd = old_r
        gcd_divsion = [t, s]
        return bezu

    def generate_closed_exponent(phi, e):
        bezu = extended_gcd(phi, e)
        return bezu[1]

    def generate_open_exponent(phi):
        return 65537

    p, q = generate_primes(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = generate_open_exponent(phi)
    d = generate_closed_exponent(phi, e)
    keys = {(e, n), (d, n)}
    return keys


def encrypt(message, public_key):
    if len(message) > (public_key[1].bit_length() + 7) // 8:
        raise Exception("Message exceeds key size. Can't encrypt.")
    m = int.from_bytes(message.encode('utf-8'), byteorder='little')
    e, n = public_key[0], public_key[1]
    cipher_ = pow(m, e, n)
    return cipher_


def decrypt(cipher, private_key):
    def int_to_string(i):
        length = math.ceil(i.bit_length() / 8)
        return i.to_bytes(length, byteorder='little').decode('utf-8')

    c = cipher
    d, n = private_key[0], private_key[1]
    m = pow(c, d, n)
    return int_to_string(m)


def create_signature(message_hash, signer_private_key):
    signature = encrypt(message_hash, signer_private_key)
    return signature


def check_signature(signature, message_hash, signer_public_key) -> bool:
    recovered_hash = decrypt(signature, signer_public_key)
    if recovered_hash == message_hash:
        return True
    else:
        return False


def export_rsa_key(rsa_key, path, label):
    path_ = path + '/' + label + '.key'
    f = open(path_, 'w')
    f.write(f"+----BEGIN {label}----+" + "\n")
    f.write(str(rsa_key[0]) + '\n')
    f.write(str(rsa_key[1]) + '\n')
    f.write(f"+----END {label}----+" + "\n")
    f.close()


def import_rsa_key(path) -> [int, int]:
    f = open(path, 'r')
    f.readline()
    exponent = f.readline()
    modulus = f.readline()
    f.close()
    return [int(exponent), int(modulus)]

def import_and_encrypt(key_path, text_file_path, mode):
    key = import_rsa_key(key_path)
    #print(f"Imported key: {key}")
    text_file = open(text_file_path, 'r', encoding='utf-8')
    try:
        source = text_file.read()
    except Exception as e:
        print("FUCK")
        print(e)
    if mode == "encrypt":
        result = encrypt(source, key)
    elif mode == "decrypt":
        source = int(source)
        print(source)
        result = decrypt(source, key)
    else:
        print("Unknown RSA work mode.")
        result = None
    return result


if __name__ == "__main1__":
    import_and_encrypt(r"C:\Users\leoni\PycharmProjects\dumb_crypto_system\rsa_keys\PRIVATE_KEY.key",
                       r"C:\Users\leoni\PycharmProjects\dumb_crypto_system\rsa_keys\result1.txt",
                       "decrypt")

if __name__ == "__main__":
    # print("keys...")
    # public_key, private_key = generate_keys(8192)
    # print("exporting...")
    # export_rsa_key(public_key, "C:/Users/leoni/Desktop/public.key", "PUBLIC KEY")
    # export_rsa_key(private_key, "C:/Users/leoni/Desktop/private.key", "PRIVATE KEY")

    print("importing keys...")
    public_key = import_rsa_key(r"/rsa_keys/PUBLIC_KEY_2048.key")
    private_key = import_rsa_key(r"/rsa_keys/PRIVATE_KEY_2048.key")

    # public_key = (65537, 21231005681092718128517562992936840872831144429910193720319161098360816600046433565887757850209969498321728175525368854240731689543342043679299301706447494070258905322453889030844588892393329430998405701629625942627853689401679153592081762295253285879788155275307059458640863306799460840086241119268514002355502828917628778753012826259743501303247050336391183093591728062881920997936868521713967327719477413033507659183324995348630428023919222016067642670595452045733906077593747731617798217978398254574283238230405808688800538844966397582012217216807487086874510526054515091592139825556985586404823938258840387741943)
    # private_key = (-4135927026420353881727630601504869728907872208625104036304907605517075019192102435810137853023951059478973764696772573692592298707597965601928897949039705155789789649385367063747087391689971113196463762343491987877531898814276481284009152985695083705803673930754310208103329445014399751977982519335659524666508747282412220415119278454822941721685835567341627394151657843109260225371407207604476290469125021129474249281800046737345437818587630828307037136345703879332765080447103475362233978837709773079759271206243184323994706734253636568077289572845834101297955235990416663793512482692818642560371753543946110868167, 21231005681092718128517562992936840872831144429910193720319161098360816600046433565887757850209969498321728175525368854240731689543342043679299301706447494070258905322453889030844588892393329430998405701629625942627853689401679153592081762295253285879788155275307059458640863306799460840086241119268514002355502828917628778753012826259743501303247050336391183093591728062881920997936868521713967327719477413033507659183324995348630428023919222016067642670595452045733906077593747731617798217978398254574283238230405808688800538844966397582012217216807487086874510526054515091592139825556985586404823938258840387741943)

    message = """You let i reach the largest number allowed to access the vector. The problem is you adding even more when calling "at".
Let's say that listOfStringTokens contains 12 Element. Imagine the last iteration: i<listOfStringTokens.size() is true and i is 11: curl"""
    print("encrypting...")
    cipher = encrypt(message, public_key)
    print("decrypting...")
    decrypted_message = decrypt(cipher, private_key)
    print(f"Original message: {message}")
    print(f"Cipher: {cipher}")
    print(f"Decrypted message: {decrypted_message}")
