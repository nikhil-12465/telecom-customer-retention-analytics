
// AUTO TOTAL CHARGES

function updateTotalCharges() {

    const monthlyCharges =
        parseFloat(
            document.getElementById("monthlyCharges").value
        ) || 0;

    const tenure =
        parseInt(
            document.getElementById("tenure").value
        ) || 0;

    const totalCharges =
        (monthlyCharges * tenure).toFixed(2);

    document.getElementById("totalCharges").value =
        totalCharges;
}

// EVENT LISTENERS

document.addEventListener("DOMContentLoaded", function () {

    const monthlyInput =
        document.getElementById("monthlyCharges");

    const tenureInput =
        document.getElementById("tenure");

    if (monthlyInput) {
        monthlyInput.addEventListener(
            "input",
            updateTotalCharges
        );
    }

    if (tenureInput) {
        tenureInput.addEventListener(
            "input",
            updateTotalCharges
        );
    }

    updateTotalCharges();


    // LOADING SPINNER


    const form =
        document.getElementById("predictionForm");

    const loading =
        document.getElementById("loading");

    const button =
        document.getElementById("predictBtn");

    if (form) {

        form.addEventListener("submit", function () {

            updateTotalCharges();

            loading.style.display = "block";

            button.disabled = true;

            button.innerHTML =
                "Analyzing...";
        });
    }
});

