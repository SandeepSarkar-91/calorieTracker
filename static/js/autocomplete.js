document.addEventListener("DOMContentLoaded", () => {
    function setupAutocomplete(inputId, type) {
        const input = document.getElementById(inputId);
        input.addEventListener("input", async () => {
            const q = input.value;
            const res = await fetch(`/autocomplete/${type}?q=${q}`);
            const suggestions = await res.json();

            const datalistId = `${inputId}-list`;
            let datalist = document.getElementById(datalistId);
            if (!datalist) {
                datalist = document.createElement("datalist");
                datalist.id = datalistId;
                input.setAttribute("list", datalistId);
                document.body.appendChild(datalist);
            }

            datalist.innerHTML = "";
            suggestions.forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                datalist.appendChild(opt);
            });
        });
    }

    if (document.getElementById("food_name")) setupAutocomplete("food_name", "food");
    if (document.getElementById("workout_name")) setupAutocomplete("workout_name", "workout");
});
