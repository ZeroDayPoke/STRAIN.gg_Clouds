let strainsData = [];

// Function to fetch strains from the API
async function fetchStrains() {
  try {
    const response = await fetch('/clouds/api/v1/strains');
    const data = await response.json();
    strainsData = data;
    renderStrains();
  } catch (error) {
    console.error('Error fetching strains:', error);
  }
}

// Function to render the strains list in DOM
function renderStrains(strainsToRender = strainsData) {
  const strainsContainer = document.querySelector('#strainsContainer');
  strainsContainer.innerHTML = '<div class="row"></div>';

  let currentRow = strainsContainer.querySelector(".row");

  strainsToRender.forEach((strain, index) => {
    const isCloudProducer = userRole === userRoles.CLOUD_PRODUCER;
    const isCloudChaser = userRole === userRoles.CLOUD_CHASER;
    const isCloudVendor = userRole === userRoles.CLOUD_VENDOR;
    const isCloudConsumer = userRole === userRoles.CLOUD_CONSUMER;
    const editDeleteButtonsHTML = (isCloudProducer || isCloudChaser || isCloudVendor) ? `
      <button class="btn btn-sm btn-warning" onclick="openUpdateStrainModal('${strain.id}')">Edit</button>
      <button class="btn btn-sm btn-danger" onclick="openDeleteStrainModal('${strain.id}')">Delete</button>
    ` : '';
    const addFavoritesButtonHTML = (isCloudChaser || isCloudConsumer || isCloudProducer || isCloudVendor) ? `
      <button class="btn btn-sm btn-success" onclick="addToFavorites('${strain.id}')">Save to Favorites</button>
    ` : `
      <a href="${signInUrl}" class="btn btn-primary">Sign In to use Favorites</a>
    `;

    const strainCard = `
    <div class="col-md-6 mb-4">
      <div class="strain-card">
        <div class="row">
          <div class="col-md-6">
            <img src="/static/images/strain_images/${strain.image_filename}" alt="${strain.name}" class="strain-image">
            <div class="strain-concentrations">
              <p>Delta-9 Concentration: ${strain.delta_nine_concentration}</p>
              <p>CBD Concentration: ${strain.cbd_concentration}</p>
            </div>
            <div class="strain-card-buttons">
              ${editDeleteButtonsHTML}
              ${addFavoritesButtonHTML}
            </div>
          </div>
          <div class="col-md-6">
            <h3>${strain.name}</h3>
            <h4>${strain.id}</h4>
            <p>Type: ${strain.type}</p>
            <p>Terpene Profile: ${strain.terpene_profile}</p>
            <p>Effects: ${strain.effects}</p>
            <p>Uses: ${strain.uses}</p>
            <p>Flavor: ${strain.flavor}</p>
          </div>
        </div>
      </div>
    </div>`;

    currentRow.innerHTML += strainCard;

    // Create a new row for every two strain cards
    if (index % 2 === 1) {
      const newRow = document.createElement("div");
      newRow.className = "row";
      strainsContainer.appendChild(newRow);
      currentRow = newRow;
    }
  });
}

// Function to add the strain to the user's favorites
async function addToFavorites(strainId) {
  try {
    const response = await fetch(`/clouds/api/v1/strains/favorite_strains/${strainId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (data.success) {
      alert('Strain added to favorites successfully');
    } else {
      alert('Error adding strain to favorites: ' + data.message);
    }
  } catch (error) {
    console.error('Error adding strain to favorites:', error);
  }
}

// Function to handle the CREATE form submission
async function submitCreateStrain(event) {
  event.preventDefault();

  // Create a FormData object to handle the image upload
  let formData = new FormData();

  // Retrieve the form inputs
  let name = $("#name").val();
  let type = $("#type").val();
  let delta_nine_concentration = $("#delta_nine_concentration").val();
  let cbd_concentration = $("#cbd_concentration").val();
  let terpene_profile = $("#terpene_profile").val();
  let effects = $("#effects").val();
  let uses = $("#uses").val();
  let flavor = $("#flavor").val();
  let image = $("#image").get(0).files[0];

  // Append the form inputs to the FormData object
  formData.append("name", name);
  formData.append("type", type);
  formData.append("delta_nine_concentration", delta_nine_concentration);
  formData.append("cbd_concentration", cbd_concentration);
  formData.append("terpene_profile", terpene_profile);
  formData.append("effects", effects);
  formData.append("uses", uses);
  formData.append("flavor", flavor);
  formData.append("image", image);

  try {
    // Send the POST request with the FormData object
    const response = await fetch('/clouds/api/v1/strains', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.success) {
      // Update the strains data and re-render the strains list
      strainsData.push(data.strain);
      renderStrains();

      // Close the modal and clear the form inputs
      const createStrainModal = new bootstrap.Modal(document.getElementById('createStrainModal'));
      createStrainModal.hide();
      document.querySelector('#createStrainForm').reset();
    } else {
      alert('Error creating strain: ' + data.message);
    }
  } catch (error) {
      console.error('Error creating strain:', error);
  }
}

// Function to set up the event listener for the form submission
function setupCreateStrainForm() {
  const createStrainForm = document.querySelector('#createStrainForm');
  createStrainForm.addEventListener('submit', submitCreateStrain);
}

// Function to handle the UPDATE form submission
async function submitUpdateStrain(event) {
  event.preventDefault();

  // Get the strain ID and data from the form
  const strainId = document.querySelector('#modal_strain_id').value;
  const name = document.querySelector('#update_name').value;
  const type = document.querySelector('#update_type').value;
  const delta_nine_concentration = document.querySelector('#update_delta_nine_concentration').value;
  const cbd_concentration = document.querySelector('#update_cbd_concentration').value;
  const terpene_profile = document.querySelector('#update_terpene_profile').value;
  const effects = document.querySelector('#update_effects').value;
  const uses = document.querySelector('#update_uses').value;
  const flavor = document.querySelector('#update_flavor').value;
  const image = document.querySelector('#update_image').files[0];

  // Create a FormData object to handle the image upload
  let formData = new FormData();

  // Append the form inputs to the FormData object
  formData.append("name", name);
  formData.append("type", type);
  formData.append("delta_nine_concentration", delta_nine_concentration);
  formData.append("cbd_concentration", cbd_concentration);
  formData.append("terpene_profile", terpene_profile);
  formData.append("effects", effects);
  formData.append("uses", uses);
  formData.append("flavor", flavor);
  if (image) {
    formData.append("image", image);
  }

  try {
    // Send the PUT request with the FormData object
    const response = await fetch(`/clouds/api/v1/strains/${strainId}`, {
      method: 'PUT',
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      // Update the strains data and re-render the strains list
      const strainIndex = strainsData.findIndex((strain) => strain.id === strainId);
      strainsData[strainIndex] = data.strain;
      renderStrains();

      // Close the modal and clear the form inputs
      const updateStrainModalInstance = new bootstrap.Modal(document.getElementById('updateStrainModal'));
      updateStrainModalInstance.hide();

      // Add a delay before resetting the form
      setTimeout(() => {
        document.querySelector('#updateStrainForm').reset();
      }, 500);
    } else {
      alert('Error updating strain: ' + data.message);
    }
  } catch (error) {
    console.error('Error updating strain:', error);
  }
}

function setupUpdateStrainForm() {
  const updateStrainForm = document.querySelector('#updateStrainForm');
  updateStrainForm.addEventListener('submit', submitUpdateStrain);
}

// Function to handle the DELETE form submission
async function deleteStrain(strainId) {
  try {
    const response = await fetch(`/clouds/api/v1/strains/${strainId}`, {
      method: 'DELETE',
    });

    const data = await response.json();

    if (data.success) {
      // Remove the strain from the strains data and re-render the strains list
      strainsData = strainsData.filter((strain) => strain.id !== strainId);
      renderStrains();

      // Close the modal
      const deleteStrainModalInstance = new bootstrap.Modal(document.getElementById('deleteStrainModal'));
      deleteStrainModalInstance.hide();
    } else {
      alert('Error deleting strain: ' + data.message);
    }
  } catch (error) {
    console.error('Error deleting strain:', error);
  }
}

// Function to set up the event listener for the openCreateStrainModal button
function setupOpenCreateStrainModalButton() {
  const openCreateStrainModalButton = document.querySelector('#openCreateStrainModal');
  openCreateStrainModalButton.addEventListener('click', () => {
    const createStrainModal = new bootstrap.Modal(document.getElementById('createStrainModal'));
    createStrainModal.show();
  });
}

// Function to open the delete strain modal
function openDeleteStrainModal(strainId) {
  const deleteStrainModalElement = document.getElementById('deleteStrainModal');
  const deleteStrainModal = new bootstrap.Modal(deleteStrainModalElement);
  const confirmDeleteStrainButton = document.getElementById('confirmDeleteStrain');

  // Remove existing event listeners
  confirmDeleteStrainButton.replaceWith(confirmDeleteStrainButton.cloneNode(true));
  const newConfirmDeleteStrainButton = document.getElementById('confirmDeleteStrain');
  
  newConfirmDeleteStrainButton.onclick = () => deleteStrain(strainId);

  deleteStrainModal.show();
}

// Function to open the update strain modal
function openUpdateStrainModal(strainId) {
  const updateStrainModalElement = document.getElementById('updateStrainModal');
  const updateStrainModal = new bootstrap.Modal(updateStrainModalElement);
  const strain = strainsData.find((strain) => strain.id === strainId);

  document.getElementById('modal_strain_id').value = strain.id;
  document.getElementById('update_name').value = strain.name;
  document.getElementById('update_type').value = strain.type;
  document.getElementById('update_delta_nine_concentration').value = strain.delta_nine_concentration;
  document.getElementById('update_cbd_concentration').value = strain.cbd_concentration;
  document.getElementById('update_terpene_profile').value = strain.terpene_profile;
  document.getElementById('update_effects').value = strain.effects;
  document.getElementById('update_uses').value = strain.uses;
  document.getElementById('update_flavor').value = strain.flavor;

  updateStrainModal.show();
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  fetchStrains();
  setupCreateStrainForm();
  setupUpdateStrainForm();
  setupOpenCreateStrainModalButton();
});

//Filtering
document.addEventListener("DOMContentLoaded", function() {
  // Filtering
  document.getElementById("filter_type").addEventListener("change", filterStrains);
  document.getElementById("filter_thc").addEventListener("input", function() {
    document.getElementById("thc_value").innerText = this.value + '%';
    filterStrains();
  });
  document.getElementById("filter_cbd").addEventListener("input", function() {
    document.getElementById("cbd_value").innerText = this.value + '%';
    filterStrains();
  });
});

function filterStrains() {
  const filterType = document.getElementById("filter_type").value;
  const filterTHC = parseFloat(document.getElementById("filter_thc").value);
  const filterCBD = parseFloat(document.getElementById("filter_cbd").value);

  const filteredStrains = strainsData.filter(strain => {
    const typeMatch = !filterType || strain.type === filterType;
    const thcMatch = isNaN(filterTHC) || strain.delta_nine_concentration >= filterTHC;
    const cbdMatch = isNaN(filterCBD) || strain.cbd_concentration >= filterCBD;

    return typeMatch && thcMatch && cbdMatch;
  });

  renderStrains(filteredStrains);
}
