const m3MoreBtn = document.getElementById("m3MoreBtn");
const m3Extra = document.getElementById("m3Extra");

if (m3MoreBtn && m3Extra) {

    m3MoreBtn.addEventListener("click", () => {

        m3Extra.classList.toggle("active");

        m3MoreBtn.textContent =
            m3Extra.classList.contains("active")
            ? "Ver menos"
            : "Saber más";

    });

}