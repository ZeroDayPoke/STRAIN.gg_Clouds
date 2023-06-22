document.addEventListener("DOMContentLoaded", (event) => {
  const updateButtons = document.querySelectorAll(".update-btn");

  updateButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      const id = event.target.getAttribute("data-id");
      const name = event.target.getAttribute("data-name");
      const location = event.target.getAttribute("data-location");
      const operatingHours = event.target.getAttribute("data-operating-hours");

      const form = document.querySelector("#updateStoreForm");
      form.action = `/stores/update_store`;
      form.querySelector('input[name="id"]').value = id;
      form.querySelector('input[name="name"]').value = name;
      form.querySelector('input[name="location"]').value = location;
      form.querySelector('input[name="operating_hours"]').value =
        operatingHours;
      const relatedStrains = event.target
        .getAttribute("data-related-strains")
        .split(",");
      console.log("Related strains:", relatedStrains);
      debugger;
      const strainsSelect = form.querySelector(
        'select[name="related_strains"]'
      );
      for (let option of strainsSelect.options) {
        if (relatedStrains.includes(option.value)) {
          option.selected = true;
        } else {
          option.selected = false;
        }
      }
    });
  });
});
