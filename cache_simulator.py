import sys
import math
import random

def main():
    random.seed(0)
    if len(sys.argv) != 7:
        print("Uso: python cache_simulator.py <nsets> <bsize> <assoc> <subst> <flag_saida> <arquivo>")
        exit(1)

    nsets = int(sys.argv[1])
    bsize = int(sys.argv[2])
    assoc = int(sys.argv[3])
    subst = sys.argv[4].upper()
    flagOut = int(sys.argv[5])
    arquivoEntrada = sys.argv[6]

    if subst not in ['R', 'F', 'L']:
        print("Política de substituição inválida! Use R, F ou L.")
        exit(1)

    n_bits_offset = int(math.log2(bsize))
    n_bits_indice = int(math.log2(nsets))
    n_bits_tag = 32 - n_bits_offset - n_bits_indice

    # Inicializa a cache
    cache = [
        [ {'valid': False, 'tag': None, 'fifo_order': 0, 'last_used': 0} for _ in range(assoc)]
        for _ in range(nsets)
    ]

    fifo_counter = 0
    last_used_counter = 0

    hits = 0
    misses = 0
    miss_compulsorio = 0
    miss_capacidade = 0
    miss_conflito = 0

    with open(arquivoEntrada, 'rb') as f:
        while True:
            bytes_lidos = f.read(4)
            if len(bytes_lidos) < 4:
                break
            endereco = int.from_bytes(bytes_lidos , 'big')

            tag = endereco >> (n_bits_offset + n_bits_indice)
            indice = (endereco >> n_bits_offset) & ((1 << n_bits_indice) - 1)

            conjunto = cache[indice]

            # Procura hit
            hit_idx = -1
            for i, bloco in enumerate(conjunto):
                if bloco['valid'] and bloco['tag'] == tag:
                    hit_idx = i
                    break

            if hit_idx != -1:
                # Hit
                hits += 1
                if subst == 'L':
                    last_used_counter += 1
                    conjunto[hit_idx]['last_used'] = last_used_counter
            else:
                # Miss
                misses += 1

                # Verifica se há bloco inválido (miss compulsório)
                invalido_idx = -1
                for i, bloco in enumerate(conjunto):
                    if not bloco['valid']:
                        invalido_idx = i
                        break

                if invalido_idx != -1:
                    #Miss compulsório
                    miss_compulsorio += 1
                    bloco = conjunto[invalido_idx]
                else:
                    #miss capacidade ou conflito
                    #verifica se toda cache esta cheia
                    cache_cheia = all(b['valid'] for conj in cache for b in conj)
                
                    if cache_cheia:
                        miss_capacidade += 1
                    else:
                        miss_conflito +=1
            
                    # Substituição
                    if subst == "R":
                        invalido_idx = random.randint(0, assoc -1)
                    elif subst == 'F':
                        invalido_idx = min(range(assoc), key = lambda i: conjunto[i]['fifo_order'])
                    elif subst == 'L':
                        invalido_idx = min(range(assoc), key = lambda i: conjunto[i]['last_used'])
                    bloco = conjunto[invalido_idx]

                # Atualiza bloco escolhido
                bloco['valid'] = True
                bloco['tag'] = tag

                if subst == 'F':
                    fifo_counter += 1
                    bloco['fifo_order'] = fifo_counter
                if subst == 'L':
                    last_used_counter += 1
                    bloco['last_used'] = last_used_counter

    total = hits + misses
    taxa_hit = hits / total if total > 0 else 0
    taxa_miss = misses / total if total > 0 else 0
    taxa_miss_comp = miss_compulsorio / misses if misses > 0 else 0
    taxa_miss_cap = miss_capacidade / misses if misses > 0 else 0
    taxa_miss_conf = miss_conflito/ misses if misses > 0 else 0



    if flagOut == 0:
        print(f"Total de acessos: {total}")
        print(f"Hits: {hits} ({taxa_hit:.2%})")
        print(f"Misses: {misses} ({taxa_miss:.2%})")
        print(f"Miss compulsório: {miss_compulsorio}")
        print(f"Miss capacidade: {miss_capacidade}")
        print(f"Miss conflito: {miss_conflito}")
    else:
        print(f"{total} {taxa_hit:.4f} {taxa_miss:.4f} {taxa_miss_comp: .4f} {taxa_miss_cap: .4f} {taxa_miss_conf: .4f}")

    # Exibe os argumentos lidos
    print("nsets =", nsets)
    print("bsize =", bsize)
    print("assoc =", assoc)
    print("subst =", subst)
    print("flagOut =", flagOut)
    print("arquivo =", arquivoEntrada)

if __name__ == '__main__':
    main()
