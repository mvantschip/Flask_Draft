from flask import Blueprint, request, url_for, render_template, redirect, session, flash, current_app
from bs4 import BeautifulSoup
from flaskdraft import db
from flaskdraft.search.forms import PlayerConfirm
from flaskdraft.models import bid
import requests
import re

search = Blueprint('search', __name__)


@search.route('/search', methods=['GET', 'POST'])
def search_page():
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
        test_value_table = soup.find('dl', {'class' : 'dl-horizontal'})
        test_value = test_value_table.findAll('dt')
        test_value_list = [i.string for i in test_value]
        for item in range(len(test_value_list)):
            if test_value_list[item] == 'Value':
                test_value_place = item
        value_total = soup.findAll('dd')[test_value_place].text
        if "k" in value_total or value_total == "£0":
            flash("Uw speler is minder waard dan €1 miljoen, waarde is gezet op €1 miljoen.", 'top')
            value_total = "1m"
        value = int(re.sub('[£m]', '', value_total))
        club = soup.findAll('dd')[3].text
        session['player_id'] = player_id
        session['player_name'] = player_choice
        session['player_value'] = value
        session['player_club'] = club
        return redirect(url_for('bids.bid_page'))
    return render_template('player.html', form_player = form_player)
