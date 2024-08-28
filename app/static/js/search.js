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

  let body = await response.json();

  document.getElementById("div_query").classList.remove("hidden");
  document.getElementById("loading").classList.add("hidden");

  window.location.href = window.location.origin + body.redirect;
}
