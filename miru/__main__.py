import logging

from optparse import OptionParser

from flask import Flask, render_template, request

from miru.batch import search_images, update_tags, get_tags


app = Flask(__name__, template_folder="web/templates", static_folder="web/static")


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        tags = request.form["tags"].split(", ")
        urls = search_images(tags)
        return render_template("index.html", urls=urls)


@app.route('/update')
def update():
    update_tags()
    return render_template("update.html")


@app.route('/tags')
def tags():
    tags = get_tags()
    return render_template("tags.html", tags=tags)


if __name__ == "__main__":
    # parse options
    parser = OptionParser()
    parser.add_option(
        "-v", "--verbose",
        action="store_true", dest="verbose", default=False,
        help="debug log")
    (options, _) = parser.parse_args()

    # set log-level
    FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=FORMAT)

    app.run(debug=True, port=9090, threaded=True)
