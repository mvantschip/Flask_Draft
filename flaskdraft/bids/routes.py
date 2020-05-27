from datetime import datetime
from flask import Blueprint, request, url_for, render_template, redirect, session, flash, current_app
from flaskdraft import db
from flaskdraft.bids.forms import PlaceBids
from flaskdraft.models import bid

bids = Blueprint('bids', __name__)

@bids.route('/bids', methods=['GET', 'POST'])
def bid_page():
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
            return redirect(url_for('bid_page'))
        elif check_bid and round(form_bids.bid_player_value.data, 2) < min_overbid_value:
            session.pop('_flashes', None)
            flash("Uw bod is te laag om te kunnen overbieden, probeer opnieuw.", 'bottom')
            return redirect(url_for('bid_page'))
        else:
            user_bid = bid(player_id = player_id, player_name = form_bids.bid_player_name.data, player_value = player_value, username = form_bids.username.data, user_bid = round(form_bids.bid_player_value.data, 2))
            db.session.add(user_bid)
            db.session.commit()
            session.pop('_flashes', None)
            flash(f"Bod geplaatst! U heeft €{form_bids.bid_player_value.data} miljoen geboden op {form_bids.bid_player_name.data}! U kunt een nieuw bod plaatsen.", 'bottom')
            return redirect(url_for('main.index'))
            #return render_template('bids.html', form_bids = form_bids, player_name = player_name, player_club = player_club, player_value = player_value)
    return render_template('bids.html', form_bids = form_bids, player_name = player_name, player_club = player_club, player_value = player_value)
