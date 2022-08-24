ALTER TABLE IF EXISTS ONLY public.answer
DROP CONSTRAINT IF EXISTS fk_question_id,
ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS ONLY public.comment
DROP CONSTRAINT IF EXISTS fk_question_id,
ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS ONLY public.comment
DROP CONSTRAINT IF EXISTS fk_answer_id,
ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS ONLY public.question_tag
DROP CONSTRAINT IF EXISTS fk_question_id,
ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE IF EXISTS ONLY public.question_tag
DROP CONSTRAINT IF EXISTS fk_tag_id,
ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE;


ALTER TABLE IF EXISTS ONLY users DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;

ALTER TABLE IF EXISTS ONLY users_questions DROP CONSTRAINT IF EXISTS pk_user_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY users_questions DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY users_questions DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;

ALTER TABLE IF EXISTS ONLY users_answers DROP CONSTRAINT IF EXISTS pk_user_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY users_answers DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY users_answers DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;

ALTER TABLE IF EXISTS ONLY users_comments DROP CONSTRAINT IF EXISTS pk_user_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY users_comments DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY users_comments DROP CONSTRAINT IF EXISTS fk_comment_id CASCADE;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS users_questions;
DROP TABLE IF EXISTS users_answers;
DROP TABLE IF EXISTS users_comments;

CREATE TABLE IF NOT EXISTS users (
    id serial NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    num_of_questions INTEGER DEFAULT 0,
    num_of_answers INTEGER DEFAULT 0,
    num_of_comments INTEGER DEFAULT 0,
    reputation INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users_questions (
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users_answers (
    user_id INTEGER NOT NULL,
    answer_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users_comments (
    user_id INTEGER NOT NULL,
    comment_id INTEGER NOT NULL
);

ALTER TABLE users
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE users_questions
    ADD CONSTRAINT pk_user_question_id PRIMARY KEY (user_id, question_id);

ALTER TABLE users_questions
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE users_questions
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE users_answers
    ADD CONSTRAINT pk_user_answer_id PRIMARY KEY (user_id, answer_id);

ALTER TABLE users_answers
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE users_answers
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id) ON DELETE CASCADE;

ALTER TABLE users_comments
    ADD CONSTRAINT pk_user_comment_id PRIMARY KEY (user_id, comment_id);

ALTER TABLE users_comments
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE users_comments
    ADD CONSTRAINT fk_comment_id FOREIGN KEY (comment_id) REFERENCES comment(id) ON DELETE CASCADE;