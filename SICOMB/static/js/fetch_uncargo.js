// seta a data e a hora atual => {
function set_date() {
    var dataAtual = new Date();
    var dia = dataAtual.getDate();
    var mes = dataAtual.getMonth() + 1; // Lembrando que os meses começam em 0
    var ano = dataAtual.getFullYear();

    let diaFormatado = dia < 10 ? '0' + dia : dia;
    let mesFormatado = mes < 10 ? '0' + mes : mes;

    var time = dataAtual.getHours() + ':' + dataAtual.getMinutes();
    var data = diaFormatado + '/' + mesFormatado + '/' + ano;

    document.getElementById('date').innerText = data;
    document.getElementById('time').innerText = time;
}

// => }

function selectCargo(id) {
    
    fetch("/static/html/cargo.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById("means_room_content").innerHTML = data;
        set_date();
        
        fetch('http://localhost:8000/cargo/get/' + id + '/')
            .then(response => response.json())
            .then(data_cargo => {
                for (cargo in data_cargo.equipment_cargos) {
                    console.log(data_cargo.equipment_cargos[cargo]['Equipment&model']);
                    insertLine(data_cargo.equipment_cargos[cargo]['Equipment&model']);
                }
            });
        })
            
    }
