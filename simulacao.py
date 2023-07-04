import numpy as np
import subprocess
import csv


def coeficientes_aerodinamicos(leBendLocation,  leBendHeight, teBendLocation, teBendHeight):

	# Define os valores das variáveis
	teBendLocation = teBendLocation + 0.5
	thickness = 0.008
	AirfoilLc = 0.01

	# Extrair os valores do eixo x e y
	angulos = [0,5,10,15]


	cl_medio, cd_medio= 0, 0
	for alpha in angulos:
		aoa = alpha
	    # Cria o conteúdo do arquivo
		content = f'aoa = {aoa}; // Angle of attack, in degrees.\n'
		content += f'leBendHeight = {leBendHeight}; // chord-normalized maximum height (due to thickness and bend).\n'
		content += f'leBendLocation = {leBendLocation}; // chord-normalized location of bend along the chord (0 @ LE, 1 @ TE).\n'
		content += f'teBendHeight = {teBendHeight}; // chord-normalized maximum height (due to thickness and bend).\n'
		content += f'teBendLocation = {teBendLocation}; // chord-normalized location of bend along the chord (0 @ LE, 1 @ TE).\n'
		content += f'thickness = {thickness}; // chord-normalized thickness.\n'
		content += f'AirfoilLc = {AirfoilLc}; // Grid cell size on surface of airfoil.\n'

	    # Cria o arquivo e escreve o conteúdo
		with open('mesh/parameters.geo', 'w') as file:
			file.write(content)

	    # Comando a ser executado
		malha = 'gmsh -3 -o main.msh mesh/main.geo'
		executavel = './run.sh'


	    # Executa o comando no prompt de comando
		subprocess.run(malha, shell=True)
		subprocess.run(executavel, shell=True)

	    # Abre o arquivo coefficient.dat para leitura
		with open('case/postProcessing/forceCoeffs1/0/coefficient_0.dat', 'r') as arquivo:
			linhas = arquivo.readlines()

	    # Obtém os valores do Cd, Cl e CmPitch na última linha
		ultima_linha = linhas[-1].split()
		iteracao = int(ultima_linha[0])
		cd = float(ultima_linha[1])
		cl = float(ultima_linha[4])
		cm_pitch = float(ultima_linha[7])

		cl_medio = cl_medio + cl
		cd_medio = cd_medio + cd
	    

		# Salva os valores em um arquivo CSV
		with open('resultados/resultados.csv', 'r+') as arquivo_csv:
			# Ler as linhas existentes do arquivo
			linhas = arquivo_csv.readlines()

			# Posicionar o ponteiro de arquivo no final
			arquivo_csv.seek(0, 2)

			# Verificar se é necessário adicionar uma quebra de linha no início
			if linhas and not linhas[-1].endswith('\n'):
				arquivo_csv.write('\n')

			writer = csv.writer(arquivo_csv)

			# Escrever os novos dados na última linha
			writer.writerow([alpha, cd, cl, cm_pitch])


		limpar = 'rm -r case/*00'
		subprocess.run(limpar, shell=True)
		if iteracao < 2000:
			limpar = 'rm -r case/' + str(int(iteracao/10)) + '*'
			subprocess.run(limpar, shell=True)

	cl_medio = cl_medio/len(angulos)    
	cd_medio = cd_medio/len(angulos)

	return cl_medio, cd_medio
