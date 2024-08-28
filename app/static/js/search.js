const inputElement = document.getElementById("input_query");
inputElement.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    search();
  }
});

const buttonElement = document.getElementById("button_query");
buttonElement.addEventListener("click", (_) => {
  search();
});

async function search() {
  document.getElementById("div_query").classList.add("hidden");
  document.getElementById("loading").classList.remove("hidden");

  switchLoadingText(0);

  const body = await api();

  document.getElementById("div_query").classList.remove("hidden");
  document.getElementById("loading").classList.add("hidden");

  if (body === null) {
    document.getElementById("error").classList.remove("hidden");
  }

  window.location.href = window.location.origin + body.redirect;
}

loading_values = [
  "Collecting for the first time...",
  "Scraping from YouTube...",
  "Adding to database...",
  "Wrapping things up...",
];

async function switchLoadingText(iteration) {
  document.getElementById("loading_text").textContent =
    loading_values[iteration];

  if (iteration < loading_values.length) {
    setTimeout(function () {
      iteration++;
      switchLoadingText(iteration);
    }, 4000);
  } else {
    document.getElementById("loading_text").textContent = loading_values[3];
  }
}

async function api() {
  const response = await fetch(`/api/search/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      query: document.getElementById("input_query").value,
    }),
    redirect: "follow",
  });

  if (response.ok) {
    return await response.json();
  } else {
    return null;
  }
}
