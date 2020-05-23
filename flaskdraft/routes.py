from datetime import datetime
from flask import request, url_for, render_template, redirect, session, flash
from bs4 import BeautifulSoup
from flaskdraft import app, db
from flaskdraft.forms import PlayerSearch, PlayerConfirm, PlaceBids
from flaskdraft.models import bid
from wtforms.validators import NumberRange
from sqlalchemy import func
import requests
import re


@app.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('player'))
    except:
        flash("Speler niet gevonden!", 'bottom')
        return render_template('index.html', form_search = form_search)
    return render_template('index.html', form_search = form_search)

@app.route('/player', methods=['GET', 'POST'])
def player():
    form_player = PlayerConfirm()
    names = session.get('names')
    form_player.player.choices = [(names, names) for names in names]
    if request.method == 'POST' and form_player.validate_on_submit():
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        results_page = requests.get("https://sortitoutsi.net/search/database?q=" + session.get('search_value') + "&game_id=11&type=player", headers = headers).text
        soup = BeautifulSoup(results_page, 'html.parser')
        player_choice = form_player.player.data
        url = soup.find('a', {'title' : player_choice})['href']
        segments = url.split('/')
        player_id = segments[5]
        player_page = requests.get("https://sortitoutsi.net/football-manager-2020/player/" + player_id + "/" + player_choice, headers = headers).text
        soup = BeautifulSoup(player_page, 'html.parser')
        value_total = soup.findAll('dd')[8].text
        if "k" in value_total or value_total == "£0":
            flash("Uw speler is minder waard dan €1 miljoen, waarde is gezet op €1 miljoen.", 'top')
            value_total = "1m"
        value = int(re.sub('[£m]', '', value_total))
        club = soup.findAll('dd')[3].text
        session['player_id'] = player_id
        session['player_name'] = player_choice
        session['player_value'] = value
        session['player_club'] = club
        return redirect(url_for('bids'))
    return render_template('player.html', form_player = form_player)

@app.route('/bids', methods=['GET', 'POST'])
def bids():
    player_id = session.get('player_id')
    player_name = session.get('player_name')
    player_value = session.get('player_value')
    player_club = session.get('player_club')
    check_bid = bid.query.filter_by(player_id = player_id).order_by(bid.date_bid.desc()).first()
    if check_bid:
        current_bid_username = check_bid.username
        elapsed_time = ((datetime.utcnow() - check_bid.date_bid).total_seconds())
        elapsed_time_hours = int(elapsed_time // 3600)
        elapsed_time_minutes = int((elapsed_time % 3600) // 60)
        if  elapsed_time_hours > 12:
            flash(f"{player_name} is al gekocht door {current_bid_username}. U kunt deze speler niet meer kopen.", 'danger')
        current_bid_value = round(check_bid.user_bid, 2)
        min_overbid_value = round((current_bid_value * 1.1), 2)
        form_bids = PlaceBids(bid_player_name = player_name, bid_player_value = min_overbid_value)
        flash(f"Huidig bod is: €{current_bid_value} miljoen, geboden door {current_bid_username}, {elapsed_time_hours} uur en {elapsed_time_minutes} minuten geleden. U moet 10% meer bieden, dus minimaal: €{min_overbid_value} miljoen.", 'top')
    else:
        form_bids = PlaceBids(bid_player_name = player_name, bid_player_value = player_value)
    if request.method == 'POST' and form_bids.validate_on_submit():
        if form_bids.bid_player_value.data < player_value:
            session.pop('_flashes', None)
            flash("Uw bod is lager dan de minimale waarde van de speler, probeer opnieuw.", 'bottom')
            return redirect(url_for('bids'))
        elif check_bid and round(form_bids.bid_player_value.data, 2) < min_overbid_value:
            session.pop('_flashes', None)
            flash("Uw bod is te laag om te kunnen overbieden, probeer opnieuw.", 'bottom')
            return redirect(url_for('bids'))
        else:
            user_bid = bid(player_id = player_id, player_name = form_bids.bid_player_name.data, player_value = player_value, username = form_bids.username.data, user_bid = round(form_bids.bid_player_value.data, 2))
            db.session.add(user_bid)
            db.session.commit()
            flash(f"Bod geplaatst! U heeft €{form_bids.bid_player_value.data} miljoen geboden op {form_bids.bid_player_name.data}!", 'bottom')
            return render_template('bids.html', form_bids = form_bids, player_name = player_name, player_club = player_club, player_value = player_value)
    return render_template('bids.html', form_bids = form_bids, player_name = player_name, player_club = player_club, player_value = player_value)

@app.route('/overview', methods=['GET', 'POST'])
def overview():
    rows = bid.query.with_entities(bid.username, bid.player_name, bid.user_bid, bid.date_bid, func.max(bid.date_bid)).group_by(bid.player_id).order_by(bid.date_bid.desc()).all()
    return render_template('overview.html', rows = rows)
