from quart import render_template

from . import meta_bp

from forms import SearchForm


@meta_bp.route("/", methods=["GET"])
async def _index():
    search_form = await SearchForm().create_form()

    return await render_template("meta/index.html", search_form=search_form)
