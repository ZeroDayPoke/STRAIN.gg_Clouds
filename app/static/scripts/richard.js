document.addEventListener("DOMContentLoaded", () => {
  
  getReviewsBtn.addEventListener("click", async () => {
    await getStrains();
  });

  // Fetch reviews data from the API
  async function getStrains() {
    try {
      const response = await fetch("clouds/strains");
      const strains = await response.json();
      displayStrains(strains);
    } catch (error) {
      console.error("Error fetching strains:", error);
    }
  }

  // Display reviews on the page
  function displayStrains(strains) {
    renderStrains(strains);
  }

  function renderStrains(strains) {
    const strainsContainer = document.querySelector('.strains');
    strainsContainer.innerHTML = '';
  
    if (strains.length === 0) {
      strainsContainer.innerHTML = '<p>No strains found.</p>';
      return;
    }
  
    strains.forEach(strain => {
      const strainCard = `
        <div class="card mb-3" data-id="${strain.id}">
          <div class="card-body">
            <h5 class="card-title">Strain ID: ${strain.id}</h5>
            <p class="card-text">
              <strong>Name:</strong> ${strain.name}<br>
              <strong>Concentration:</strong> ${strain.delta_nine_concentration}<br>
              <strong>Target:</strong> ${strain.target_symptom}<br>
            </p>
            <button class="btn btn-primary updateReview" data-review-id="${strain.id}" data-bs-toggle="modal" data-bs-target="#updateReviewModal">Update</button>
            <button class="btn btn-danger deleteReview" data-review-id="${strain.id}" data-bs-toggle="modal" data-bs-target="#deleteReviewModal">Delete</button>
          </div>
        </div>
      `;
      strainsContainer.innerHTML += strainCard;
    });
  
    addUpdateDeleteListeners();
  }
});
