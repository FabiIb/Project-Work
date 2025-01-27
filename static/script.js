// Esegue la funzione al caricamento della schermata
document.addEventListener("DOMContentLoaded", () => {
  setDateConstraints();
  document.querySelector("form").addEventListener("submit", function (e) {
    if (!validateTime()) {
      e.preventDefault();
    }
  });
});

// Mostra il form di prenotazione quando si clicca sul bottone "Prenota Ora"
document.getElementById("book-button").addEventListener("click", function () {
  const formContainer = document.getElementById("reservation-form-container");
  formContainer.style.display = "block";
  this.style.display = "none";
});

document
  .getElementById("reservation-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    // Recupero i valori dal form
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const date = document.getElementById("date").value;
    const time = document.getElementById("time").value;
    const number = document.getElementById("number").value;
    const location = document.getElementById("location").value;

    const reservationData = {
      name,
      email,
      date,
      time,
      number,
      location,
    };

    // Invio dati al BE
    fetch("/prenotazione", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(reservationData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("res:", data);
        document.getElementById("response-message").textContent = data.message;
      })
      .catch((error) => {
        console.warn("Error:", error);
        document.getElementById("response-message").textContent =
          "Si è verificato un errore. Riprova.";
      });
  });

// Funzione per calcolare la data corrente
function getTodayDate() {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const dd = String(today.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

// Funzione per calcolare la data 3 anni da oggi
function getFutureDate() {
  const today = new Date();
  today.setFullYear(today.getFullYear() + 3);
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const dd = String(today.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

// Funzione per impostare i limiti di data per il campo date
function setDateConstraints() {
  document.getElementById("date").setAttribute("min", getTodayDate()); // Min giorno corrente
  document.getElementById("date").setAttribute("max", getFutureDate()); // Max 3 anni in avanti
}

// Validazione Orario
function validateTime() {
  const timeInput = document.getElementById("time").value;
  const dateInput = document.getElementById("date").value; // Data selezionata

  // Orari di apertura, con possibilità di prenotare massimo mezz'ora prima della chiusura
  const lunchStart = "12:00";
  const lunchEnd = "14:00";
  const dinnerStart = "19:00";
  const dinnerEnd = "22:00";

  // Combina data e ora in un oggetto Date e ne crea un altro con data corrente
  const selectedDateTime = new Date(dateInput + "T" + timeInput);
  const currentDateTime = new Date();

  // Controllo validità dell'ora
  if (selectedDateTime < currentDateTime) {
    // L'ora inserita è già superata
    alert(
      "La data e l'ora selezionata sono già passate. Per favore, scegli una data futura."
    );
    return false;
  } else if (
    (timeInput >= lunchStart && timeInput <= lunchEnd) ||
    (timeInput >= dinnerStart && timeInput <= dinnerEnd)
  ) {
    // L'ora inserita non è stata superata e rientra nel range
    return true;
  } else {
    // L'ora inserita non è stata superata, ma non rientra nel range
    alert(
      "L'orario selezionato non è valido. Scegli un orario tra 12:00-14:00 o 19:00-22:00."
    );
    return false;
  }
}
