let table_itens = document.getElementById("actually_load");
let list_equipment;

setInterval(fetchList, 1000);

function fetchList() {
    fetch("http://localhost:8000/carga/lista_equipamentos/get", {
    method: 'POST', // Método HTTP POST para enviar dados
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
        'user': user,
        'pass': pass,
    })}) // faz uma requisição da lista
    .then(response => response.json())
    .then(data => {
        table_itens.innerHTML = "";
        list_equipment = data;
        for (let key in list_equipment) { // percorre a lista se existir
            insertLine(list_equipment[key]); // insere cada objeto novamente na tabela
        }
    })
}
// Insere na tabela uma line que é um objeto 
// equipment com um model em formato json
function insertLine(line, x) {
    x = x ?? true;
    table_itens.innerHTML += // Insere efetivamente na lista => {
        '<tr>' +
        '<td></td>' +
        '<td>' + (line.equipment.serial_number == null || line.equipment.serial_number == undefined ? "-" : line.equipment.serial_number) + '</td>' +
        '<td>' + (line.model.description == null || line.model.description == undefined ? "-" : line.model.description) + '</td>' +
        '<td>' + (line.campo == null || line.campo == undefined ? "-" : line.campo) + '</td>' +
        '<td>' + (line.model.caliber == null || line.model.caliber == undefined ? "-" : line.model.caliber) + '</td>' +
        '<td>' + (line.amount == null || line.amount == undefined || line.amount == '' ? "1" : line.amount) + '</td>' +
        '<td>' + (line.registred == 'wearable' ? line.model.size : "-") + '</td>' +
        '<td>' + (line.equipment.observation == null || line.equipment.observation == undefined ? "-" : line.equipment.observation) + '</td>' +
        '<td></td>' +
        '</tr>' // => }

    // renumera e adiciona o botão de deletar
    updateRowNumbers(x);
}

// Básicamente checa o numero que foi retirado e renumera as linha de acordo e coloca o botão de excluir linha
function updateRowNumbers() {
    var rows = table_itens.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        cells[0].innerHTML = i + 1; // primeira coluna, a do numero de série da tabela
    }
}

function confirmCargo(self) {
    self.style['background-color'] = "#9999";
    self.style.color = "black";
    fetch('http://localhost:8000/equipamento/allow_cargo', {
            method: 'POST', // Método HTTP POST para enviar dados
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'user': user,
            'pass': pass,
        })}); // faz uma requisição da lista
}