const filterField = document.querySelector('#filter-category');
const tableOutput = document.querySelector('.table-output');
const mainTable = document.querySelector('.main-table');
const paginationContainer = document.querySelector('.pagination-container');
const tableBody = document.querySelector('.table-body');


tableOutput.style.display = 'none';

filterField.addEventListener('change', (e) => {
  const filterValue = e.target.value;

  if (filterValue !== "Default") {
    paginationContainer.style.display = 'none';
    tableBody.innerHTML = "";
    fetch('/filter-expenses', {
      body: JSON.stringify({ filter_by: filterValue }),
      method: "POST"
    })
      .then(res => res.json())
      .then(data => {

        mainTable.style.display = 'none';
        tableOutput.style.display = 'block';

        if (data.length === 0) {
          tableBody.innerHTML = "<p class='mt-4'>No records found.</p>"
        } else {
          data.forEach((item) => {
            tableBody.innerHTML += `
              <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
              </tr>`;
          });
        }
      })
  } else {
    mainTable.style.display = 'block';
    paginationContainer.style.display = 'block';
    tableOutput.style.display = 'none';
  }
})
