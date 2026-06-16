document.addEventListener("DOMContentLoaded", () => {
  const weatherBox = document.getElementById("navWeather");

  if (!weatherBox) return;

  if (!navigator.geolocation) {
    weatherBox.style.display = "none";
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      const response = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,is_day&timezone=auto`
      );

      const data = await response.json();
      const temp = Math.round(data.current.temperature_2m);
      const icon = data.current.is_day ? "fa-sun" : "fa-moon";

      weatherBox.innerHTML = `
  <span>${temp}°</span>
  <i class="fa-solid ${icon}"></i>
`;
    },
    () => {
      weatherBox.style.display = "none";
    }
  );
});