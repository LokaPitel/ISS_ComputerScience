send_json = function(){
    let to_search = document.querySelector('input[name="to_search"]')
    let checkboxes = document.querySelectorAll('input[type=checkbox]')

    to_send = {}

    to_send['to_search'] = to_search.value;

    for (let i = 0; i < checkboxes.length; i ++)
        to_send[checkboxes[i].getAttribute('name')] = checkboxes[i].checked
    
    // Creating a XHR object
    let xml_http_request = new XMLHttpRequest();
    let url = "";

    // open a connection
    xml_http_request.open("POST", url, true);

    // Set the request header i.e. which type of content you are sending
    xml_http_request.setRequestHeader("Content-Type", "application/json");

    // Create a state change callback
    xml_http_request.onreadystatechange = function () {
        if (xml_http_request.readyState === 4 && xml_http_request.status === 200) {

            // Print received data from server
            // result.innerHTML = this.responseText;
            const info_from_server = JSON.parse(this.responseText)
            
            const results_div = document.getElementsByClassName("block_values")[0];
            while (results_div.firstChild) {
                results_div.removeChild(results_div.lastChild);
            }

            let inner = ""

            // console.log(info_from_server[0]['desc'].split(" ").slice(0, 3))

            for (let i = 0; i < info_from_server.length; i ++)
            {
                col_class = ""

                if (i == 0)
                    col_class = "col col-1"

                else
                    col_class = "col"

                inner += `
                <div class="${col_class}">
                    <div class="col_block_img_with_link d-flex">
                        <div class="col_img">
                            <img src="static/img/info_link.svg" alt="">
                        </div>
                        <a href="/info/${info_from_server[i]['id']}/" class="col_link">/info/${info_from_server[i]['id']}/</a>
                    </div>
                    <div class="col_block_h3">
                        <h3 class="col_h3">${info_from_server[i]['name']}</h3>
                    </div>
                    <div class="col_block_p">
                        <p class="col_p">${info_from_server[i]['desc'].split(" ").slice(0, 4).join(" ")}...</p>
                    </div>
                </div>
                `
            }

            console.log()

            results_div.innerHTML = inner
        }
    };

    // Converting JSON data to string
    var data = JSON.stringify(to_send);

    // Sending data with the request
    xml_http_request.send(data);
}

submitForms = function(){
    let i, checkboxes = document.querySelectorAll('input[type=checkbox]');
    for (i = 0; i < checkboxes.length; i++) {
        
        localStorage.setItem(checkboxes[i].getAttribute('name'), checkboxes[i].checked); 
    }

    send_json()
}

const input = document.querySelector('input[name="to_search"]')

input.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      console.log("ТТТТТТТТТТТТТТТТТТТТТТТТТТТТТ")
      submitForms()
    }
  });

load_checkboxes = function() {
    let i, checkboxes = document.querySelectorAll('input[type=checkbox]');
    console.log(checkboxes)
    for (i = 0; i < checkboxes.length; i++) {
        // console.log(checkboxes[i].getAttribute('name'))

        // console.log("Checkbox: " + checkboxes[i].checked)
        // console.log("Storage: " + localStorage.getItem(checkboxes[i].getAttribute('name')))
        // console.log(localStorage.getItem(checkboxes[i].getAttribute('name')));
        if (localStorage.getItem(checkboxes[i].getAttribute('name')) == "true")
            checkboxes[i].checked = true

        else
            checkboxes[i].checked = false
    }

    console.log(checkboxes)
}


