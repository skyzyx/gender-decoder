from flask import Flask
from flask import render_template, redirect, request
from wtforms.validators import ValidationError
import datetime
from app import app, db
from app.forms import JobAdForm
from app.models import JobAd, CodedWordCounter, TranslatedWordlist
from app.wordlists.wordlists_en import *


@app.route('/', methods=['GET', 'POST'])
def home():
    form = JobAdForm()
    if request.method == "POST" and form.validate_on_submit():
        ad = JobAd(form.texttotest.data, form.language.data)
        return redirect('results/{0}'.format(ad.hash))
    return render_template('home.html',
                          form=form)


@app.route('/about')
def about():
    return render_template('about.html',
        masculine_coded_words=masculine_coded_words,
        feminine_coded_words=feminine_coded_words)


@app.route('/results/<ad_hash>')
def results(ad_hash):
    job_ad = JobAd.query.get_or_404(ad_hash)
    masculine_coded_words, feminine_coded_words = job_ad.list_words()
    language, source = TranslatedWordlist.get_language_name_and_source(
                       job_ad.language)
    return render_template('results.html', job_ad=job_ad,
        masculine_coded_words=masculine_coded_words,
        feminine_coded_words=feminine_coded_words,
        explanation=job_ad.provide_explanation(),
        language=language,
        source=source)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
