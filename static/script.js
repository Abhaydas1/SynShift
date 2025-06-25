function translateCode() {
    const sourceLang = document.getElementById("source_lang").value;
    const targetLang = document.getElementById("target_lang").value;
    const inputCode = document.getElementById("input_code").value;

    if (!inputCode) {
        alert("Please enter code to translate.");
        return;
    }

    fetch("/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            source_lang: sourceLang,
            target_lang: targetLang,
            code: inputCode
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output_code").value = data.translated_code;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while translating the code.");
    });
}
