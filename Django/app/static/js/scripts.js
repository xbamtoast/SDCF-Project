function applicationTableSearch() {
  // Declare variables
  var input, filter, table, tr, tds, i, j, txtValue, match;
  input = document.getElementById("applications_search");
  filter = input.value.toUpperCase();
  table = document.getElementById("applications_table");
  tr = table.getElementsByTagName("tr"); // Get all rows, including the header

  // Loop through all table rows, starting from index 1 to skip the header
  for (i = 1; i < tr.length; i++) {
    tds = tr[i].getElementsByTagName("td"); // Get all columns for the current row
    match = false; // Flag to check if the row matches the filter

    // Loop through all columns in the current row
    for (j = 0; j < tds.length; j++) {
      td = tds[j];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          match = true; // A match is found in at least one column
          break; // No need to check further columns in this row
        }
      }
    }

    // Display or hide the row based on whether a match was found
    if (match) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }
  }
}

function sortTable(n) {
    let table = document.getElementById("applications_table");
    let rows = Array.from(table.rows).slice(1); // Skip header row
    let isAscending = table.dataset.sortOrder === "asc";
    
    // Sort rows based on text content
    rows.sort((a, b) => {
        let valA = a.cells[n].textContent.trim();
        let valB = b.cells[n].textContent.trim();
        return isAscending 
            ? valA.localeCompare(valB) 
            : valB.localeCompare(valA);
    });
    
    // Re-append sorted rows
    table.tBodies[0].append(...rows);
    
    // Toggle sort order
    table.dataset.sortOrder = isAscending ? "desc" : "asc";
}

// Color application statuses on the applications page.

function colorApplicationStatus()
{

    let statuses = document.getElementsByClassName("application_status");
    let color_dict = {"Approved":"green", "Review":"red"}
    for (i = 0; i< statuses.length; i++)
    {
       let new_color = color_dict[statuses[i].innerText]
       console.log(new_color)
       console.log(statuses[i].innerText)
       statuses[i].style.color = new_color;
       statuses[i].style.fontWeight = "bold";
    }

}

colorApplicationStatus();