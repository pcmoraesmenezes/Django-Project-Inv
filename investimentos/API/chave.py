import random
import string

def gerar_chave():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

if __name__ == '__main__':
    chave = gerar_chave()
    print(chave)