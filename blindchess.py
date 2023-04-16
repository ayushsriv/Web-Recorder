#
# Web based GUI for BBC chess engine
#

# packages
from flask import Flask
from flask import render_template

# create web app instance
blindchess = Flask(__name__)

# define root(index) route
@chess.route('/chess')
def root():
    return render_template('blindchess.html')

# main driver
if __name__ == '__main__':
    # start HTTP server
    blindchess.run(debug=True, threaded=True)
