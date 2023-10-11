from platypus import GDE3, Problem, Real
from platypus.indicators import Hypervolume, Spacing
from platypus.core import nondominated, normalize, crowding_distance
from simulacao import coeficientes_aerodinamicos
import time
import math
import csv

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# Especifique a fonte diretamente nas configurações do Matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{newtxtext,newtxmath}'



# Definindo o problema de otimização
class MyProblem(Problem):
    def __init__(self):
        super().__init__(4, 2)  # 4 variáveis de decisão e 2 objetivos
        self.types[0] = Real(0.05, 0.95)  # Intervalo das variáveis de decisão
        self.types[1] = Real(0, 1.4)  # Intervalo das variáveis de decisão
        self.types[2] = Real(0.05, 0.95)  # Intervalo das variáveis de decisão
        self.types[3] = Real(0, 1.4)  # Intervalo das variáveis de decisão

    def evaluate(self, solution):
        x = solution.variables
        if abs(x[0] - x[2]) < 0.02:
            cl = -100
            cd = 100
        elif x[0] < x[2]:
            h_le = x[0]*math.tan(x[1])
            h_te = x[2]*math.tan(x[3])
            cl, cd = coeficientes_aerodinamicos(x[0], h_le, x[2], h_te)
        else: 
            h_le = x[2]*math.tan(x[1])
            h_te = x[0]*math.tan(x[3])
            cl, cd = coeficientes_aerodinamicos(x[2], h_le, x[0], h_te)           
        f1 = -cl
        f2 = cd
        solution.objectives[:] = [f1, f2]


def functionGDE3(n_iterations, pop_size, off_size):
    problem = MyProblem() # Cria uma instância do problema

    inicio = time.time() # Inicia a contagem do tempo

    algorithm = GDE3(problem, population_size = pop_size , offspring_size= off_size, crossover_rate=0.1, step_size=0.5) # Cria uma instância do algoritmo GDE3
    algorithm.run(n_iterations) # Executa o algoritmo de otimização

    final_pop = algorithm.result # Obtem a população final

    fim = time.time() # Finaliza a contagem do tempo

    # Calcula e printa o tempo decorrido
    tempo_decorrido = fim - inicio
    print("Tempo decorrido:", tempo_decorrido, "segundos")

    return final_pop


def saveResults(file_name, results):
    # Abre o arquivo CSV em modo de escrita
    with open('results/' + file_name, 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)

        # Escreve o cabeçalho do arquivo CSV
        writer.writerow(['cl', 'cd', 'x_le', 'angle_le', 'x_te', 'angle_te'])

        # Escreve as soluções encontradas no arquivo CSV
        for result in results:
            cl = -result.objectives[0]
            cd = result.objectives[1]
            var = []
            for v in result.variables: 
                var.append(v)
            writer.writerow([cl, cd, var[0], var[1], var[2], var[3]])

            # Imprime as soluções encontradas no console
            print(f'cl: {cl}')
            print(f'cd: {cd}')
            print(result)
            print('---')

    # Informa ao usuário que os resultados foram salvos no arquivo CSV
    print("Resultados salvos no arquivo:", 'results/' + file_name)


def savesGraphics(file_name, results): 
    plt.figure(figsize=(6, 4))
    plt.grid(True)
    plt.gca().set_axisbelow(True)  # 'gca' é abreviação de 'get current axis'


    plt.scatter([s.objectives[0] for s in results],
                [s.objectives[1] for s in results], c='tab:blue')  # Define a cor como azul
    
    
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

    plt.xlabel("$f_1(x)$")
    plt.ylabel("$f_2(x)$")


    plt.savefig('graphics/' + file_name, format='pdf', bbox_inches='tight')# Salva o gráfico gerado


# Define as variaveis 
vetor = [3,4]
for i in vetor:
    n_iterations = 1*i
    pop_size = 10
    off_size = 1

    #Salva população final
    final_pop = functionGDE3(n_iterations, pop_size, off_size) 
    saveResults('finalPopulation' + str(i) + '.csv', final_pop)
    savesGraphics('finalPopulation' + str(i) + '.pdf', final_pop)

    #Salva resultado
    results = nondominated(final_pop)
    saveResults('paretoOptimal' + str(i) + '.csv', results)
    savesGraphics('paretoOptimal' + str(i) + '.pdf', results)

"""
minimo, maximo = normalize(results)
hyp = Hypervolume(minimum=minimo, maximum=maximo)
hyp_result = hyp.calculate(results)
print(hyp_result)

spc = Spacing()
spc_result = spc.calculate(results)
print(spc_result)
"""
