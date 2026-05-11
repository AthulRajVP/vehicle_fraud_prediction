const form = document.getElementById('prediction-form');
const resultDiv = document.querySelector('.result');
const apiUrl = 'http://127.0.0.1:8000/predict';

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    resultDiv.textContent = 'Predicting...';

    const payload = {
        Age: Number(document.getElementById('age').value),
        Gender: document.getElementById('gender').value.trim(),
        Policy_Type: document.getElementById('policy_type').value.trim(),
        Vehicle_Type: document.getElementById('vehicle_type').value.trim(),
        Accident_Type: document.getElementById('accident_type').value.trim(),
        Annual_Premium: Number(document.getElementById('annual_premium').value),
        Claim_Amount: Number(document.getElementById('claim_amount').value),
        Police_Report: document.getElementById('police_report').value.trim(),
        Witness_Present: document.getElementById('witnesses').value.trim(),
        Past_Claims: Number(document.getElementById('past_claims').value),
        Days_To_Claim: Number(document.getElementById('days_to_claim').value),
        Incident_Location: document.getElementById('incident_location').value.trim(),
    };

    console.log('Prediction payload:', payload);

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        const text = await response.text();
        console.log('Raw response text:', text);

        let data;
        try {
            data = JSON.parse(text);
        } catch (jsonError) {
            throw new Error(`Server did not return valid JSON: ${jsonError.message}`);
        }

        if (!response.ok) {
            resultDiv.textContent = data.error || 'Prediction failed. Check server logs.';
            return;
        }

        resultDiv.textContent = data.prediction || 'No prediction returned.';
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    }
});
