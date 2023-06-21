let storesData = [];

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  fetchStores();
  setupCreateStoreForm();
  setupUpdateStoreForm();
  setupOpenCreateStoreModalButton();
  setupAddStrainForm();
});

async function fetchStores() {
  try {
    const response = await fetch('/clouds/api/stores');
    const data = await response.json();
    storesData = data;
    renderStores();
  } catch (error) {
    console.error('Error fetching stores:', error);
  }
}

function renderStores(storesToRender = storesData) {
  const storesContainer = document.querySelector('#storesContainer');
  storesContainer.innerHTML = '<div class="row"></div>';

  let currentRow = storesContainer.querySelector(".row");

  storesToRender.forEach(async (store, index) => {
    // You may need to modify the following HTML to match the properties of the Store model
    const storeCard = `
    <div class="col-md-6 mb-4">
      <div class="store-card">
        <h3>${store.name}</h3>
        <p>Location: ${store.location}</p>
        <p>Operating Hours: ${store.operating_hours}</p>
        <p>Owner ID: ${store.owner_id}</p>
        <div class="store-card-buttons">
          <button class="btn btn-sm btn-warning" onclick="openUpdateStoreModal('${store.id}')">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="openDeleteStoreModal('${store.id}')">Delete</button>
          <button class="btn btn-primary mt-2" onclick="showAddStrainForm('${store.id}')">>Add Strain</button>
          <div class="dropdown">
          <button class="btn btn-primary dropdown-toggle" type="button" id="strainDropdown-${store.id}" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Strains
          </button>
          <ul class="dropdown-menu" aria-labelledby="strainDropdown-${store.id}" id="strainList-${store.id}">
            <!-- The strains will be populated here by the populateStrainDropdown function -->
          </ul>
          </div>
        </div>
      </div>
    </div>`;

    currentRow.innerHTML += storeCard;

    // Populate the strain dropdown for the current store
    await populateStrainDropdown(store.id);

    // Create a new row for every two store cards
    if (index % 2 === 1) {
      const newRow = document.createElement("div");
      newRow.className = "row";
      storesContainer.appendChild(newRow);
      currentRow = newRow;
    }
  });
}

// Function to set up the event listener for the openCreateStoreModal button
function setupOpenCreateStoreModalButton() {
  const openCreateStoreModalButton = document.querySelector('#openCreateStoreModal');
  openCreateStoreModalButton.addEventListener('click', () => {
    const createStoreModal = new bootstrap.Modal(document.getElementById('createStoreModal'));
    createStoreModal.show();
  });
}

// Function to set up the event listener for the form submission
function setupCreateStoreForm() {
  const createStoreForm = document.querySelector('#createStoreForm');
  createStoreForm.addEventListener('submit', submitCreateStore);
}

// Function to handle the CREATE form submission
async function submitCreateStore(event) {
  event.preventDefault();

  // Create a FormData object to handle the image upload
  let formData = new FormData();

  // Retrieve the form inputs
  let name = $("#name").val();
  let location = $("#location").val();
  let operating_hours = $("#operating_hours").val();
  let owner_id = userId;
  let image = $("#image").get(0).files[0];

  // Append the form inputs to the FormData object
  formData.append("name", name);
  formData.append("location", location);
  formData.append("operating_hours", operating_hours);
  formData.append("owner_id", owner_id);
  formData.append("image", image);

  try {
    // Send the POST request with the FormData object
    const response = await fetch('/clouds/api/stores', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.success) {
      // Update the stores data and re-render the stores list
      storesData.push(data.store);
      renderStores();

      // Close the modal and clear the form inputs
      const createStoreModal = new bootstrap.Modal(document.getElementById('createStoreModal'));
      createStoreModal.hide();
      document.querySelector('#createStoreForm').reset();
    } else {
      alert('Error creating Store: ' + data.message);
    }
  } catch (error) {
      console.error('Error creating Store:', error);
  }
}

// Event listener for Update Form
function setupUpdateStoreForm() {
  const updateStoreForm = document.querySelector('#updateStoreForm');
  updateStoreForm.addEventListener('submit', submitUpdateStore);
}

// Function to open the update store modal
function openUpdateStoreModal(storeId) {
  const updateStoreModalElement = document.getElementById('updateStoreModal');
  const updateStoreModal = new bootstrap.Modal(updateStoreModalElement);
  const store = storesData.find((store) => store.id === storeId);

  document.getElementById('modal_store_id').value = store.id;
  document.getElementById('update_name').value = store.name;
  document.getElementById('update_location').value = store.location;
  document.getElementById('update_operating_hours').value = store.operating_hours;

  updateStoreModal.show();
}

// Function to handle the UPDATE form submission
async function submitUpdateStore(event) {
  event.preventDefault();

  // Get the Store ID and data from the form
  const storeId = document.querySelector('#modal_store_id').value;
  const name = document.querySelector('#update_name').value;
  const location = document.querySelector('#update_location').value;
  const operating_hours = document.querySelector('#update_operating_hours').value;
  const image = document.querySelector('#update_image').files[0];

  // Create a FormData object to handle the image upload
  let formData = new FormData();

  // Append the form inputs to the FormData object
  formData.append("name", name);
  formData.append("location", location);
  formData.append("operating_hours", operating_hours);
  if (image) {
    formData.append("image", image);
  }

  try {
    // Send the PUT request with the FormData object
    const response = await fetch(`/clouds/api/stores/${storeId}`, {
      method: 'PUT',
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      // Update the stores data and re-render the stores list
      const storeIndex = storesData.findIndex((store) => store.id === storeId);
      storesData[storeIndex] = data.store;
      renderStores();

      // Close the modal and clear the form inputs
      const updateStoreModalInstance = new bootstrap.Modal(document.getElementById('updateStoreModal'));
      updateStoreModalInstance.hide();

      // Add a delay before resetting the form
      setTimeout(() => {
        document.querySelector('#updateStoreForm').reset();
      }, 500);
    } else {
      alert('Error updating Store: ' + data.message);
    }
  } catch (error) {
    console.error('Error updating Store:', error);
  }
}

// Function to open the delete store modal
function openDeleteStoreModal(storeId) {
  const deleteStoreModalElement = document.getElementById('deleteStoreModal');
  const deleteStoreModal = new bootstrap.Modal(deleteStoreModalElement);
  const confirmDeleteStoreButton = document.getElementById('confirmDeleteStore');

  // Remove existing event listeners
  confirmDeleteStoreButton.replaceWith(confirmDeleteStoreButton.cloneNode(true));
  const newConfirmDeleteStoreButton = document.getElementById('confirmDeleteStore');
  
  newConfirmDeleteStoreButton.onclick = () => deleteStore(storeId);

  deleteStoreModal.show();
}

// Function to handle the DELETE form submission
async function deleteStore(storeId) {
  try {
    const response = await fetch(`/clouds/api/stores/${storeId}`, {
      method: 'DELETE',
    });

    const data = await response.json();

    if (data.success) {
      // Remove the store from the stores data and re-render the stores list
      storesData = storesData.filter((store) => store.id !== storeId);
      renderStores();

      // Close the modal
      const deleteStoreModalInstance = new bootstrap.Modal(document.getElementById('deleteStoreModal'));
      deleteStoreModalInstance.hide();
    } else {
      alert('Error deleting Store: ' + data.message);
    }
  } catch (error) {
    console.error('Error deleting Store:', error);
  }
}

async function getStrainsByStoreId(storeId) {
  // Replace this with the actual API call to fetch strains for a given store
  const response = await fetch(`/clouds/api/stores/${storeId}/strains`);
  const strains = await response.json();
  return strains;
}

// Function to populate the strain dropdown for the current store
async function populateStrainDropdown(storeId) {
  // Fetch the strains for the given store
  const strains = await getStrainsByStoreId(storeId);

  // Get the dropdown menu element
  const strainList = document.getElementById(`strainList-${storeId}`);

  // Clear the existing strains from the dropdown
  strainList.innerHTML = '';

  // Add each strain to the dropdown menu
  strains.forEach((strain) => {
    const listItem = document.createElement('li');
    listItem.innerHTML = `<a class="dropdown-item" href="#" data-strain-id="${strain.id}">${strain.name}</a>`;
    strainList.appendChild(listItem);
  });
}

// Function to show the add strain form
function showAddStrainForm(storeId) {
  document.getElementById('store-id-input').value = storeId;
  const addStrainModal = new bootstrap.Modal(document.getElementById('addStrainModal'));
  addStrainModal.show();
}

// Event listener for Add Strain Form
function setupAddStrainForm() {
  const addStrainForm = document.querySelector('#addStrainForm');
  addStrainForm.addEventListener('submit', submitAddStrainForm);
}

// Function to handle the ADD STRAIN form submission
async function submitAddStrainForm(event) {
  event.preventDefault();

  const storeId = document.getElementById('store-id-input').value;
  const strainId = document.getElementById('strain-id-input').value;

  let formData = new FormData();
  formData.append("store_id", storeId);
  formData.append("strain_id", strainId);
  try {
    // Send the PUT request with the FormData object
    const response = await fetch(`/clouds/api/stores/${storeId}/strains`, {
      method: 'PUT',
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      // Refresh the strain dropdown for the store
      await populateStrainDropdown(storeId);

      // Close the modal and clear the form inputs
      const addStrainModal = new bootstrap.Modal(document.getElementById('addStrainModal'));
      addStrainModal.hide();
      document.querySelector('#addStrainForm').reset();
    } else {
      alert('Error adding strain: ' + data.message);
    }
  } catch (error) {
    console.error('Error adding strain:', error);
  }
}
