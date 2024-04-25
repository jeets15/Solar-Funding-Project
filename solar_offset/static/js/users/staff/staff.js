// Logic to be executed once tabulator table is fully built
function afterTableBuilt() {
    document.getElementById("download-csv").addEventListener("click", function(){
        table.download("csv", "data.csv");
    });
}

// Create and Setup Tabulator table
let tableData = [];
let rows = document
        .getElementById("donation-data")
        .getElementsByTagName("tbody")[0]
        .getElementsByTagName("tr");

for (let row of rows) {
    let cells = row.getElementsByTagName("td");
    tableData.push({
        timestamp: cells[0].textContent.trim(),
        country: cells[1].textContent.trim(),
        organization: cells[2].textContent.trim(),
        amount: cells[3].textContent.trim(),
        solar_panels: cells[4].textContent.trim(),
        householder: cells[5].textContent.trim(),
    })
}

function actionFormatter(cell) {
    return cell.getValue();
}



let tabulatorColumns = [
    {title: "Timestamp",    field:"timestamp"},
    {title: "Country",      field:"country"},
    {title: "Organization", field:"organization"},
    {title: "Amount (£)",   field:"amount", sorter:"number", hozAlign: "right"},
    {title: "Solar Panels", field:"solar_panels", sorter:"number"},
    {title: "Householder",  field:"householder"},
];

for (let col of tabulatorColumns) {
    col.frozen = true;
    col.headerFilter = true;
    col.headerFilterPlaceholder = "filter...";
}

let table = new Tabulator('#donation-data', {
    layout: "fitData",
    pagination: "local",
    paginationSize: 50,
    columns: tabulatorColumns
});

// Callback to afterTableBuilt callback
table.on("tableBuilt", function () {
    table.setData(tableData);
    afterTableBuilt();
});