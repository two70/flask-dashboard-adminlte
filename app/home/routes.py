# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from .kegman import kegman
import json

@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html', kegman=kegman.conf)

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith( '.html' ):
            template += '.html'

        if template == "tune.html":
            return render_template( template, kegman=kegman.conf )

        return render_template( template )

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500

@blueprint.route('/api/kegman', methods=['POST', 'GET'])
@login_required
def kegman_data():
    d = request.form.to_dict()
    json = request.get_json()
    print(json)

    itemChanged = False
    try:
        for item in kegman.conf:
            if item in json and str(json[item]) != str(kegman.conf[item]) and float(json[item]) != float(kegman.conf[item]) and not item in ['identifier', 'time']:
                print(item, json[item], kegman.conf[item])
                kegman.conf[item] = str(json[item])
                itemChanged = True
            else:
                json[item] = kegman.conf[item]
        if itemChanged:
            kegman.element_updated = True
            kegman.write_config(kegman.conf)
            #tunePush.send_json(kegman.conf)
    except:
        pass
    return kegman.conf
