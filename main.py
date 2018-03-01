import requests
from bs4 import BeautifulSoup

maior_salario = 0

def main():
	base_url = 'http://www.portaldatransparencia.gov.br/'
	search = base_url+"servidores/Servidor-ListaServidores.asp?bogus=1&Pagina="

	cont = 1
	while True:
		pro = False

		get_link = requests.get(search+str(cont))
		
		site_html = BeautifulSoup(get_link.text, 'html.parser')


		get_func = site_html.find_all('a')

		for i in get_func:
			if 'Detalha' in i.get('href'):
				get_dados(base_url + 'servidores/' + i.get('href'), base_url)
				pro = True

		cont += 1

		if not pro: break

def get_dados(url, base):
	site = requests.get(url)
	new = BeautifulSoup(site.text, 'html.parser')
	dados = new.find_all('td', {'class':'colunaValor'})

	with open('funcionarios', 'a') as arquivo:
		
		funcionario = []

		for i in dados:
			arquivo.write(i.text.strip()+'\n')
			funcionario.append(i.text.strip())

		salario = get_salario_link(new, base, funcionario)
		arquivo.write('Salario : '+str(salario)+'\n')
		arquivo.write('======================== \n')


def get_salario_link(dados, base, funcionario):
	search = dados.find_all('a')

	for i in search:
		if 'Remuneracao' in i.get('href'):
			return get_salario(base + i.get('href'), funcionario)


def get_salario(url, funcionario):
	global maior_salario

	try:
		site = requests.get(url)
		dados = BeautifulSoup(site.text, 'html.parser')
		new = dados.find('tr', {'class':'remuneracaolinhatotalliquida'}).text

		for i in range(len(new)):
			if new[i].isnumeric():
				novo = new[i:].replace('.','').replace(',','').strip()
				
				if int(novo) > maior_salario:
					maior_salario = int(novo)
					
					with open('maior_salario','w') as maior:
						for i in funcionario:
							maior.write(i+'\n')
						maior.write('Salario : '+str(maior_salario))

				return int(novo)
	except Exception:
		return 'Salario não disponibilizado'
main()