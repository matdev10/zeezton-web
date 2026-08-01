document.addEventListener("DOMContentLoaded", () => {
  /* =========================================================
     ELEMENTOS DEL FORMULARIO
  ========================================================= */

  const typeSelect =
    document.getElementById("id_tipo_mensaje");

  const vehicleFields =
    document.getElementById("vehicleFields");

  const orderFields =
    document.getElementById("orderFields");

  const ratingFields =
    document.getElementById("ratingFields");

  const messageInput =
    document.getElementById("id_comentario");

  const messageHelp =
    document.getElementById("messageHelp");

  if (
    !typeSelect ||
    !vehicleFields ||
    !orderFields ||
    !ratingFields
  ) {
    return;
  }

  /* =========================================================
     CAMPOS INTERNOS DE CADA GRUPO
  ========================================================= */

  const vehicleInputs =
    vehicleFields.querySelectorAll(
      "input, select, textarea"
    );

  const orderInputs =
    orderFields.querySelectorAll(
      "input, select, textarea"
    );

  const ratingInputs =
    ratingFields.querySelectorAll(
      "input, select, textarea"
    );

  const vehicleInput =
    document.getElementById("id_vehiculo");

  const partInput =
    document.getElementById("id_repuesto");

  const orderInput =
    document.getElementById("id_numero_pedido");

  const ratingInput =
    document.getElementById("id_calificacion");

  /* =========================================================
     MOSTRAR U OCULTAR GRUPOS
  ========================================================= */

  const setGroupState = (
    group,
    inputs,
    visible
  ) => {
    group.hidden = !visible;

    inputs.forEach((input) => {
      input.disabled = !visible;
    });
  };

  /* =========================================================
     TEXTOS SEGÚN EL TIPO DE CONSULTA
  ========================================================= */

  const messageConfiguration = {
    IMPORTACION: {
      placeholder:
        "Indícanos qué repuesto necesitas y cualquier detalle adicional que pueda ayudarnos a encontrarlo.",
      help:
        "Incluye toda la información disponible sobre el vehículo y la pieza que necesitas.",
    },

    COMPATIBILIDAD: {
      placeholder:
        "Indícanos qué producto deseas revisar y cualquier duda sobre su compatibilidad.",
      help:
        "Incluye modelo, año, versión y producto consultado.",
    },

    PEDIDO: {
      placeholder:
        "Cuéntanos qué necesitas revisar respecto de tu compra o pedido.",
      help:
        "Incluye cualquier antecedente adicional relacionado con tu pedido.",
    },

    CALIFICACION: {
      placeholder:
        "Cuéntanos cómo fue tu experiencia y qué aspectos podríamos mejorar.",
      help:
        "Tu opinión nos ayuda a mejorar la atención y experiencia de compra.",
    },

    SUGERENCIA: {
      placeholder:
        "Comparte tu sugerencia o idea para ayudarnos a seguir mejorando.",
      help:
        "Cada comentario es revisado por el equipo Zeezton.",
    },

    OTRO: {
      placeholder:
        "Cuéntanos detalladamente cómo podemos ayudarte.",
      help:
        "Incluye toda la información que consideres importante.",
    },
  };

  /* =========================================================
     ACTUALIZAR FORMULARIO
  ========================================================= */

  const updateContactForm = () => {
    const selectedType = typeSelect.value;

    const showVehicleFields =
      selectedType === "IMPORTACION" ||
      selectedType === "COMPATIBILIDAD";

    const showOrderFields =
      selectedType === "PEDIDO";

    const showRatingFields =
      selectedType === "CALIFICACION";

    setGroupState(
      vehicleFields,
      vehicleInputs,
      showVehicleFields
    );

    setGroupState(
      orderFields,
      orderInputs,
      showOrderFields
    );

    setGroupState(
      ratingFields,
      ratingInputs,
      showRatingFields
    );

    /*
      Requisitos del navegador.
      El backend también valida estos campos.
    */
    if (vehicleInput) {
      vehicleInput.required =
        showVehicleFields;
    }

    if (partInput) {
      partInput.required =
        showVehicleFields;
    }

    if (orderInput) {
      orderInput.required =
        showOrderFields;
    }

    if (ratingInput) {
      ratingInput.required =
        showRatingFields;
    }

    /*
      Cambiar ayuda y placeholder
      según el tipo seleccionado.
    */
    const configuration =
      messageConfiguration[selectedType] ||
      messageConfiguration.OTRO;

    if (messageInput) {
      messageInput.placeholder =
        configuration.placeholder;
    }

    if (messageHelp) {
      messageHelp.textContent =
        configuration.help;
    }
  };

  /* =========================================================
     EVENTOS
  ========================================================= */

  typeSelect.addEventListener(
    "change",
    updateContactForm
  );

  /*
    Ejecutar al cargar la página.
    También conserva correctamente la selección
    cuando Django devuelve errores de validación.
  */
  updateContactForm();
});