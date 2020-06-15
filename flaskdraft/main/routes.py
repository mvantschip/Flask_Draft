from flask import Blueprint, request, url_for, render_template, redirect, session, flash, current_app
from bs4 import BeautifulSoup
from flaskdraft import db
from flaskdraft.main.forms import PlayerSearch
from flaskdraft.models import bid
from sqlalchemy import func
from datetime import datetime
import pytz
import requests
import re


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form_search = PlayerSearch()
    try:
        if request.method == 'POST' and form_search.validate():
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
            results_page = requests.get("https://sortitoutsi.net/search/database?q=" + form_search.name.data + "&game_id=11&type=player", headers = headers).text
            soup = BeautifulSoup(results_page, 'html.parser')
            names_list = soup.find('table', {'class' : 'table table-striped'})
            names = []
            for link in names_list.findAll('a', title=True):
                names.append(link.get('title'))
            session['names'] = names
            session['search_value'] = form_search.name.data
            return redirect(url_for('search.search_page'))
    except:
        flash("Speler niet gevonden!", 'bottom')
        return render_template('index.html', form_search = form_search)
    return render_template('index.html', form_search = form_search)


@main.route('/overview', methods=['GET', 'POST'])
def overview():
    subq = bid.query.distinct(bid.player_id).order_by(bid.player_id, bid.date_bid.desc()).subquery()
    rows = bid.query.select_entity_from(subq).order_by(bid.date_bid.desc()).all()
    confirmed_list = []
    for row in rows:
        #check if 12 hours have passed to mark the confirmed bids as green
        elapsed_time = (datetime.utcnow() - row.date_bid).total_seconds()
        elapsed_time_hours = int(elapsed_time // 3600)
        if  elapsed_time_hours > 12:
            confirmed_list.append("True")
        else:
            confirmed_list.append("False")
        #for heroku, specific timezone conversion is required
        row.date_bid = row.date_bid.replace(tzinfo=pytz.utc)
        tz = pytz.timezone('Europe/Amsterdam')
        row.date_bid = row.date_bid.astimezone(tz)
    return render_template('overview.html', rows = rows, confirmed_list = confirmed_list)
