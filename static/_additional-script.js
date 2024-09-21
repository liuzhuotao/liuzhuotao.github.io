function displayTopic() {
    var topicSection = document.getElementById("topic-section");
    var dateSection = document.getElementById("date-section");
    topicSection.style.display = "block";
    dateSection.style.display = "none";
}

function displayDate() {
    var topicSection = document.getElementById("topic-section");
    var dateSection = document.getElementById("date-section");
    topicSection.style.display = "none";
    dateSection.style.display = "block";
}