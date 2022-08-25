let filter_phrase = document.querySelector('#filter_text');
let button = document.querySelector('#filter_button');
let font_size_up = document.querySelector('#font_size_up');
let font_size_down = document.querySelector('#font_size_down');
button.addEventListener("click", search);
filter_phrase.addEventListener("keyup", search);
font_size_up.addEventListener("click", change_font_size);
font_size_down.addEventListener("click", change_font_size);


let sort_order = {
    "title": true,
    "description": true,
    "view_number": true,
    "vote_number": true
};

search(null);

let table = document.querySelector('.bonus_que');
table.style.fontSize = "16px";

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
    build_questions_html(filtered_questions);

    return filtered_questions;
}


function sort(key) {
    let sort_by = key.target.sort_by;
    let f_questions = search();


    function GetSortOrder(prop) {
        return (a, b) => {
            if (a[prop] > b[prop]) return sort_order[prop] ? 1 : -1;
            if (a[prop] < b[prop]) return sort_order[prop] ? -1 : 1;
            return 0;
        }
    }
    f_questions.sort(GetSortOrder(sort_by));
    sort_order[sort_by] = !sort_order[sort_by];
    build_questions_html(f_questions);
}

function build_questions_html(questions) {
    let questions_html = "";
    let questions_container = document.querySelector('#questions_div');
    questions_html += "<table class='bonus_que'>";
    questions_html += "<tr>";
    questions_html += "<th class='bonus_que_header'><a href='#' id='title'>Title</a></th>" +
                      "<th class='bonus_que_header'><a href='#' id='description'>Description</a></th>" +
                      "<th class='bonus_que_header'><a href='#' id='view_number'>View number</a></th>" +
                      "<th class='bonus_que_header'><a href='#' id='vote_number'>Vote number</a></th>";
    questions_html += "</tr>";
        for (let que of questions) {
            questions_html += "<tr>";
            questions_html += "<td class='bonus_que_title'>" + que.title + "</td>" +
                              "<td class='bonus_que_desc'>" + que.description + "</td>" +
                              "<td class='bonus_que_views'>" + que.view_number + "</td>" +
                              "<td class='bonus_que_votes'>" + que.vote_number + "</td>";
            questions_html += "</tr>";
        }
    questions_html += "</table>";
    questions_container.innerHTML = questions_html;

    let title_sort = document.querySelector('#title');
    title_sort.addEventListener("click", sort);
    title_sort.sort_by = "title";
    let description_sort = document.querySelector('#description');
    description_sort.addEventListener("click", sort);
    description_sort.sort_by = "description";
    let view_number_sort = document.querySelector('#view_number');
    view_number_sort.addEventListener("click", sort);
    view_number_sort.sort_by = "view_number";
    let vote_number_sort = document.querySelector('#vote_number');
    vote_number_sort.addEventListener("click", sort);
    vote_number_sort.sort_by = "vote_number";
}


function change_font_size(key) {
    let font_size_direction = key.target.id;
    let table_font_size = +table.style.fontSize.substring(0,table.style.fontSize.length - 2);
    if (font_size_direction === "font_size_up" && table_font_size < 25) {
        table.style.fontSize = table_font_size + 1 + "px";
    }
    if (font_size_direction === "font_size_down" && table_font_size > 10) {
        table.style.fontSize = table_font_size - 1 + "px";
    }
}