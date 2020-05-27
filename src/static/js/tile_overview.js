//get statistics from selected year
async function checkdata(marked) {

    var marked_value = marked.value; // store the selected year

    const response = await fetch('/get_statistics_year/' + marked_value);
    const json = await response.json();

    var ai = document.getElementById("ai_year");
    var cap = document.getElementById("cap_year");
    var dataset = document.getElementById("dataset_year");

    ai.innerHTML = json.ai;
    cap.innerHTML = json.cap;
    dataset.innerHTML = json.dataset;
}