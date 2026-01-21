const tbody = document.querySelector("#recipeTable tbody");
const drawer = document.getElementById("drawer");

fetch("/api/recipes?page=1&limit=15")
  .then(res => res.json())
  .then(data => {
    if (data.data.length === 0) {
      tbody.innerHTML = "<tr><td colspan='5'>No Data Found</td></tr>";
      return;
    }

    data.data.forEach(r => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="truncate">${r.title}</td>
        <td>${r.cuisine}</td>
        <td>${stars(r.rating)}</td>
        <td>${r.total_time}</td>
        <td>${r.serves}</td>
      `;
      tr.onclick = () => openDrawer(r);
      tbody.appendChild(tr);
    });
  });

function stars(rating) {
  return `<span class="star">${"★".repeat(Math.round(rating))}</span>`;
}

function openDrawer(r) {
  document.getElementById("drawerTitle").innerText = r.title;
  document.getElementById("drawerCuisine").innerText = r.cuisine;
  document.getElementById("drawerDesc").innerText = r.description;
  document.getElementById("drawerTotal").innerText = r.total_time;
  document.getElementById("drawerCook").innerText = r.cook_time;
  document.getElementById("drawerPrep").innerText = r.prep_time;

  const nutrition = document.getElementById("nutritionBody");
  nutrition.innerHTML = "";

  ["calories","carbohydrateContent","cholesterolContent","fiberContent","proteinContent"]
    .forEach(key => {
      nutrition.innerHTML += `
        <tr>
          <td><strong>${key}</strong></td>
          <td>${r.nutrients[key] || "-"}</td>
        </tr>
      `;
    });

  drawer.classList.add("open");
}

function closeDrawer() {
  drawer.classList.remove("open");
}

function toggleTime() {
  document.getElementById("timeDetails").classList.toggle("hidden");
}
