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

function changeFormula() {
    let donationFormula = document.getElementById("donation-formula")
    var solarPrice = document.getElementById("form-solar-price").value;
    let donationInput = document.getElementById("form-number-solar-panels");
    let answer = solarPrice * donationInput.value;
    donationFormula.innerText = `${solarPrice} * ${donationInput.value} = £${answer}`;
}

function prepareDonation(donateForm, userData) {
    var buttonContainers = document.getElementsByClassName('paypal-button-container');
    // Iterate over each container and render PayPal button
    var solarPrice = document.getElementById("form-solar-price").value;
    let donationInput = document.getElementById("form-number-solar-panels");
    let banner = "";
    for (var i = 0; i < buttonContainers.length; i++) {
        var orgaSlug = buttonContainers[i].getAttribute('data-orga-slug');
        var countryCode = buttonContainers[i].getAttribute('data-country-code');
        let sessionData = sessionStorage.getItem('user_id');
        paypal.Buttons({
            style: {
                width: '20%'
            },
            createOrder: function (data, actions) {
                var donationAmount = (donationInput.value * solarPrice);
                return actions.order.create({
                    intent: 'CAPTURE',
                    payer: {
                        name: {
                            given_name: userData["name"],
                            surname: ""
                        },
                        email_address: userData["email_username"],
                    },
                    purchase_units: [{
                        amount: {
                            value: donationAmount,
                            currency_code: "GBP"
                        }
                    }]
                });
            },
            // On successful capture, display a success message
            onApprove: function (data, actions) {
                let donationAmount = (donationInput.value * solarPrice);
                let xhr = new XMLHttpRequest();
                xhr.open("POST", "/api/donate", true);
                xhr.setRequestHeader("Content-Type", "application/json");
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === XMLHttpRequest.DONE) {
                        if (xhr.status === 200) {
                            console.log("Donation successful");
                        } else {
                            console.error("Donation failed:", xhr.responseText);
                        }
                    }
                };

                let requestData = JSON.stringify({
                    organization_slug: orgaSlug,
                    country_code: countryCode,
                    donation_amount: donationAmount,
                    orderID: data.orderID,
                });
                // Send the request
                xhr.send(requestData);

                // Display a success message to the user
                let bannerWrapper = document.createElement("div");
                bannerWrapper.classList.add("alert", "alert-success");
                bannerWrapper.role = "alert";
                bannerWrapper.innerText = "Thank you for your donation!";
                document.getElementById("popup-wrapper").firstElementChild.prepend(bannerWrapper);
                setTimeout(() => {
                    document.getElementById("popup-wrapper").innerHTML = "";
                }, 5000);
            }
        }).render(buttonContainers[i]);

    }
}

function donateButtonClicked(event) {
    let button = event.target;
    var userData = button.getAttribute("data-user");
    // Now you can access user data like userData.id, userData.user_type, etc.
    console.log(userData);
    let hrefDonateGet = button.getAttribute("ajaxref");
    if (hrefDonateGet) {
        let getRequest = new XMLHttpRequest();
        getRequest.open("GET", hrefDonateGet, true);
        getRequest.onload = (xhr) => {
            document.getElementById("popup-wrapper").innerHTML = xhr.target.responseText;
            let donateForm = document.getElementById("form-donate");
            prepareDonation(donateForm, userData);
        }
        getRequest.send();
    }
}

function donateMain() {
    // for each donation button, define the onclick event
    for (let button of document.getElementsByClassName("btn-orga-donate")) {
        button.addEventListener("click", donateButtonClicked);
    }
    //
    // // Define click event to make popup wrapper disappear
    document.getElementById("popup-wrapper").addEventListener("click", (event) => {
        if (event.target == document.getElementById("popup-wrapper")) {
            document.getElementById("popup-wrapper").innerHTML = "";
        }
    });


}

// Call main method when script is loaded
document.addEventListener("DOMContentLoaded", function () {
    donateMain();
});