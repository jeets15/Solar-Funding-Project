
/* TEMPLATE REQUIREMENTS

-- Use the donate.css style sheet
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/donate.css') }}">
{% endblock %}

-- Div high up the dom that will display pop ups
<div id="popup-wrapper"></div>

-- Button that will load the popup
<button
    class="btn-orga-donate btn btn-outline-primary"
    ajaxref="{{ url_for('api.donate', country=country.country_code, orga=orga.name_slug) }}">
    Donate Now
</button>

-- Load this javascript code file
{% block scripts %}
<script src="{{ url_for('static', filename='js/donate.js') }}" defer></script>
{% endblock %}
*/


function prepareDonation(donateForm) {
    donateForm.addEventListener("submit", (event) => {
        event.preventDefault();
        if (document.getElementById("flash-banner")) {
            document.getElementById("flash-banner").innerHTML = "";
        }
        let submitButton = document.getElementById("form-donate-submit");
        if (submitButton) {
            submitButton.type = "hidden"
        }
        let donationInput = document.getElementById("form-donation-amount");
        if (donationInput) {
            donationInput.readOnly = true;
            // donationInput.setAttribute('readonly', true);
        }
        let xhr = new XMLHttpRequest();
        xhr.open("POST", donateForm.action, true);
        xhr.onload = () => {
            let banner = "";
            if (xhr.status === 200) {
                banner = `<div class="alert alert-success" role="alert">
                            Thank you for your Donating!</div>`;
            } else {
                banner = `<div class="alert alert-danger" role="alert" style="text-align: center;">
                            Oh no! We couldn't Process your Donation!<br>Reason: ${xhr.responseText}</div>`;
            }
            let bannerWrapper = document.createElement("div");
            bannerWrapper.id = "flash-banner";
            bannerWrapper.innerHTML = banner;
            document.getElementById("popup-wrapper").firstElementChild.prepend(bannerWrapper);
            setTimeout(() => {
                document.getElementById("popup-wrapper").innerHTML = "";
            }, 5000);
        };
        xhr.send(new FormData(donateForm));
    });
}

function donateButtonClicked(event) {
    let button = event.target;

    let hrefDonateGet = button.getAttribute("ajaxref");
    if (hrefDonateGet) {
        let getRequest = new XMLHttpRequest();
        getRequest.open("GET", hrefDonateGet, true);
        getRequest.onload = (xhr) => {
            document.getElementById("popup-wrapper").innerHTML = xhr.target.responseText;
            let donateForm = document.getElementById("form-donate");
            prepareDonation(donateForm);
        }
        getRequest.send();
    }
}

function donateMain() {
    // for each donation button, define the onclick event
    for (let button of document.getElementsByClassName("btn-orga-donate")) {
        button.addEventListener("click", donateButtonClicked);
    }

    // Define click event to make popup wrapper disappear
    document.getElementById("popup-wrapper").addEventListener("click", (event) => {
        if (event.target == document.getElementById("popup-wrapper")) {
            document.getElementById("popup-wrapper").innerHTML = "";
        }
    });
}

// Call main method when script is loaded
donateMain();