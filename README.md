BOT CALLBACK EPB

VERSÃO ORIGINAL FEITA POR RUAN

COLABORADORES QUE PARTICIPARAM DO PROJETO: Anny Caroline, Diego Farias, Leonardo Correia, Ruan Carlos;

UPLOAD NO GITHUB FEITO POR LEONARDO CORREIA

ESSE BOT VISA AUTOMATIZAR O PROCESSO DE CALLBACK REALIZADO NO COI


COMO FUNCIONA O BOT?

1 - O BOT FUNCIONA IMPORTANDO A BASE DE DADOS FORNECIDA A ELE

2 - ENVIA MENSAGENS AUTOMATICAMENTE PARA OS CLIENTES PARA SABER O STATUS DA ENERGIA DO CLIENTE



COMO RODAR O BOT?

1 - PREPARAÇÃO

1.1 - PRIMEIRO, VÁ AO  SPOOL SISTEMAS(spoolsistemas (\\fileserver.scl.corp)) E BUSQUE A PASTA "Exportacoes_BD_DEOP"

1.2 - BUSQUE OS ARQUIVOS QUE CONTÉM "H.001[...]"

1.2.1 - DENTRE ESSES ARQUIVOS, ESCOLHA O QUE MELHOR LHE SATISFIZER, .1 CONTÉM TODAS AS OCORRÊNCIAS, .2 CONTÉM TODAS AS OCORRÊNCIAS DE NIVEL DE TENSÃO, .3 TODAS DO LESTE, .4 TODAS DO CENTRO, .5 TODAS DO OESTE.

1.3 - COPIE A PLANILHA SELECIONADA E COLE NA PASTA EM QUE ESTÁ O BOT *ATENÇÃO, ESSE DETALHE É MUITO IMPORTANTE*

1.4 - RENOMEIE O ARQUIVO PARA 'ocorrencias' *sem as aspas*


2 - RODANDO O BOT

PARA RODAR O BOT, SE FAZ NECESSÁRIO QUE VOCÊ TENHA INSTALADO NA MÁQUINA OS SEGUINTES ITENS

- PYTHON

- VISUAL STUDIO CODE ou IDLE(IDE)

CASO ALGUM DESSES ITENS ESTEJA FALTANDO NA SUA MÁQUINA, VIDE SESSÃO "3" DESTE ARQUIVO


2.1 - USANDO O VISUAL STUDIO CODE

2.1.1 - ABRA O VS CODE USANDO A BARRA DE PESQUISA DO WINDOWS

2.1.2 - VERIFIQUE SE O PYTHON ESTÁ INSTALADO NO VS CODE

2.1.3 - ABRA O ARQUIVO "MAIN_COI_EPB_R.py"

2.1.4 - RODE O PROGRAMA (Run>>Run without debugging ou simplesmente shift+F5)


2.2 - USANDO O IDLE(IDE)

2.2.1 - ABRA A IDLE USANDO A BARRA DE PESQUISA DO WINDOWS

2.2.2 - VÁ EM FILE>>OPEN

2.2.3 - ABRA O ARQUIVO "MAIN_COI_R.py"

2.2.4 - RODE O PROGRAMA (Run>>Run Module ou simplesmente F5)


3 - MINHA MÁQUINA NÃO TEM UM DOS ITENS

3.1 - MÁQUINA SEM PYTHON

3.1.1 - No diretório "DADOS PB", localize a pasta "7- Leonardo Correia" (DADOS PB\Deod\OPERACAO DA DISTRIBUICAO\12 - COI BT\5 - Operadores COI\7 - Leonardo Correia)

3.1.2 - Localize o arquivo "python-3.13.13-amd64.txt"

3.1.3 - Cole o arquivo na sua máquina, em qualquer lugar

3.1.4 - Procure a opção "Visualizar"  e clique

3.1.5 - Role até o final e clique em "Mostrar"

3.1.6 - Marque a opção "Extensões de nomes de arquivos"

3.1.7 - Renomeie o arquivo "python-3.13.13-amd64.txt" para "python-3.13.13-amd64.exe" *LEMBRANDO SEMPRE QUE É SEM AS ASPAS*

3.1.8 - Na caixa que abrir, clique em "SIM"

3.1.9 - Execute o arquivo

3.1.10 - Na tela que abriu marque a caixa que diz "Add python.exe to PATH"

3.1.11 - Clique em "Install Now" e aguarde a instalação completa

3.1.12 - Teste se o python foi corretamente instalado na sua máquina digitando "python --version" no CMD


3.2 - 
