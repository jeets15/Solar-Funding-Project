// Logic to be executed once tabulator table is fully built
function afterTableBuilt() {
    document.getElementById("download-csv").addEventListener("click", function(){
        table.download("csv", "data.csv");
    });
}



function actionFormatter(cell) {
    return cell.getValue();
}

function comparisonFilterEditor(cell, onRendered, success, cancel, editorParams) {
    let container = document.createElement("span");
    let selector = document.createElement("select");
    for (let opt_txt of ["=", "<", ">", "<=", ">="]) {
        let opt = document.createElement("option");
        opt.value = opt_txt;
        opt.innerHTML = opt_txt;
        selector.appendChild(opt);
    }
    selector.style.width = "20%";
    selector.style['min-width'] = "3.2em";
    let filterInput = document.createElement("input");
    filterInput.setAttribute("type", "text");
    filterInput.setAttribute("placeholder", "filter...");
    filterInput.style.width = "80%";

    function buildValues(){
        success({
            compOperator: selector.value,
            filterText: filterInput.value,
        });
    }

    function keypress(e){
        if(e.keyCode == 13){
            buildValues();
        }

        if(e.keyCode == 27){
            cancel();
        }
    }

    selector.addEventListener("change", buildValues);
    filterInput.addEventListener("change", buildValues);
    filterInput.addEventListener("blur", buildValues);
    filterInput.addEventListener("keydown", keypress);

    container.appendChild(selector);
    container.appendChild(filterInput);
    return container;
}
function comparisonFilterFunction(headerValue, rowValue, rowData, filterParams) {
    let dataType = filterParams.data_type;
    if (rowValue) {
        if (headerValue.filterText) {
            let value = rowValue.toLowerCase();
            let target = headerValue.filterText.toLowerCase();
            let comp = headerValue.compOperator;
            if (dataType === "numeric") {
                value = parseFloat(value);
                target = parseFloat(target);
            }
            console.log(value, comp, target)
            if (comp === "=") {
                if (dataType === "string") {
                    return value.includes(target);
                } else {
                    return value == target;
                }
            } else if (comp === "<") {
                return value < target;
            } else if (comp === ">") {
                return value > target;
            } else if (comp === "<=") {
                return value <= target;
            } else if (comp === ">=") {
                return value >= target;
            }
        }
    }
    return true;
}

window.addEventListener('load', function () {
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

    let tabulatorColumns = [
        {title: "Timestamp",    field:"timestamp", headerFilterFuncParams: {data_type: "string"}},
        {title: "Country",      field:"country", headerFilterFuncParams: {data_type: "string"}},
        {title: "Organization", field:"organization", headerFilterFuncParams: {data_type: "string"}},
        {title: "Amount (£)",   field:"amount", sorter:"number", hozAlign: "right", headerFilterFuncParams: {data_type: "numeric"}},
        {title: "Solar Panels", field:"solar_panels", sorter:"number", headerFilterFuncParams: {data_type: "numeric"}},
        {title: "Householder",  field:"householder", headerFilterFuncParams: {data_type: "string"}},
    ];
    
    for (let col of tabulatorColumns) {
        col.frozen = true;
        col.headerFilter = comparisonFilterEditor;
        col.headerFilterFunc = comparisonFilterFunction;
        col.headerFilterLiveFilter = false;
        col.minWidth = 150;
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
});