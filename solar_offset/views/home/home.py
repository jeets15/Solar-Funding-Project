from flask import Blueprint, render_template, request, session, redirect
from solar_offset.utils.statistics_util import calculate_statistics

bp = Blueprint("home", __name__)


@bp.route("/")
def home():
    # Fetching the statistics
    stats = calculate_statistics()
    # Return the stats to the home.html
    return render_template("./home/home.html", statistics=stats)
