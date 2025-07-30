# Simulador de Cache Parametrizável

**Disciplina:** Arquitetura e Organização de Computadores II

**Autores:**
- Milena Ferreira
- Kananda Winter

## Descrição

Este projeto consiste em um simulador de cache funcional e parametrizável, desenvolvido para a disciplina de Arquitetura e Organização de Computadores II. 
O programa simula o comportamento de uma hierarquia de memória cache, permitindo ao usuário configurar dinamicamente suas principais características através de parâmetros de linha de comando.
O simulador processa um arquivo binário contendo uma sequência de endereços de memória de 32 bits e analisa o desempenho da configuração de cache especificada,
calculando métricas essenciais como taxas de hit e miss (compulsório, de capacidade e de conflito).

## Funcionalidades

- **Configuração flexível:** Permite definir o número de conjuntos, tamanho do bloco e nível de associatividade
- **Políticas de substituição:** Suporte para Random (Aleatória), FIFO (First-In, First-Out) e LRU (Least Recently Used)
- **Múltiplos formatos de saída:** Formato detalhado para análise humana e formato padrão para avaliação automatizada
- **Simulação realística:** Baseada em endereços de 32 bits com cache endereçada a byte

## Como Executar

O simulador deve ser executado via linha de comando. O nome do executável deve ser `cache_simulator`, independentemente da linguagem de programação utilizada.

### Formato do Comando

```bash
python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> <arquivo_de_entrada>
```

### Detalhamento dos Parâmetros

- **`<nsets>`:** O número total de conjuntos (ou linhas) na cache
- **`<bsize>`:** O tamanho de cada bloco em bytes
- **`<assoc>`:** O grau de associatividade (número de vias por conjunto)
- **`<substituição>`:** A política de substituição para caches associativas:
  - `R`: Aleatória (Random)
  - `F`: FIFO (First-In, First-Out)
  - `L`: LRU (Least Recently Used)
- **`<flag_saida>`:** Controla o formato da saída:
  - `0`: Formato livre com textos e labels (ex: "Taxa de hit = 90%")
  - `1`: Formato padrão para avaliação (valores numéricos separados por espaços)
- **`<arquivo_de_entrada>`:** Caminho para o arquivo binário com endereços de 32 bits (formato big-endian)

### Formato de Saída Padrão (flag_saida = 1)

Os resultados são exibidos na seguinte ordem:
1. Total de Acessos
2. Taxa de Hit
3. Taxa de Miss
4. Taxa de Miss Compulsório
5. Taxa de Miss de Capacidade
6. Taxa de Miss de Conflito

## Exemplo de Uso

Simulação com cache de 256 conjuntos, blocos de 4 bytes, mapeamento direto, política aleatória e formato padrão:

```bash
python cache_simulator.py 256 4 1 R 1 bin_100.bin
```

**Saída Esperada:**
```
100 0.9200 0.0800 1.0000 0.0000 0.0000
```

## Notas Técnicas

- O simulador trabalha com endereços de 32 bits em formato big-endian
- A cache é endereçada a byte
- Todas as taxas são calculadas como valores decimais entre 0 e 1
- O arquivo de entrada deve conter endereços sequenciais em formato binário
