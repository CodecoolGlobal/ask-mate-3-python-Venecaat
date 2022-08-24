import os

import connection, bonus_questions
from datetime import datetime


# QUESTION_COLUMNS = ['id', 'submission_time', "view_number", "vote_number", "title", "message", "image"]
# ANSWER_COLUMNS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
# COMMENT_COLUMNS = ["id", "question_id", "answer_id", "message", "submission_time", "edited_count"]
# TAG_COLUMNS = ["id", "name"]


def sort_questions(views=False, votes=False, submission=False, desc=False):
    questions = get_questions_db()

    if views:
        return sorted(questions, key=lambda x: int(x['view_number']), reverse=desc)
    elif votes:
        return sorted(questions, key=lambda x: int(x['vote_number']), reverse=desc)
    elif submission or not submission:
        return sorted(questions, key=lambda x: x['submission_time'], reverse=desc)


def get_time():
    curr_date = datetime.now()
    norm_time = curr_date.strftime("%Y/%m/%d %H:%M:%S")

    return norm_time


# ----------------------------------------------------------------------------------------------------
# Get all question/answer/comment/tag from corresponding tables

@connection.connection_handler
def get_questions_db(cursor):
    cursor.execute("SELECT * FROM question")
    return cursor.fetchall()


@connection.connection_handler
def get_questions_ids(cursor):
    cursor.execute("SELECT id FROM question")
    return cursor.fetchall()


@connection.connection_handler
def get_answers_db(cursor, question_id):
    cursor.execute(f"SELECT * FROM answer WHERE question_id = {question_id} ORDER BY id")
    return cursor.fetchall()


@connection.connection_handler
def get_comments_for_question_db(cursor, question_id):
    cursor.execute(f"SELECT * FROM comment WHERE question_id = {question_id} ORDER BY id")
    return cursor.fetchall()


@connection.connection_handler
def get_comments_for_answers_db(cursor, answers):
    comments = []
    for ans in answers:
        cursor.execute(f"""
        SELECT id, question_id, answer_id, submission_time, message, edited_count
        FROM comment
        WHERE answer_id = {ans['id']}
        ORDER BY id
        """)
        comments.append(cursor.fetchall())
    return comments


# ----------------------------------------------------------------------------------------------------
# Add question/answer/comment/tag to corresponding tables

@connection.connection_handler
def add_question_db(cursor, new_question):
    cursor.execute(
        f"""
        INSERT INTO question
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """,
        (new_question['id'], new_question['submission_time'], new_question['view_number'], new_question['vote_number'],
         new_question['title'], new_question['message'], new_question['image'])
    )


@connection.connection_handler
def add_answer_db(cursor, new_answer):
    cursor.execute(
        """
        INSERT INTO answer
        VALUES(%s, %s, %s, %s, %s, %s)
        """,
        (new_answer['id'], new_answer['submission_time'], new_answer['vote_number'], new_answer['question_id'],
         new_answer['message'], new_answer['image'])
    )


@connection.connection_handler
def add_comment_db(cursor, new_comment):
    if "question_id" in new_comment.keys():
        cursor.execute("""
            INSERT INTO comment (id, question_id, message, submission_time, edited_count)
            VALUES(%s, %s, %s, %s, %s)""", (new_comment['id'], new_comment['question_id'], new_comment['message'],
                                            new_comment['submission_time'], new_comment['edited_count'])
                       )
    else:
        cursor.execute("""
            INSERT INTO comment (id, answer_id, message, submission_time, edited_count)
            VALUES(%s, %s, %s, %s, %s)""", (new_comment['id'], new_comment['answer_id'], new_comment['message'],
                                            new_comment['submission_time'], new_comment['edited_count'])
                       )


# ----------------------------------------------------------------------------------------------------
# Get next ID for question/answer/comment/tag from corresponding tables

@connection.connection_handler
def get_next_question_id(cursor):
    cursor.execute("SELECT MAX(id) as id FROM question")
    return cursor.fetchall()[0]['id'] + 1


@connection.connection_handler
def get_next_answer_id(cursor):
    cursor.execute("SELECT MAX(id) as id FROM answer")
    return cursor.fetchall()[0]['id'] + 1


@connection.connection_handler
def get_next_comment_id(cursor):
    cursor.execute("SELECT MAX(id) as id FROM comment")
    return cursor.fetchall()[0]['id'] + 1


# ----------------------------------------------------------------------------------------------------
# Delete question/answer/comment from corresponding tables

@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute(f"SELECT image FROM answer WHERE question_id = {question_id}")
    answer_images = cursor.fetchall()
    # cursor.execute(f"""
    # DELETE FROM comment WHERE answer_id IN
    # (SELECT answer.id FROM answer JOIN question ON answer.question_id = question.id
    #  WHERE answer.question_id = {question_id})
    # """)
    # cursor.execute(f"DELETE FROM comment WHERE question_id = {question_id}")
    # cursor.execute(f"DELETE FROM question_tag WHERE question_id = {question_id}")
    # cursor.execute(f"DELETE FROM answer WHERE question_id = {question_id}")
    cursor.execute(f"DELETE FROM question WHERE id = {question_id}")

    for d in answer_images:
        os.remove(d['image'])


@connection.connection_handler
def delete_answer_and_comments(cursor, answer_id):
    cursor.execute(f"DELETE FROM comment WHERE answer_id = {answer_id}")
    cursor.execute(f"DELETE FROM answer WHERE id = {answer_id}")


@connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute(f"DELETE FROM comment WHERE id = {comment_id}")


# ----------------------------------------------------------------------------------------------------
# Get question/answer/comment/tag by ID from corresponding tables

@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute(f"SELECT * FROM question WHERE id = {question_id}")
    return cursor.fetchall()[0]


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute(f"SELECT * FROM answer WHERE id = {answer_id}")
    return cursor.fetchall()[0]


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute(f"SELECT * FROM comment WHERE id = {comment_id}")
    return cursor.fetchall()[0]


# ----------------------------------------------------------------------------------------------------
# Get an answer's/comment's question_id

@connection.connection_handler
def get_answer_question_id(cursor, answer_id):
    cursor.execute(f"SELECT question_id FROM answer WHERE id = {answer_id}")
    return cursor.fetchall()[0]["question_id"]


@connection.connection_handler
def get_comment_question_id(cursor, comment_id):
    cursor.execute(f"""
    SELECT
    CASE
        WHEN comment.question_id IS NOT NULL THEN comment.question_id
        ELSE answer.question_id
    END AS question_id
    FROM comment
    LEFT JOIN answer ON comment.answer_id = answer.id
    WHERE comment.id = {comment_id}
    LIMIT 1
    """)
    return cursor.fetchall()[0]["question_id"]


# ----------------------------------------------------------------------------------------------------
# Modify question/answer/comment/tag in corresponding tables

@connection.connection_handler
def modify_value_in_question(cursor, question_id, voting="", view="", edited_question=False, title="", message=""):
    if view:
        cursor.execute(f"UPDATE question SET view_number = view_number + 1 WHERE id = {question_id}")
    elif voting == "vote-up":
        cursor.execute(f"UPDATE question SET vote_number = vote_number + 1 WHERE id = {question_id}")
    elif voting == "vote-down":
        cursor.execute(f"UPDATE question SET vote_number = vote_number - 1 WHERE id = {question_id}")
    if edited_question:
        cursor.execute(f"UPDATE question SET title = '{title}', message = '{message}' WHERE id = {question_id}")


@connection.connection_handler
def modify_value_in_answer(cursor, answer_id, voting="", edited_answer=False, message=""):
    if voting == "vote-up":
        cursor.execute(f"UPDATE answer SET vote_number = vote_number + 1 WHERE id = {answer_id}")
    elif voting == "vote-down":
        cursor.execute(f"UPDATE answer SET vote_number = vote_number - 1 WHERE id = {answer_id}")
    if edited_answer:
        cursor.execute(f"UPDATE answer SET message = '{message}' WHERE id = {answer_id}")


@connection.connection_handler
def modify_value_in_comment(cursor, comment_id, message, submission_time):
    cursor.execute(f"""
    UPDATE comment SET message = '{message}', edited_count = edited_count + 1,
    submission_time = '{submission_time}'
    WHERE id = {comment_id}
    """)


# ----------------------------------------------------------------------------------------------------
# Search results

@connection.connection_handler
def get_latest_questions(cursor):
    cursor.execute(
        """
        SELECT * FROM question
        ORDER BY submission_time DESC
        LIMIT 5
        """
    )

    return cursor.fetchall()


@connection.connection_handler
def get_search_results(cursor, search_phrase):
    cursor.execute(
        """
        SELECT DISTINCT question.* FROM question
        LEFT JOIN answer ON question.id = answer.question_id
        WHERE question.title ILIKE %(srch_ph)s OR question.message ILIKE %(srch_ph)s OR answer.message ILIKE %(srch_ph)s
        """,
        {'srch_ph': '%{}%'.format(search_phrase)}
    )

    return cursor.fetchall()


# ----------------------------------------------------------------------------------------------------
# Tags


@connection.connection_handler
def get_all_tags(cursor):
    cursor.execute("SELECT name FROM tag")

    return cursor.fetchall()


@connection.connection_handler
def add_tag(cursor, tag_name):
    cursor.execute(f"INSERT INTO tag(name) VALUES('{tag_name}') WHERE '{tag_name}' NOT IN tag(name)")


@connection.connection_handler
def delete_tag_from_question(cursor, question_id, tag_id):
    cursor.execute(
        f"""
        DELETE FROM question_tag
        WHERE question_id = {question_id} AND tag_id = {tag_id}
        """
    )


@connection.connection_handler
def get_tag_id(cursor, tag_name):
    cursor.execute(f"SELECT id FROM tag WHERE name = '{tag_name}'")

    return cursor.fetchall()


@connection.connection_handler
def add_tag_to_question(cursor, question_id, tag_id):
    cursor.execute(
        f"""
        INSERT INTO question_tag(question_id, tag_id)
        VALUES('{question_id}', '{tag_id}')
        ON CONFLICT (tag_id, question_id) DO NOTHING
        """
    )


@connection.connection_handler
def add_custom_tag(cursor, tag_name):
    cursor.execute(f"SELECT name FROM tag WHERE name LIKE '{tag_name}'")
    found_tag = cursor.fetchall()

    if not found_tag:
        cursor.execute(
            f"""
            INSERT INTO tag(name)
            VALUES('{tag_name}')
            """)


@connection.connection_handler
def get_tags_for_question(cursor, question_id):
    cursor.execute(
        f"""
        SELECT tag.* FROM tag
        JOIN question_tag ON tag.id = question_tag.tag_id
        WHERE question_tag.question_id = {question_id};
        """)
    return cursor.fetchall()


def get_bonus_questions():
    bonus_questions_list = bonus_questions.SAMPLE_QUESTIONS
    return bonus_questions_list


# def filter_bonus_questions(filter_phrase=""):
#     bonus_questions_list = bonus_questions.SAMPLE_QUESTIONS
#     if filter_phrase:
#         bonus_questions_filtered_list = []
#         for que in bonus_questions_list:
#             if filter_phrase[0] == "!":
#                 try:
#                     if filter_phrase[1:filter_phrase.index(":")].lower() == "description":
#                         if filter_phrase[filter_phrase.index(":") + 1:] not in que["description"]:
#                             bonus_questions_filtered_list.append(que)
#                 except ValueError:
#                     if filter_phrase[1:] not in que["title"]:
#                         bonus_questions_filtered_list.append(que)
#             else:
#                 try:
#                     if filter_phrase[:filter_phrase.index(":")].lower() == "description":
#                         if filter_phrase[filter_phrase.index(":") + 1:] in que["description"]:
#                             bonus_questions_filtered_list.append(que)
#                 except ValueError:
#                     if filter_phrase in que["title"]:
#                         bonus_questions_filtered_list.append(que)
#         return bonus_questions_filtered_list
#     return bonus_questions_list
