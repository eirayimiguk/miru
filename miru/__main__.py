import logging

from optparse import OptionParser

import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from miru.batch import search_images, update_tags, get_tags


app = FastAPI(title="Miru for Notion")
templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request}
    )

@app.post("/")
async def index(request: Request):
    data = await request.form()
    tags = [x.strip() for x in data["tags"].split(",") if not x.strip() == '']
    urls = search_images(tags)
    return templates.TemplateResponse(
        "index.html", {"request": request, "urls": urls}
    )


# @app.route('/', methods=["GET", "POST"])
# def index():
#     if request.method == "GET":
#         return render_template("index.html")
#     if request.method == "POST":
#         tags = request.form["tags"].split(", ")
#         urls = search_images(tags)
#         return render_template("index.html", urls=urls)
#
#
# @app.route('/update')
# def update():
#     update_tags()
#     return render_template("update.html")
#
#
# @app.route('/tags')
# def tags():
#     tags = get_tags()
#     return render_template("tags.html", tags=tags)


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

    uvicorn.run(app=app, host="0.0.0.0", port=9090)
