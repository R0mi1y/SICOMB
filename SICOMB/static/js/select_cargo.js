function changeTemplate(template) {
    fetch("/static/html/" + template + ".html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("means_room_content").innerHTML = data;
        })
    if (template == "cargo") {
        setTimeout(() => {
            var script = document.createElement('script');
            script.src = '/static/js/fetch_cargo.js';
            document.head.appendChild(script);
        }, 500)
    }
}

var turn_type;

function setTurnType() {
    var radioSelecionado = document.querySelector('input[name="options_load"]:checked');

    if (radioSelecionado && radioSelecionado.value) {
        var inputElement = document.createElement("input");
        inputElement.type = "hidden";
        inputElement.name = "turn_type";
        inputElement.value = radioSelecionado.value;
        document.getElementById("form-equipment").appendChild(inputElement);

        turn_type = radioSelecionado.value;
        changeTemplate("cargo");
    } else {
        popUp("Selecione uma das opções!");
    }
}

var interval = setInterval(() => {
    let url = 'http://localhost:8000/police/get_login/';
    fetch(url)
        .then(response => response.json())
        .then(policial => {
            console.log(policial);
            if (policial && Object.keys(policial).length !== 0) {
                clearInterval(interval);

                let table = `<table class="police_officer_table">
            <thead>
                <tr>
                    <th class="cargo_title">` + policial.lotacao + `</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <a href="#"><img class="shadow" src="/media/` + policial.foto + `" alt=""></a>
                    </td>
                </tr>
                <tr>
                    <td>` + policial.nome + `</td>
                </tr>
                <tr>
                    <td>` + policial.matricula + `</td>
                </tr>
                <tr>
                    <td>` + policial.telefone + `</td>
                </tr>
                <tr>
                    <td>` + policial.lotacao + `</td>
                </tr>
                <tr>
                    <td>` + policial.email + `</td>
                </tr>
            </tbody>
            </table>`;

                var inputElement = document.createElement("input");
                inputElement.type = "hidden";
                inputElement.name = "plate";
                inputElement.value = policial.matricula
                document.getElementById("form-equipment").appendChild(inputElement);

                document.getElementById("police_officer_field").innerHTML = table;

                changeTemplate("select_cargo");
            }
        });
}, 1000);