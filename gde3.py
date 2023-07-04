from platypus import GDE3, Problem, Real
from simulacao import coeficientes_aerodinamicos
import time
import csv

# Definindo o problema de otimização
class MyProblem(Problem):
    def __init__(self):
        super().__init__(4, 2)  # 4 variáveis de decisão e 2 objetivos
        self.types[0] = Real(0.01, 0.5)  # Intervalo das variáveis de decisão
        self.types[1] = Real(0.01, 0.3)  # Intervalo das variáveis de decisão
        self.types[2] = Real(0, 0.49)  # Intervalo das variáveis de decisão
        self.types[3] = Real(0.01, 0.3)  # Intervalo das variáveis de decisão

    def evaluate(self, solution):
        x = solution.variables
        cl, cd = coeficientes_aerodinamicos(x[0], x[1], x[2], x[3])
        f1 = -cl
        f2 = cd
        solution.objectives[:] = [f1, f2]

# Criando uma instância do problema
problem = MyProblem()

# Inicia a contagem do tempo
inicio = time.time()

# Criando uma instância do algoritmo GDE3
algorithm = GDE3(problem, population_size=100, offspring_size= 100)

# Executando o algoritmo de otimização
algorithm.run(500)

# Obtendo a solução final
solutions = algorithm.result

# Finaliza a contagem do tempo
fim = time.time()
# Calcula o tempo decorrido
tempo_decorrido = fim - inicio
print("Tempo decorrido:", tempo_decorrido, "segundos")

# Abre o arquivo CSV em modo de escrita
with open('resultados/populacaoFinal.csv', 'w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)

    # Escreve o cabeçalho do arquivo CSV
    writer.writerow(['cl', 'cd', 'solution'])

    # Escreve as soluções encontradas no arquivo CSV
    for solution in solutions:
        cl = -solution.objectives[0]
        cd = solution.objectives[1]
        writer.writerow([cl, cd, solution])

        # Imprime as soluções encontradas no console
        print(f'cl: {cl}')
        print(f'cd: {cd}')
        print(solution)
        print('---')

# Informa ao usuário que os resultados foram salvos no arquivo CSV
print("Resultados salvos no arquivo:", 'resultados/populacaoFinal.csv')
