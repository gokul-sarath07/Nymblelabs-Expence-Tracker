const filterField = document.querySelector('#filter-users');
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
    fetch('/admin-dashboard/filter-users', {
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
                <td>${filterValue}</td>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                <td> <a href="../expenses/edit-expense/${item.id}" class="btn btn-secondary btn-sm">Edit</a> </td>
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
