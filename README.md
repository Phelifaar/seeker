<p align="center"><img src="https://i.imgur.com/jo1qA2K.png"></p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3-blue.svg?style=plastic">
<img src="https://img.shields.io/badge/Translated_on-Russian-darkgreen.svg?style=plastic">
</p>

## Контакты разработчиков

### thewhiteh4t

<p align="center">
  <a href="https://twitter.com/thewhiteh4t"><b>Twitter</b></a>
  <span> - </span>
  <a href="https://t.me/thewhiteh4t"><b>Telegram</b></a>
  <span> - </span>
  <a href="https://thewhiteh4t.github.io"><b>Блог</b></a>
</p>

#### Phelifar

<p align="center">
  <a href="https://t.me/phelifaar"><b>Telegram</b></a>
</p>

<p align="center">
  <br>
  <b>Доступно в</b>
  <br>
  <img src="https://i.imgur.com/1wJVDV5.png">
</p>

Концепция Seeker проста, подобно тому, как мы размещаем фишинговые страницы для получения учетных данных, почему бы не разместить поддельную страницу, которая запрашивает ваше местоположение, как многие популярные веб-сайты, основанные на местоположении. Читать больше в <a href="https://thewhiteh4t.github.io">  блоге thewhiteh4t </a>. Seeker Hosts является фальшивым веб-сайтом **на встроенном PHP-сервере** и использует **ngrok** для создания ссылки, которую мы будем перенаправлять к цели, веб-сайт запрашивает разрешение на местоположение и, если цель позволяет, мы можем получить:

* Долгота
* Широта
* Точность
* Высота - Не всегда доступно
* Напрвление - Доступно, если пользователь движется
* Скорость - Доступно, если пользователь движется

Наряду с информацией о местоположении мы также получаем **информацию об устройстве** без каких-либо разрешений:

* Операционная система
* Платформа
* Количество ядер в CPU
* Количество RAM - Приблизительные Результаты
* Разрешение экрана
* Информация о GPU
* Данные браузера
* Публичный IP-адрес

**Этот инструмент является проверкой концепции и предназначен только для образовательных целей. Seeker показывает, какие данные может собирать вредоносный веб-сайт о вас и ваших устройствах, и почему вы не должны нажимать на случайные ссылки и разрешать критические разрешения, такие как местоположение и т.д.**

## Чем это отличается от IP GeoLocation

* Другие инструменты и сервисы предлагают IP-геолокацию, которая НЕ является точной и не дает определения местоположения цели, а является приблизительным местоположением провайдера.

* Seeker использует HTML API и получает разрешение на местоположение, а затем захватывает долготу и широту с помощью GPS оборудования, которое присутствует в устройстве, поэтому Seeker лучше всего работает со смартфонами, если отсутствует GPS-оборудование, например, на ноутбуке, Seeker откатится к IP-геолокации или будет искать кэшированные координаты.

* Как правило, если пользователь принимает разрешение на определение местоположения, точность полученной информации составляет **с точностью приблизительно до 30 метров**, точность зависит от устройства.

**P.S.** : На iPhone точность определения местоположения составляет примерно 65 метров.

## Шаблоны
<p align="centre">
  <h3> NearYou (От thewhiteh4t) </h3>
  <img src="https://i.imgur.com/v5vaYLS.png">
</p>

## Работает на :

* Kali Linux 2019.2
* BlackArch Linux
* Ubuntu 19.04
* Kali Nethunter
* Termux
* Parrot OS
* Windows 10

## Установка

### Kali Linux / Ubuntu / Parrot OS

```bash
git clone https://github.com/Phelifaar/seeker.git
cd seeker/
chmod 777 install.sh
./install.sh
```

### BlackArch Linux

```bash
pacman -S seeker
```

### Docker

```bash
docker pull Phelifaar/seeker
```

### Windows 10

1) Скачать и установить <a href="https://www.python.org"><b>Python 3</b></a>
2) Скачать и установить <b>от имени администратора</b> <a href="https://mega.nz/file/okZw1SpB#c5mIn6Pfgw5A1iqnnrHFvqwE6jg_5dPlJIZEHng2i8w"><b>PHP</b></a>
3) Установить <a href="https://winitpro.ru/index.php/2019/10/17/windows-openssh-server/"><b>SSH</b></a> через <a href="https://docs.microsoft.com/ru-ru/powershell/scripting/windows-powershell/starting-windows-powershell?view=powershell-7#at-the-command-prompt"><b>PowerShell</b></a>
4) Запустить win_install.bat

### Termux

```bash
git clone https://github.com/Phelifaar/seeker.git
cd seeker/
chmod 777 termux_install.sh
./termux_install.sh
```

## Использование

```bash
python3 seeker.py
