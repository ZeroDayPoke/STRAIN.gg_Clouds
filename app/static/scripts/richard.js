let strainsData = [];

// Fetch all strains
async function fetchStrains() {
  try {
    const response = await fetch('/clouds/api/strains');
    const data = await response.json();
    strainsData = data;
    renderStrains();
  } catch (error) {
    console.error('Error fetching strains:', error);
  }
}

// Function to render the strains list
function renderStrains() {
  const strainsTableBody = document.querySelector('#strainsTableBody');
  strainsTableBody.innerHTML = strainsData
    .map((strain) => `
      <tr>
        <td>${strain.name}</td>
        <td>${strain.delta_nine_concentration}</td>
        <td>${strain.target_symptom}</td>
        <td>
          <button class="btn btn-sm btn-warning" onclick="openUpdateStrainModal('${strain.id}')">Edit</button>
          <button class="btn btn-sm btn-danger" onclick="openDeleteStrainModal('${strain.id}')">Delete</button>
        </td>
      </tr>`)
    .join('');
}

// Function to handle the form submission
async function submitCreateStrain(event) {
  event.preventDefault();

  const name = document.querySelector('#name').value;
  const delta_nine_concentration = document.querySelector('#delta_nine_concentration').value;
  const target_symptom = document.querySelector('#target_symptom').value;

  try {
    const response = await fetch('/clouds/api/strains', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
        delta_nine_concentration,
        target_symptom,
      }),
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

// Update strain
async function submitUpdateStrain(event) {
  event.preventDefault();

  // Get the strain ID and data from the form
  const strainId = document.querySelector('#modal_strain_id').value;
  const name = document.querySelector('#update_name').value;
  const delta_nine_concentration = document.querySelector('#update_delta_nine_concentration').value;
  const target_symptom = document.querySelector('#update_target_symptom').value;

  try {
    const response = await fetch(`/clouds/api/strains/${strainId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
        delta_nine_concentration,
        target_symptom,
      }),
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

// Delete strain
async function deleteStrain(strainId) {
  try {
    const response = await fetch(`/clouds/api/strains/${strainId}`, {
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

function openUpdateStrainModal(strainId) {
  const updateStrainModalElement = document.getElementById('updateStrainModal');
  const updateStrainModal = new bootstrap.Modal(updateStrainModalElement);
  const strain = strainsData.find((strain) => strain.id === strainId);

  document.getElementById('modal_strain_id').value = strain.id;
  document.getElementById('update_name').value = strain.name;
  document.getElementById('update_delta_nine_concentration').value = strain.delta_nine_concentration;
  document.getElementById('update_target_symptom').value = strain.target_symptom;

  updateStrainModal.show();
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  fetchStrains();
  setupCreateStrainForm();
  setupUpdateStrainForm();
  setupOpenCreateStrainModalButton();
});
