// Carbon Emission Calculator

// User Interface
const rangeInput = document.getElementById('donation-amount-range');
const displayDiv = document.getElementById('donation-amount');
const reducedCO2InKg = document.getElementById('weight');

// Event Listeners
rangeInput.addEventListener('input', function () {
    displayDiv.textContent = '£' + this.value;
    reducedCO2InKg.textContent = calculateReducedCarbonFootprint(this.value);
});


// Helper Methods

// Solar Energy Offset Calculations
function calculateReducedCarbonFootprint(donationAmount) {
    // Placeholder for average CO2 offset per dollar donated
    const averageCO2OffsetPerDollar = 0.1; // kg CO2 equivalent per dollar (modify based on your data)

    // Calculate the CO2 offset in kilograms
    const co2OffsetKg = donationAmount * averageCO2OffsetPerDollar;

    // Convert CO2 offset to metric tons (optional)
    const co2OffsetTonnes = co2OffsetKg / 1000;

    // Return the CO2 offset value
    return co2OffsetKg.toFixed(2) + " kg CO2 equivalent" +
        (co2OffsetTonnes ? " (" + co2OffsetTonnes.toFixed(2) + " metric tons)" : "");
}
