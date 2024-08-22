// funcs.js
document.getElementById("generator-form").onsubmit = async function(event) {
    event.preventDefault();
    
    const size = document.getElementById("size").value;
    const rng = document.getElementById("rng").value;
    const mode = document.getElementById("mode").value;
    const round = document.getElementById("round").value;

    try {
        const response = await fetch(`/rand_m?size=${size}&rng=${rng}&mode=${mode}`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Convert the matrix to an HTML table
        let tableHTML = '<div class="table-container"><table><tbody>';
        data.result.forEach(row => {
            tableHTML += '<tr>';
            row.forEach(cell => {
                tableHTML += `<td>${cell.toFixed(round)}</td>`; // Round values to 2 decimal places
            });
            tableHTML += '</tr>';
        });
        tableHTML += '</tbody></table></div>';
        
        document.getElementById("result").innerHTML = tableHTML;

        document.getElementById("copy-button").style.display = "block";
        document.getElementById("copy-button").onclick = () => copyMatrix(data.result);

        // Display global info in dropdown
        let globalInfoHTML = `
            <h6>Global Info</h6>
            <p><strong>Base URL:</strong> <a href = "${data.global_info.GlobalRet.base_url}" target="_blank">${data.global_info.GlobalRet.base_url}</a></p>
            <p><strong>Full Path:</strong> <a href = "${data.global_info.GlobalRet.full_path}" target="_blank">${data.global_info.GlobalRet.full_path}</a> </p>
            <p><strong>Method:</strong> ${data.global_info.GlobalRet.method}</p>
            <p><strong>Path:</strong> <a href = "${data.global_info.GlobalRet.path}" target="_blank">${data.global_info.GlobalRet.path}</a></p>
            <p><strong>Host:</strong> ${data.global_info.GlobalRet.host}</p>
            <p><strong>Host URL:</strong> <a href = "${data.global_info.GlobalRet.host_url}" target="_blank">${data.global_info.GlobalRet.host_url}</a></p>
            <p><strong>API Key:</strong> ${data.global_info.api_key.substring(0, 20)}... (truncated)</p>
            <p><strong>Link to API:</strong> <a href="${data.global_info.link_to_api}" target="_blank">${data.global_info.link_to_api}</a></p>
        `;
        document.getElementById("global-info-main").style.display = "block";
        document.getElementById("global-info").innerHTML = globalInfoHTML;
        
    } catch (error) {
        document.getElementById("error").innerHTML = error.message;
    }
}


function copyMatrix(matrix) {
    // Convert matrix to JSON string
    const matrixString = JSON.stringify(matrix);
    
    // Create a temporary textarea to copy the string
    const textarea = document.createElement("textarea");
    textarea.value = matrixString;
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        // Copy to clipboard
        document.execCommand('copy');
        alert("Matrix copied to clipboard!");
    } catch (err) {
        alert("Failed to copy matrix.");
    }
    
    // Remove the temporary textarea
    document.body.removeChild(textarea);
}