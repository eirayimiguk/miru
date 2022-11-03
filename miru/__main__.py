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
    urls, _ = search_images(tags)
    return templates.TemplateResponse(
        "index.html", {"request": request, "urls": urls}
    )


@app.get('/tags')
def tags(request: Request):
    tags = get_tags()
    return templates.TemplateResponse(
        "tags.html", {"request": request, "tags": tags}
    )


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
