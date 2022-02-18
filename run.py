#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diabeteswarrior Runtime"""

from flaskblog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
