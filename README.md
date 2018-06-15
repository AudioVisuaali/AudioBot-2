# AudioBot-2
AudioBot-2 - This is the second version of audiobot. This version of the bot uses OOP, cached data, PostgreSQL and sqlalchemy for storing data!

# Features

* Command system (Create and manage your own commands)
* Get the AO canteen menus
* User information and profile picture inspection
* Meme system
* Random lennyfaces
* Calculate math equations
* Server leveling system
* Server ecomony system
* Bank to gather more points by saving points in the bank
* Minigames: Slots, Four in a line, Rock Paper scissors, Roulette, Duel, fishing and more coming
* Ability for different lists sorted by xp, points, tokens, wins in mode X and more
* Personal stats for minigames and roll
* Numberfacts
* Dog pictures and facts
* Cat pictures and facts
* Chronogg intregation
* Shop (Upcoming profile swag)
* Jokes: Normal jokes, Puns, dad, yo mama and Chuck Norris jokes
* Roll system, change to get random rewards
* Google, bumb google
* Youtube search
* Urban search
* Wikipedia search
* Translator with custom end languages
* Osu search user search and stats look up
* Timer reminder
* Strawpoll creation
* Trump 
* Fingerpori cartoon
* Text manipulation commands
* Dynamic time system, get time of place X
* Geolocation
* Ip resolver
* Find out what trump has said
* Message logging
* Ban phrase filter system incoming
* Kick, ban
* Set bots avatar
* Server stats and information

# Installation

### 1. Create Folder

Create folder

```
sudo mkdir /srv/audiobot
cd /srv/pajbot
```

### 2. Copy project

Copy project from github
```
# in /srv/audiobot
git clone https://github.com/AudioVisuaali/AudioBot-2.git .
```

### 3. Install Postgresql

Install Postgresql

```
apt-get install postgresql
```

configure user and database

```
sudo -u postgres psql

CREATE ROLE audiobot WITH LOGIN PASSWORD 'hdtry6gtresd';
CREATE DATABASE audiobot OWNER audiobot;
ALTER ROLE audiobot SET client_encoding = 'UTF8';
```
### 4. Settings up virtual envioriment

Setup virtual env

```
apt install virtualenv

virtualenv -p python3 botenv
source botenv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
```

### 5. Configure config file

In /srv/audiobot/maps/config.json set database 

### 6. Run bot

```
# Actiavte virtual enviorimental

source botenv/bin/activate
python start.py
```


