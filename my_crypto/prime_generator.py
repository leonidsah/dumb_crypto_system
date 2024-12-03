import time
from random import randrange, random


def generate_primes(n):
    p = get_probably_prime(n)
    q = get_probably_prime(n)
    while q == p:
        print("Ooops, looks like we got two equal primes... Try once again...")
        q = get_probably_prime(n)
    primes = [p, q]
    return primes

def nBitRandom(n):
    # Returns a random number
    # between 2**(n-1)+1 and 2**n-1'''
    return randrange(2 ** (n - 1) + 1, 2 ** n - 1)

def get_primes_less_than(n):
    numbers = [2, 3, 5]
    for i in range(6, n):
        if (i % 2 == 0) or (i % 3 == 0) or (i % 5 == 0):
            continue
        else:
            numbers.append(i)

    index = 0

    for i in numbers:
        for j in numbers[i+1:]:
            if j <= i:
                continue
            else:
                if (j % i) == 0:
                    numbers.remove(j)
    return numbers


def get_low_level_prime(n):
    #first_primes_list = get_primes_less_than(2000)
    first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                         31, 37, 41, 43, 47, 53, 59, 61, 67,
                         71, 73, 79, 83, 89, 97, 101, 103,
                         107, 109, 113, 127, 131, 137, 139,
                         149, 151, 157, 163, 167, 173, 179,
                         181, 191, 193, 197, 199, 211, 223,
                         227, 229, 233, 239, 241, 251, 257,
                         263, 269, 271, 277, 281, 283, 293,
                         307, 311, 313, 317, 331, 337, 347, 349]
    '''Generate a prime candidate divisible
    by first primes'''

    # Repeat until a number satisfying
    # the test isn't found
    while True:
        # Obtain a random number
        prime_candidate = nBitRandom(n)

        for divisor in first_primes_list:
            if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                break
            # If no divisor found, return value
            else:
                return prime_candidate

def isMillerRabinPassed(miller_rabin_candidate):
    '''Run 20 iterations of Rabin Miller Primality test'''

    maxDivisionsByTwo = 0
    evenComponent = miller_rabin_candidate-1

    while evenComponent % 2 == 0:
        evenComponent >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * evenComponent == miller_rabin_candidate-1)

    def trialComposite(round_tester):
        if pow(round_tester, evenComponent, miller_rabin_candidate) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * evenComponent, miller_rabin_candidate) == miller_rabin_candidate-1:
                return False
        return True

    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = randrange(2, miller_rabin_candidate)
        if trialComposite(round_tester):
            return False
    return True


# n - number of bits
def get_probably_prime(n):
    while True:
        prime_candidate = get_low_level_prime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate

if __name__ == "__main__":
    start_time = time.time()
    n = 8192
    p = get_probably_prime(n)
    print("First prime number is done...")
    q = get_probably_prime(n)
    print("Second prime number is done...")
    while q == p:
        print("Ooops, looks like we got two equal primes... Try once again...")
        q = get_probably_prime(n)
    end_time = time.time()
    print(p)
    print(q)
    print(f"Time elapsed: {round((end_time - start_time) // 60)} minutes {round((end_time - start_time) % 60)} seconds")