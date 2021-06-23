# Sharknado
Criando um jogo em ambiente marinho com Pygame. Feito por iniciantes em Python.
 
O jogo foi adaptado do Corona Shooter, disponível em: https://github.com/fccoelho/curso_pygame
 
 
## O Grupo
Formado por 5 alunos de Matemática Aplicada e Ciência de Dados e Inteligência Artificial da FGV (Fundação Getúlio Vargas) EMAp (Escola de Matemática Aplicada) no 1º período como trabalho de conclusão do semestre de Introdução à Computação. São eles:
 
André Felipe Araújo Ferreira, Darlan Augusto Farias Araújo, Letícia Brandão Gonçalves Silva, Paloma Vieira Borges e Pedro Lima Garcia.
 
 
## O Jogo
 
O jogador possui um barco e o principal objetivo é protegê-lo contra ataques de animais marinhos que pretendem destruí-lo. Com o passar das fases, a profundidade do mar aumenta e, com isso, surgem novos animais, além dos já existentes tornarem-se mais rápidos e agressivos. Você aceita o desafio? Será que conseguirá sair intacto dessa aventura?
 
### Entendendo a tela de fundo
 
Para acompanhar o jogador nessa aventura, disponibilizamos os elementos fundamentais para sua sobrevivência: vidas, pontos e nível.
 
* As **vidas** representam a quantidade de dano que o jogador pode receber sem que perca o jogo. Se elas chegarem a 0, você terá que reiniciar todo o progresso.
 
* Os **pontos** representam a quantidade de dano que foi gerado aos inimigos. Você conseguirá bater o recorde?
 
* O **nível** representa o grau de dificuldade em que o jogador se encontra. Além de acompanhá-la pelo menu, pode-se perceber essa mudança pela coloração do fundo, que é proporcional à profundidade do mar.
 
![Screenshot](https://github.com/leticia-brand/curso_pygame/blob/main/sharknado/imagens/fase1.png)
 
Se você for capaz de encontrar o chefão, a **barra de vida** dele será acrescentada na parte inferior da tela, indicando quanto ainda falta para que você o vença.
 
[adicionar barra de vida]
 
### Como jogar
#### Controle de movimentos

![Screenshot](https://github.com/leticia-brand/curso_pygame/blob/main/sharknado/imagens/menu.png)
 
#### A função pause
 
Quando estiver em modo pausado, o jogador não poderá se movimentar ou se ausentar do jogo, restando apenas a possibilidade de continuar nele.
 
![Screenshot](https://github.com/leticia-brand/curso_pygame/blob/main/sharknado/imagens/pause.png)

### Fase 1
 
É uma fase introdutória. Contém somente um tipo de inimigo, a **Arraia**, que possui apenas uma vida. O surgimento dela, apesar de ocorrer apenas na parte superior da tela, é aleatório tanto na posição quanto nos intervalos de spawn.
 
O único movimento dela é a descida, sendo a velocidade igual para todas as arraias .
 
![Screenshot](https://github.com/leticia-brand/curso_pygame/blob/main/sharknado/imagens/fase1.png)
 
### Fase 2
 
Aqui é adicionado um novo desafio, escapar do **Peixe-Espada**. Esse inimigo possui a capacidade de atacar seu barco pelas laterais - ele é tão rápido que não pode ser morto. A velocidade do peixe-espada é incorporada no inimigo. Fuja dele antes que seja tarde demais!
 
 ![Screenshot](https://github.com/leticia-brand/curso_pygame/blob/main/sharknado/imagens/fase2.png)

### Fase 3
 
Com o surgimento do **Polvo**, jatos de tinta serão lançados em direção ao seu barco. Esses jatos são tóxicos! Não deixe que eles acertem sua embarcação, ou perderá uma vida.
 
O **Polvo** pode surgir em qualquer canto superior da tela e, diferentemente dos inimigos das fases anteriores, ele não sairá de lá enquanto você não conseguir derrotá-lo.
 
![Screenshot](https://github.com/leticia-brand/curso_pygame/blob/main/sharknado/imagens/fase3.png)

### Fase 4
 
Em águas um pouco mais profundas, os inimigos se multiplicam com mais facilidade e são mais rápidos (ou será que você está mais lento?)
 
![Screenshot](https://github.com/leticia-brand/curso_pygame/blob/main/sharknado/imagens/fase4.png)

### Fase 5
 
Essa é a fase final e o maior desafio do jogo. O **Tubarão** é um dos animais mais perigosos do oceano. Destrua-o antes que seja tarde demais!
 
Enquanto se prepara para atacar seu barco, o tubarão parece ser inofensivo, {...}. Tome cuidado, pois quando menos esperar, ele poderá atacar sua embarcação de várias maneiras:
 
1. Seguir o barco para onde quer que você for
2. Ataque surpresa e veloz, tanto pela vertical quanto pela horizontal
3. Lançar seus súditos do mar, os **Mini-tubarões** na direção do barco
 
### As armas disponíveis
Em águas rasas, pescadores usam técnicas rudimentares para conseguir seus peixes. Assim como eles, você terá à sua disposição apenas um **Arpão** nos primeiros dois níveis.
 
À medida que a profundeza das águas aumenta, é preciso melhorar suas técnicas de defesa e, para isso, no nível 3 serão disponibilizadas 3 **Redes de Pesca** gigantes e com material super resistente (ainda não disponível no planeta Terra). Elas são maiores do que os arpões, por isso sua mira não precisa ser tão apurada.

Na fase 4, você terá à disposição 5 **Balas de Canhão**. Aqui, agilidade é a palavra-chave.
 
Para enfrentar o grande **Tubarão**, todo cuidado é pouco e, por isso, você será equipado com **Balas de Canhão** também, afinal, essa é a melhor arma de um barco de pesca em formato comercial.

### As vidas
A cada um dos níveis que você conseguir completar, sua vidas aumentarão em **3**. E ao completar o nível 4, ganhará mais **6** vidas para enfrentar o tubarão. 

Apesar de parecerem muitas, tome cuidado, porque tudo o que é bom dura pouco. 

## Detalhes técnicos
* A **Arraia** tem 1 vida
* O **Peixe Espada** tem 10 vidas
* O **Polvo** tem 5 vidas
* O **Tubarão** tem 150 vidas