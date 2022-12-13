from flask import Flask, url_for, redirect, request, render_template

app = Flask(__name__)

from application.views import *
