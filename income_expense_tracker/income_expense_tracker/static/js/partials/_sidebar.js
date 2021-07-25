// Add active class in selected list items
const list = document.querySelectorAll('.list');
const dashboard = document.querySelector('#dashboard_nav');
const expenses = document.querySelector('#expenses_nav');
const report = document.querySelector('#report_nav');

for (let i = 0; i < list.length; i++) {
  list[i].onclick = () => {
    let j = 0;
    while (j < list.length) {
      list[j++].className = "list"
    }
    list[i].className = "list active"
  }
}

// dashboard.toggleClass('active');
//
// report.toggleClass('active');

// dashboard.className = "list active";
//
// function makeLinkActive(list) {
//   for (let i = 0; i < list.length; i++) {
//       list[i].className = "list";
//     }
// }

// dashboard.addEventListener('click', (e) => {
//   makeLinkActive(list);
//   e.target.className = "list active";
//   console.log(e.target.innerHTML);
// })
//
// expenses.addEventListener('click', (e) => {
//   makeLinkActive(list);
//   e.target.className = "list active";
//   console.log(e.target.innerHTML);
//   expenses.toggleClass('active');
// })
//
// report.addEventListener('click', (e) => {
//   makeLinkActive(list);
//   e.target.className = "list active";
//   console.log(e.target.innerHTML);
// })
