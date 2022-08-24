from flask import Flask, render_template, redirect, request
import data_manager, os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/static/resources/uploaded-images"
ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route("/", methods=['GET', 'POST'])
def main_page():
    latest_qs = data_manager.get_latest_questions()

    return render_template("index.html", questions=latest_qs)


@app.route("/list", methods=['GET', 'POST'])
def list_questions():
    if "sort_by" in request.url:
        if request.args['sort_by'] == "views-desc":
            questions = data_manager.sort_questions(views=True, desc=True)
        elif request.args['sort_by'] == "views-asc":
            questions = data_manager.sort_questions(views=True)
        elif request.args['sort_by'] == "votes-desc":
            questions = data_manager.sort_questions(votes=True, desc=True)
        elif request.args['sort_by'] == "votes-asc":
            questions = data_manager.sort_questions(votes=True)
        elif request.args['sort_by'] == "submission-desc":
            questions = data_manager.sort_questions(submission=True, desc=True)
        elif request.args['sort_by'] == "submission-asc":
            questions = data_manager.sort_questions(submission=True)
    else:
        questions = data_manager.sort_questions(submission=True, desc=True)

    # questions_tags = []
    # for que in questions:
    #     questions_tags.append(data_manager.get_tags_for_question(question_id=que['id']))

    return render_template("list.html", questions=questions)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    question = {}

    if request.method == "POST":
        question["id"] = data_manager.get_next_question_id()
        question["submission_time"] = data_manager.get_time()
        question["view_number"] = 0
        question["vote_number"] = 0
        question["title"] = request.form["question"]
        question["message"] = request.form["description"]

        if request.files['img']:
            img = request.files['img']
            if img and allowed_file(img.filename):
                filename = secure_filename(img.filename)

                absolute_path = os.path.dirname(__file__)
                relative_path = "static\\resources\\uploaded-images"
                full_path = os.path.join(absolute_path, relative_path)

                img.save(os.path.join(full_path, filename))

            question["image"] = f"static/resources/uploaded-images/{filename}"
        else:
            question['image'] = ""

        question_id = question["id"]
        data_manager.add_question_db(new_question=question)

        return redirect(f"/question/{question_id}")

    return render_template("add-question.html")


@app.route("/question/<int:question_id>", methods=["POST", "GET"])
def display_question(question_id):
    if request.method == "POST":
        if request.form["to_question"] == "to-question":
            data_manager.modify_value_in_question(question_id=question_id, view="to-question")
        if 'tag_name' in request.form:
            tag_to_add = request.form['tag_name']
            tag_id = data_manager.get_tag_id(tag_to_add)
            data_manager.add_tag_to_question(question_id, tag_id)

    tags_for_question = data_manager.get_tags_for_question(question_id)
    all_tags = data_manager.get_all_tags()
    question_of_given_id = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_db(question_id)
    comments_for_question = data_manager.get_comments_for_question_db(question_id)
    comments_for_answers = data_manager.get_comments_for_answers_db(answers)

    """ SYNTAX FOR COMMENTS_FOR_ANSWERS - NEED 3 FOR LOOP
    all comment list []
       comments for an answer list []
          comment elements dictionary {}
    """

    return render_template('question.html', question_of_given_id=question_of_given_id, answers_to_question=answers,
                           comments_for_question=comments_for_question, comments_for_answers=comments_for_answers,
                           question_id=question_id, tags_for_question=tags_for_question, all_tags=all_tags)


@app.route("/question_voting/<int:question_id>", methods=['POST'])
def question_voting(question_id):
    if request.method == "POST":
        if request.form["vote"] == "vote-up":
            data_manager.modify_value_in_question(question_id=question_id, voting="vote-up")

        elif request.form['vote'] == "vote-down":
            data_manager.modify_value_in_question(question_id=question_id, voting="vote-down")

        if request.form["page"] == "list":
            return redirect("/list")

        elif request.form["page"] == "question":
            return redirect(f"/question/{question_id}")


@app.route("/delete_question/<int:question_id>")
def delete_question(question_id):
    sel_que = data_manager.get_question_by_id(question_id)
    img_path = sel_que['image']
    if img_path:
        os.remove(img_path)
    data_manager.delete_question(question_id)

    return redirect("/list")


@app.route("/question/<int:question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == "POST":
        modified_title = request.form["question"]
        modified_message = request.form["description"]

        data_manager.modify_value_in_question(question_id=question_id, edited_question=True, title=modified_title,
                                              message=modified_message)

        return redirect(f"/question/{question_id}")
    else:
        question_of_given_id = data_manager.get_question_by_id(question_id)

    return render_template("edit-question.html", question_for_edit=question_of_given_id)


@app.route("/question/<int:question_id>/new-answer", methods=["POST", "GET"])
def add_answer(question_id):
    answer = {}

    if request.method == "POST":
        answer["id"] = data_manager.get_next_answer_id()
        answer["submission_time"] = data_manager.get_time()
        answer["vote_number"] = 0
        answer["question_id"] = question_id
        answer["message"] = request.form["description"]

        if request.files['img']:
            img = request.files['img']
            if img and allowed_file(img.filename):
                filename = secure_filename(img.filename)

                absolute_path = os.path.dirname(__file__)
                relative_path = "static\\resources\\uploaded-images"
                full_path = os.path.join(absolute_path, relative_path)

                img.save(os.path.join(full_path, filename))

            answer["image"] = f"static/resources/uploaded-images/{filename}"
        else:
            answer['image'] = ""

        data_manager.add_answer_db(answer)

        return redirect(f"/question/{question_id}")

    return render_template("add-answer.html", question_id=question_id)


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    question_id = data_manager.get_answer_question_id(answer_id)
    ans_que = data_manager.get_answer_by_id(answer_id)
    img_path = ans_que['image']
    if img_path:
        os.remove(img_path)
    data_manager.delete_answer_and_comments(answer_id)

    return redirect(f"/question/{question_id}")


@app.route("/answer/<int:answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == "POST":
        modified_message = request.form["message"]
        ans_question_id = data_manager.get_answer_question_id(answer_id)

        data_manager.modify_value_in_answer(answer_id=answer_id, edited_answer=True, message=modified_message)

        return redirect(f"/question/{ans_question_id}")
    else:
        answer_of_given_id = data_manager.get_answer_by_id(answer_id)

    return render_template("edit-answer.html", answer_for_edit=answer_of_given_id)


@app.route("/answer_voting/<int:answer_id>", methods=['POST'])
def answer_voting(answer_id):
    ans_question_id = data_manager.get_answer_question_id(answer_id)
    if request.form["vote"] == "vote-up":
        data_manager.modify_value_in_answer(answer_id=answer_id, voting="vote-up")

    elif request.form['vote'] == "vote-down":
        data_manager.modify_value_in_answer(answer_id=answer_id, voting="vote-down")

    return redirect(f"/question/{ans_question_id}")


@app.route("/search", methods=['POST'])
def search():
    search_phrase = request.form["search_phrase"]
    matching_questions = data_manager.get_search_results(search_phrase)

    return render_template("list.html", questions=matching_questions, search_phrase=search_phrase)


@app.route("/answer/<int:answer_id>/new-comment", methods=["POST", "GET"])
@app.route("/question/<int:question_id>/new-comment", methods=["POST", "GET"])
def add_comment(question_id=-1, answer_id=-1):
    comment = {}
    if request.method == "POST":
        comment["id"] = data_manager.get_next_comment_id()
        if question_id >= 0:
            comment["question_id"] = question_id
        else:
            question_id = data_manager.get_answer_question_id(answer_id)
            comment["answer_id"] = answer_id

        comment["message"] = request.form["description"]
        comment["submission_time"] = data_manager.get_time()
        comment["edited_count"] = 0

        data_manager.add_comment_db(new_comment=comment)

        return redirect(f"/question/{question_id}")

    if question_id >= 0:
        return render_template("add-comment.html", question_id=str(question_id))
    else:
        return render_template("add-comment.html", answer_id=str(answer_id))


@app.route("/comment/<int:comment_id>/delete")
def delete_comment(comment_id):
    question_id = data_manager.get_comment_question_id(comment_id)
    data_manager.delete_comment(comment_id)

    return redirect(f"/question/{question_id}")


@app.route("/comment/<int:comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == "POST":
        modified_message = request.form["description"]
        modified_submission_time = data_manager.get_time()
        comment_question_id = data_manager.get_comment_question_id(comment_id)

        data_manager.modify_value_in_comment(comment_id=comment_id, message=modified_message,
                                             submission_time=modified_submission_time)

        return redirect(f"/question/{comment_question_id}")
    else:
        comment_of_given_id = data_manager.get_comment_by_id(comment_id)

    return render_template("edit-comment.html", comment_for_edit=comment_of_given_id)


@app.route('/question/<int:question_id>/new-tag', methods=["POST", "GET"])
def add_tag(question_id):
    all_tags = data_manager.get_all_tags()
    if request.method == "POST":
        if 'custom_tag_name' in request.form:
            tag_to_add = request.form['custom_tag_name']
            data_manager.add_custom_tag(tag_to_add)
            tag_id = data_manager.get_tag_id(tag_to_add)[0]['id']
            data_manager.add_tag_to_question(question_id, tag_id)
        elif 'tag_name' in request.form:
            tag_to_add = request.form['tag_name']
            tag_id = data_manager.get_tag_id(tag_to_add)[0]['id']
            data_manager.add_tag_to_question(question_id, tag_id)
        return redirect(f"/question/{question_id}")

    return render_template("add-tag.html", tags=all_tags, question_id=question_id)


@app.route('/question/<int:question_id>/tag/<int:tag_id>/delete', methods=['POST'])
def delete_tag(question_id, tag_id):
    data_manager.delete_tag_from_question(question_id, tag_id)

    return redirect(f'/question/{question_id}')


@app.route('/bonus-questions')
def bonus_questions():
    bonus_questions_list = data_manager.get_bonus_questions()

    return render_template("bonus-questions.html", questions=bonus_questions_list)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
