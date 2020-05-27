/* Open when someone clicks on the span element */
function openNav() {

    document.getElementById("open").style.visibility = "hidden";
    document.getElementById("myNav").style.width = "10%";

}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("open").style.visibility = "visible";
    document.getElementById("myNav").style.width = "0%";
}

            async function checkdata(marked) {

                var marked_value = marked.value; // store the selected value marked_value

                console.log(marked_value); // do further processing with "marked_value" if needed
                const response = await fetch('/get_statistics_year/' + marked_value);
                console.log(response)
                const json = await response.json();

                console.log("response"+json);
                var ai = document.getElementById("ai_year");
                var cap = document.getElementById("cap_year");
                var dataset = document.getElementById("dataset_year");
                ai.innerHTML = json.ai;
                cap.innerHTML = json.cap;
                dataset.innerHTML = json.dataset;
            }