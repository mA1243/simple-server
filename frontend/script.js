function fetchWeather(event) {
    event.preventDefault();
    
    var city = document.getElementById("city").value.trim();
    if (!city) {
        alert("Please enter a city name.");
        return;
    }
    var unit = document.querySelector('input[name="unitRadios"]:checked')?.value || "metric";

    document.getElementById("weather_container").style.display = "none";
    document.getElementById("location").innerHTML = "";
    document.getElementById("cur_temp").innerHTML = "";
    document.getElementById("like_temp").innerHTML = "";
    document.getElementById("mm_temp").innerHTML = "";
    document.getElementById("ai_summary").innerHTML = ""
    document.getElementById("icon").style.display = "none";

    document.getElementById("loader").style.display = "block";
    

    fetch("https://hello-world-8qw7.onrender.com//api/v1/weather?city=" + city + "&unit=" + unit) 
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            unitval = unit == "metric" ? "°C" : "F"
            values = data.temperature;
            document.getElementById("location").innerHTML = values.city + ", " + values.country;
            document.getElementById("cur_temp").innerHTML = "Current temperature: " + values.current_temp + unitval;
            document.getElementById("like_temp").innerHTML = "Feels Like: " + values.feels_like + unitval;
            document.getElementById("mm_temp").innerHTML = "Max: " + values.max_temp + unitval + ", Min: " + values.min_temp + unitval
            document.getElementById("ai_summary").innerHTML = values.ai_summary
            document.querySelector("img").src = values.icon;
            
            const weatherIcon = document.querySelector("img");
            weatherIcon.src = values.icon;
            weatherIcon.onload = () => {
                document.getElementById("icon").style.display = "block";
                document.getElementById("loader").style.display = "none";
                document.getElementById("weather_container").style.display = "block";
            };
        })
        .catch(error => {
            console.log('There was a problem with the fetch operation:', error);
            document.getElementById("location").innerHTML = "City Not Found";
            document.getElementById("loader").style.display = "none";
            document.getElementById("weather_container").style.display = "block";
        });
}