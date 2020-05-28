from flask import Blueprint, request, url_for, render_template, redirect, session, flash, current_app
from bs4 import BeautifulSoup
from flaskdraft import db
from flaskdraft.main.forms import PlayerSearch
from flaskdraft.models import bid
from sqlalchemy import func
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
    subq = bid.query.distinct(bid.player_id).subquery()
    rows = bid.query.select_entity_from(subq).order_by(bid.date_bid.desc()).all()
    for row in rows:
        row.date_bid = row.date_bid.replace(tzinfo=pytz.utc)
        row.date_bid = row.date_bid.astimezone()
    return render_template('overview.html', rows = rows)
