from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.category import Category


category_bp = Blueprint(
    "category",
    __name__
)


@category_bp.route("/categories")
@login_required
def categories():

    categories = Category.query.filter_by(
        user_id=current_user.id,
        archived=False
    ).all()

    return render_template(
        "categories.html",
        categories=categories
    )


@category_bp.route(
    "/categories/add",
    methods=["POST"]
)
@login_required
def add_category():

    name = request.form.get("name")

    if not name:
        flash(
            "Category name required.",
            "danger"
        )

        return redirect(
            url_for("category.categories")
        )

    category = Category(
        user_id=current_user.id,
        name=name
    )

    db.session.add(category)
    db.session.commit()

    flash(
        "Category added.",
        "success"
    )

    return redirect(
        url_for("category.categories")
    )


@category_bp.route(
    "/categories/archive/<int:id>"
)
@login_required
def archive_category(id):

    category = Category.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    category.archived = True

    db.session.commit()

    flash(
        "Category archived.",
        "success"
    )

    return redirect(
        url_for("category.categories")
    )