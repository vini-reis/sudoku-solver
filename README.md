# Sudoku Solver

Este projeto foi desenvolvido para a disciplina de Inteligência Artificial na UFABC, no primeiro quadrimestre de 2021, com o professor Fabrício Olivetti de França.

O projeto sofreu melhorias após o fim da disciplina para nível de conhecimento e treino da implementação de algortimos de busca não informada, e formulação de problemas CSP (*Constraint Satisfaction Problem*, ou Problema de Satisfação de Restrição).

A estrutura do problema ainda pode ser melhorada em futuras versões.

## Instruções

Para executar um dos algoritmos solicitados, execute o seguinte comando:

```bash
python sudoku.py <nome_do_arquivo> <nome_do_algoritmo>
```

### Opções

#### ```<nome_do_algoritmo>```

- ``bfs``
: Executa o algoritmo de Busca em Largura

- ``dfs``
: Executa o algoritmo de Busca em Profundidade

- ``greedy``
: Executa o algoritmo de Busca Gulosa

- ``astar``
: Executa o algoritmo A*

- ``ac3``
: Executa o algoritmo AC-3

- ``backtracking``
: Executa o algoritmo de Backtracking com AC-3
  
## Status de implementação

- Busca em largura - **OK**
- Busca em profundidade - **OK**
- Busca A* - **OK**
- AC-3 - **WIP**
- Backtracking - **OK** - Recomendado

## Changelog

Versão 2.0:

- Reestruturação da problema do Sudoku
- Reestruturação do CSP
- Correção do algoritmo de backtracking
- Início da reestruturação do algoritmo de AC-3 (ainda em desenvolvimento)

## Enunciado

Para esse projeto vocês devem implementar os seguintes algoritmos para resolver o Sudoku:

- Busca em largura
- Busca em profundidade
- Busca A*
- AC-3
- Backtracking

Os algoritmos podem ser escritos em sua linguagem favorita contanto que eu tenha como compilar e executar (consulte com o docente).

O programa principal deve receber como entrada um arquivo de texto contendo uma instância do problema por linha e imprimir na tela as soluções desses problemas, um em cada linha.

Exemplo de entrada:

```
.......2143.......6........2.15..........637...........68...4.....23........7....
.......241..8.............3...4..5..7.....1......3.......51.6....2....5..3...7...
.......24....1...........8.3.7...1..1..8..5.....2......2.4...6.5...7.3...........
.......23.1..4....5........1.....4.....2...8....8.3.......5.16..4....7....3......
.......21...5...3.4..6.........21...8.......75.....6.....4..8...1..7.....3.......
.......215.3......6...........1.4.6.7.....5.....2........48.3...1..7....2........
.......21.9.7.................514...63............2......6..93...1.4....2.....8..
.......314...2.........7......3.1.5.7..5.....2.6..........8.2...3.6...........4..
```

Exemplo de saída:

```
857349621432861597619752843271583964945126378386497215768915432194238756523674189
867351924143829765295746813318472596724695138956138247489513672672984351531267489
815369724294718653736524981387645192142897536659231478921453867568172349473986215
497185623312649857586732941138596472975214386264873519829357164641928735753461298
369784521187592436452613798746821953823965147591347682275436819914278365638159274
879543621523716489641829735385194267792638514164257893956481372418372956237965148
758439621194726358326158497879514263632897145415362789547681932981243576263975814
827456931461923587395817624984361752713592846256748319649185273532674198178239465
```

Cada linha representa um problema do Sudoku, por exemplo, a linha

```
.......2143.......6........2.15..........637...........68...4.....23........7....
```

representa a grade

```
|...|...|.21|
|43.|...|...|
|6..|...|...|
|---+---+---|
|2.1|5..|...|
|...|..6|37.|
|...|...|...|
|---+---+---|
|.68|...|4..|
|...|23.|...|
|...|.7.|...|
```

em que os `.` representam valores a serem preenchidos.
