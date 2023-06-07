var choicesTypes = document.getElementById("choicesTypes");
var fetchData;


fetch('http://localhost:8000/equipment/get_models')
    .then(response => response.json())
    .then(data => {

        fetchData = Object.values(data);

        console.log(fetchData);
        choicesTypes.innerHTML = "<option value='' selected disabled>ESCOLHA O TIPO DO EQUIPAMENTO</option>";

        fetchData.forEach(element => {
            console.log(element);
            choicesTypes.innerHTML += "<option value=" + element.eng_name + ">" + element.name + "</option>";
        });
    })
    .catch();

choicesTypes.addEventListener('change', () => {
    const selectedValue = choicesTypes.value;
    const choicesModels = document.getElementById("choicesModels");

    // Limpar as opções existentes e adicionar uma opção padrão
    choicesModels.innerHTML = "<option value='' selected disabled>ESCOLHA O MODELO DO EQUIPAMENTO</option>";

    if (selectedValue != '') {
        choicesModels.disabled = false; // Habilitar o elemento choicesTypes durante o processamento
        fetchData.forEach(element => {
            if (selectedValue === element.eng_name) {
                element.models.forEach(i => {
                    choicesModels.innerHTML += "<option value='" + i + "' >" + i + "</option>";
                });
            }
        });
    }
    else {
        choicesModels.disabled = true; // Desabilitar o elemento choicesTypes durante o processamento
    }
});

