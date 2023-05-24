const typeDropdown = document.getElementById("type");
const typeIdDropdown = document.getElementById("type_id");
const serialNumberInput = document.getElementById("serial_number");
let equipmentData;
// set_date;

set_date = () => {
    var dataAtual = new Date();
    var dia = dataAtual.getDate();
    var mes = dataAtual.getMonth() + 1; // Lembrando que os meses começam em 0
    var ano = dataAtual.getFullYear();
    
    if (dia < 10) {
        dia = '0' + dia;
    }
    
    if (mes < 10) {
        mes = '0' + mes;
    }
    console.log(document.getElementById('date'));
    console.log(document.getElementById('time'));
    document.getElementById('date').value = ano + '/' + mes + '/' + dia;
    document.getElementById("time").value = dataAtual.getHours() + ':' + dataAtual.getMinutes();
}


fetchEquipmentData = () => {
    fetch('http://localhost:8000/equipment/get')
        .then(response => response.json())
        .then(data => {
            console.log(data);

            // Armazena os dados do equipamento em uma variável pra usar depois
            equipmentData = data;

            // Atualiza os campos com as respectivas opções
            if (data.uid !== '') {
                document.getElementById("uid").value = data.uid;
                document.getElementById("uid1").value = data.uid;

                // Para de ficar requisitando
                clearInterval(interval);

                if (data.registred !== false) {
                    let campo;

                    if (data.registred == 'Wearable') {
                        campo = 'Vestível';
                    } else {
                        campo = 'Armamento';
                    }

                    document.getElementById("choice").innerHTML = campo;

                    if (data.registred == 'Wearable') {
                        campo = eval(`data.${data.registred}.model`) + ' ' + eval(`data.${data.registred}.size`);
                    } else if (data.registred == 'Armament') {
                        campo = eval(`data.${data.registred}.model`) + ' ' + eval(`data.${data.registred}.caliber`);
                    } else if (data.registred == 'Bullet') {
                    }

                    document.getElementById("choice_2").innerHTML = campo;
                    serialNumberInput.value = data.equipment.serial_number;
                } else {
                    // Habilita os campo pra cadastro
                    typeDropdown.removeAttribute("disabled");
                    serialNumberInput.removeAttribute("disabled");
                }
            }
        })
        .catch(error => console.error(error));
}

// cria um intervalo pra chamar a função a cada 1 segundo
const interval = setInterval(fetchEquipmentData, 1000);

// cria um evento para cada mudança no select
// typeDropdown.addEventListener('change', function () {
//     if (typeDropdown.value !== '') {
//         console.log(equipmentData);
//         console.log(typeDropdown.value);
//         console.log(equipmentData[typeDropdown.value]);
//         typeIdDropdown.removeAttribute("disabled");

//         typeIdDropdown.innerHTML = '<option value="" id="choice_2" selected="">Tipo específico</option>';

//         // Determina qual propriedade do equipmento usar para o tipo específico do dropdown
//         let property;
//         if (typeDropdown.value === 'Armament') {
//             property = 'caliber';
//         } else {
//             property = 'size';
//         }

//         // Adiciona as options no dropdown
//         for (const key in equipmentData[typeDropdown.value]) {
//             typeIdDropdown.innerHTML += `<option value="${equipmentData[typeDropdown.value][key].id}">${equipmentData[typeDropdown.value][key].model} ${equipmentData[typeDropdown.value][key][property]}</option>`;
//         }
//     } else {
//         typeIdDropdown.setAttribute("disabled", true);
//     }
// });