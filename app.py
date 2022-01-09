from flask import Flask
from flask import jsonify
from flask import Flask,render_template,redirect, url_for, request
import json
import time
import datetime
import os

localtime = time.asctime( time.localtime(time.time()))

