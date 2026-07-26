function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseElement = document.getElementById("system_response");
    const request = new XMLHttpRequest();

    request.onreadystatechange = function handleResponse() {
        if (this.readyState === 4 && this.status === 200) {
            responseElement.innerHTML = request.responseText;

            if (request.responseText.startsWith("Invalid text!")) {
                responseElement.className = "error";
            } else {
                responseElement.className = "success";
            }
        }
    };

    request.open(
        "GET",
        `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`,
        true
    );
    request.send();
}
