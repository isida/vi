![alt text](https://raw.githubusercontent.com/isida/vi/master/images/isida-logo-v6-big.png "iSida bot")

6th generation
======

Required:
* configparser
* chardet
* feedparser
* requests
* pysocks (for socks proxy feature)

------

More info:
* Official [site](https://github.com/isida/vi)
* Telegram chat: [@isida_bot_dev](https://t.me/isida_bot_dev)
* Bot: [@isida_bot](https://t.me/isida_bot)

------

Quick start:
```
pip3 install chardet
pip3 install feedparser
pip3 install requests
pip3 install pysocks
git clone https://github.com/isida/vi.git isida-vi
cd isida-vi
cp settings/config.ini.demo settings/config.ini
nano settings/config.ini
python3 isida.py
```

------

Quick start with Docker:
```
git clone https://github.com/isida/vi.git isida-vi
cd isida-vi
cp settings/config.ini.demo settings/config.ini
nano settings/config.ini
docker build -t isida-vi .
docker run -d isida-vi
```

------

Copyright 2oo9..2o24 by [diSabler](http://dsy.name) under [GPLv3](http://www.gnu.org/licenses/gpl.txt) Licence
