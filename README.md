# Where's that Pokemon? Card allocation management for players and collectors

Players and collectors of trading card games often run into a costly problem: where did that card go? Knowing you own 6 copies of a card isn't useful if you don't know where any of them are, and inventory spreadsheets are hard to keep up to date when the process of deck building is constantly moving cards around.
   
*Where's that Pokemon?* aims to solve the problem by integrating deck construction into inventory management. As you build and modify decks, card inventory is automatically managed behind the scenes to prevent losing track of their storage location.

## Installation
1. Set up a PostgreSQL server somewhere. I use a raspberry pi on my home network, and if you want to go that route [I suggest following step 6 of this tutorial on setting up a mastodon instance.](https://pimylifeup.com/raspberry-pi-mastodon/) Most cloud providers offer these kinds of services for free or low cost. Amazon Web Services has [a tutorial on setting up a free PostgreSQL instance](https://aws.amazon.com/getting-started/hands-on/create-connect-postgresql-db/) if that fits your needs better.
2. Download this repository using `git clone --recurse-submodules https://github.com/chrisbrickhouse/ptcg-inventory.git`
3. Navigate to the site directory using `cd ptcg-inventory/cardsite`
4. Install the python dependancies using `python -m pip install -r requirements.txt`
5. Install the grunt dependancies using `npm install` 
6. Navigate to the ptcg-inventory directory using `cd ..`
7. Configure the Django site and database using [the instructions for configuring a site](#Configuring the site)
7. Import the card data using `python make_set_fixtures.py`

### Configuring the site
To get the site running, you need to modify `cardsite/my_pokemon_cards/settings.py` to point to your PostgreSQL server.
1. In `cardsite/my_pokemon_cards/settings.py` modify the `DATABASES` entry with the information for your SQL server. If you need help, see [the reference doc](https://docs.djangoproject.com/en/5.0/ref/settings/#databases).
2. Set a `SECRET_KEY`. By default, the distributed settings check for an environment variable with that info, but you can also add it to the file directly. You can use `django.core.management.utils.get_random_secret_key()` to generate one.

## Roadmap

*Where's that Pokemon?* is still in initial development and the interface may change rapidly. The roadmap below contains planned features and likely migrations to help mitigate disruption. The main use case is for hobbyists who want to run their own instance, but long term it may be useful to deploy as a platform.
 - ~~Minimal viable deck building interface~~
   - ~~New deck~~
   - ~~Deck details~~
   - ~~Add and remove cards from deck~~
 - ~~Implement storage locations~~
   - ~~Generic CardStash table~~
   - ~~Migrate Deck to subclass of CardStash~~ (Destructive)
   - ~~Migrate CardAllocation to use CardStash~~ (Destructive)
 - ~~Collection overview page~~
   - ~~List summary stats for a collection~~
 - Overview of each CardStash
 - CardStash to CardStash allocation interface
   - Select two CardStashes and move cards between them
   - Modify Deck building interface to wrap this as an implementation of moving cards to and from  deck and storage
 - Feature Freeze
   - Improve testing and fix observed bugs
   - Front-end styling to make the interface pretty
 - Release 1.0 - minimal viable product
 - TCG Player integration
   - [Pricing for cards](https://docs.tcgplayer.com/reference/pricing) in collection or needed for decks
   - (Long term, needs defined) [Store management integration](https://docs.tcgplayer.com/reference/stores)
 - User accounts (Long term, needs defined)
