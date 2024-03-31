// Logic to be executed once tabulator table is fully built
function afterTableBuilt() {
    let suspendBtns = document.getElementsByClassName('suspend-btn');
    let userIdInput = document.querySelector('#suspendModalBox input[name="user_id"]');

    // Event listener for the suspend button click
    for (let i = 0; i < suspendBtns.length; i++) {
        suspendBtns[i].addEventListener('click', function (event) {
            console.log(event);
            console.log(document.getElementsByClassName('suspend-btn'));
            // Get the user id value
            let userId = this.getAttribute('data-userid');
            console.log(userId);
            // Set the user id value to the hidden input tag in the modal form
            userIdInput.value = userId;
        });
    }
}


// Create and Setup Tabulator table
let tableData = [];
let rows = document
        .getElementById("admin-table")
        .getElementsByTagName("tbody")[0]
        .getElementsByTagName("tr");

for (let i = 0; i < rows.length; i++) {
    let row = rows[i];
    let rowData = {};
    let cells = row.getElementsByTagName("td");
    rowData.user_type = cells[0].textContent.trim();
    rowData.id = cells[1].textContent.trim();
    rowData.email_username = cells[2].textContent.trim();
    rowData.action = cells[3].innerHTML.trim();
    rowData.suspend_message = cells[4].textContent.trim();
    tableData.push(rowData);
}

function actionFormatter(cell) {
    return cell.getValue();
}

let table = new Tabulator("#admin-table", {
    layout: "fitColumns",
    pagination: "local",
    paginationSize: 10,
    columns: [
        {
            title: "User Type",
            field: "user_type",
            headerFilter: true,
            headerFilterPlaceholder: "Search...",
            headerFilterPlaceholderParsed: true,
            formatter: actionFormatter
        },
        {title: "User ID", field: "id", headerFilter: true, headerFilterPlaceholder: "Search...",},
        {title: "Email", field: "email_username", headerFilter: true, headerFilterPlaceholder: "Search...",},
        {
            title: "Action",
            field: "action",
            headerFilter: false,
            headerSort: false,
            formatter: actionFormatter,
            width: 200
        },
        {
            title: "Suspend Message",
            field: "suspend_message",
            headerFilter: true,
            headerFilterPlaceholder: "Search...",
        }
    ]
});

// Callback to afterTableBuilt callback
table.on("tableBuilt", function () {
    table.setData(tableData);
    afterTableBuilt();
});


// Other code
document.getElementById("apply-filter").addEventListener("click", function () {
    let column = document.getElementById("filter-column").value;
    let type = document.getElementById("filter-type").value;
    let value = document.getElementById("filter-value").value;

    if (column && type && value) {
        if (column === "user_type") {
            if (type === "=") {
                table.setFilter(function (data) {
                    let userType = he.decode(data.user_type.trim());
                    return userType === value;
                });
            } else if (type === "!=") {
                table.setFilter(function (data) {
                    let userType = he.decode(data.user_type.trim());
                    return userType !== value;
                });
            }
        } else {
            table.setFilter(column, type, value);
        }
    }
});

document.getElementById("clear-filter").addEventListener("click", function () {
    table.clearFilter();
    document.getElementById("filter-column").value = "Select Column";
    document.getElementById("filter-type").value = "=";
    document.getElementById("filter-value").value = "";
});
