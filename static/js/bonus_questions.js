let filter_phrase = document.querySelector('#filter_text');
let button = document.querySelector('#filter_button');
button.addEventListener("click", search);
filter_phrase.addEventListener("keyup", search);

search(null);

function search(key) {
    if (key != null){
        if (key.type === "keyup"){
            if (key.key !== "Enter") return;
        }
        else if (key.type !== "click") return;
    }
    let filtered_questions = [];
    let filter_text = filter_phrase.value.toLowerCase();

    if (filter_text !== "") {
        for (let que of bonus_questions) {
            if (filter_text[0] === "!") {
                if (filter_text.indexOf("description:", 1) === 1) {
                    if (!que.description.toLowerCase().includes(filter_text.substring(filter_text.indexOf(":") + 1))) {
                        filtered_questions.push(que);
                    }
                }
                else {
                    if (!que.title.toLowerCase().includes(filter_text.substring(1))) {
                        filtered_questions.push(que);
                    }
                }
            }
            else {
                if (filter_text.indexOf("description:") === 0) {
                    if (que.description.toLowerCase().includes(filter_text.substring(filter_text.indexOf(":") + 1))) {
                        filtered_questions.push(que);
                    }
                }
                else {
                    if (que.title.toLowerCase().includes(filter_text)) {
                        filtered_questions.push(que);
                    }
                }
            }
        }
    }
    else {
        filtered_questions = [...bonus_questions];
    }

    let questions_html = "";
    let questions_container = document.querySelector('#questions_div');
    questions_html += "<table class='bonus_que'>";
    questions_html += "<tr>";
    questions_html += "<th class='bonus_que_header'>Title</th>" +
                      "<th class='bonus_que_header'>Description</th>" +
                      "<th class='bonus_que_header'>View number</th>" +
                      "<th class='bonus_que_header'>Vote number</th>";
    questions_html += "</tr>";
        for (let que of filtered_questions) {
            questions_html += "<tr>";
            questions_html += "<td class='bonus_que_title'>" + que.title + "</td>" +
                              "<td class='bonus_que_desc'>" + que.description + "</td>" +
                              "<td class='bonus_que_views'>" + que.view_number + "</td>" +
                              "<td class='bonus_que_votes'>" + que.vote_number + "</td>";
            questions_html += "</tr>";
        }
    questions_html += "</table>";

    questions_container.innerHTML = questions_html;
}
