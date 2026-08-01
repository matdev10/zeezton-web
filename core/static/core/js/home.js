document.addEventListener("DOMContentLoaded", () => {
  /* =========================================================
     CARRUSEL PRINCIPAL
  ========================================================= */

  const carouselElement = document.getElementById(
    "carouselHomeZeezton"
  );

  if (
    carouselElement &&
    typeof bootstrap !== "undefined"
  ) {
    const desktopMedia = window.matchMedia(
      "(min-width: 1025px)"
    );

    const carouselItems =
      carouselElement.querySelectorAll(
        ".carousel-item"
      );

    const carouselIndicators =
      carouselElement.querySelectorAll(
        ".carousel-indicators button"
      );

    const showFirstSlide = () => {
      carouselItems.forEach((item, index) => {
        item.classList.toggle(
          "active",
          index === 0
        );
      });

      carouselIndicators.forEach(
        (indicator, index) => {
          indicator.classList.toggle(
            "active",
            index === 0
          );

          if (index === 0) {
            indicator.setAttribute(
              "aria-current",
              "true"
            );
          } else {
            indicator.removeAttribute(
              "aria-current"
            );
          }
        }
      );
    };

    const updateHomeCarousel = () => {
      const currentInstance =
        bootstrap.Carousel.getInstance(
          carouselElement
        );

      /*
        ESCRITORIO:
        activar el carrusel automático.
      */
      if (desktopMedia.matches) {
        const carousel =
          currentInstance ||
          new bootstrap.Carousel(
            carouselElement,
            {
              interval: 3500,
              ride: "carousel",
              pause: false,
              wrap: true,
              touch: true,
            }
          );

        carousel.cycle();
        return;
      }

      /*
        TABLET Y MÓVIL:
        detener el carrusel y mostrar
        siempre la primera imagen.
      */
      if (currentInstance) {
        currentInstance.pause();
        currentInstance.dispose();
      }

      showFirstSlide();
    };

    updateHomeCarousel();

    desktopMedia.addEventListener(
      "change",
      updateHomeCarousel
    );
  }

  /* =========================================================
     NOTICIA BMW M3
  ========================================================= */

  const m3MoreBtn =
    document.getElementById("m3MoreBtn");

  const m3LessBtn =
    document.getElementById("m3LessBtn");

  const m3MoreWrap =
    document.getElementById("m3MoreWrap");

  const m3LessWrap =
    document.getElementById("m3LessWrap");

  const m3Extra =
    document.getElementById("m3Extra");

  const homeM3 =
    document.querySelector(".home-m3");

  if (
    m3MoreBtn &&
    m3LessBtn &&
    m3MoreWrap &&
    m3LessWrap &&
    m3Extra
  ) {
    const setM3Expanded = (expanded) => {
      m3Extra.classList.toggle(
        "active",
        expanded
      );

      m3Extra.setAttribute(
        "aria-hidden",
        String(!expanded)
      );

      m3MoreBtn.setAttribute(
        "aria-expanded",
        String(expanded)
      );

      /*
        Al abrir:
        - ocultar Saber más
        - mostrar Saber menos

        Al cerrar:
        - mostrar Saber más
        - ocultar Saber menos
      */
      m3MoreWrap.hidden = expanded;
      m3LessWrap.hidden = !expanded;
    };

    m3MoreBtn.addEventListener(
      "click",
      () => {
        setM3Expanded(true);
      }
    );

    m3LessBtn.addEventListener(
      "click",
      () => {
        setM3Expanded(false);

        homeM3?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    );

    /*
      Estado inicial:
      noticia cerrada y Saber más visible.
    */
    setM3Expanded(false);
  }
});