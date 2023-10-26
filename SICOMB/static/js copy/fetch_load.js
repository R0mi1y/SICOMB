var serialNumberInput = $("#serial_number");
var description = $("#description");
var type = $("#type");
var amount = $("#amount");
var observation = $("#note_equipment");
var insert_btn = $("#insert_btn");
var amount_input = $("#amount_input");
var list_equipment = [];
var semaphore = true;
var square = false;
var equipmentData = null;

set_date();

$.ajax({
    url: "http://localhost:8000/carga/lista_equipamentos/get",
    type: "POST",
    dataType: "json",
    data: {
        user: user,
        pass: pass,
    },
    success: function (data) {
        list_equipment = data;
        $.each(list_equipment, function (key, equipment) {
            console.log(equipment);
            insertLine(equipment);
        });
    }
});

function fetchEquipmentData(serial_number, type = "none") {
    let url = (serial_number == null || serial_number == undefined) ?
        "http://localhost:8000/equipamento/get_disponivel" :
        "http://localhost:8000/equipamento/get/" + serial_number;

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function (data) {
            if (data.uid !== "" && semaphore) {
                if (data.equipment.serial_number != null && data.equipment.serial_number != undefined) {
                    let equipAlreadyInList = Object.keys(list_equipment).find(function (key) {
                        return key == data.equipment.serial_number;
                    });

                    if (equipAlreadyInList) {
                        popUp("Equipamento já na lista!");
                        return;
                    }
                }

                if (data.registred !== false) {
                    list_awate_equipment.push(data);
                    checkAwateList(type);
                }
            } else if (data.confirmCargo) {
                $("#submit_btn").prop("disabled", false).removeClass("btn_disabled").addClass("btn_confirm");
                semaphore = false;
                clearInterval(interval);
            }

            if (data.msm != null) {
                popUp(data.msm);
            }
        },
        error: function (error) {
            console.error("Erro ao buscar dados do equipamento:", error);
        },
    });
}

var interval = setInterval(fetchEquipmentData, 1000);

function check_cargo_square() {
    if (equipmentData != null) {
        equipmentData.amount = amount_input.val();
        insertLine(equipmentData);
        var equipmentKey = equipmentData.equipment.serial_number ?? 'ac' + equipmentData.equipment.id;
        list_equipment[equipmentKey] = {
            serial_number: equipmentData.equipment.serial_number,
            observation: observation.text(),
            amount: equipmentData.amount,
            model: {
                image_path: $("#means_room_product").attr("src"),
            },
        };
        equipmentData.equipment.serial_number = equipmentData.equipment.serial_number ?? equipmentData.model.caliber;

        $.ajax({
            url: "http://localhost:8000/carga/lista_equipamentos/add/",
            type: "POST",
            data: {
                serialNumber: equipmentData.equipment.serial_number,
                observation: observation.val() ?? "-",
                amount: equipmentData.amount,
                user: user,
                pass: pass,
            },
            success: function (data) {
                console.log(data);
            },
            error: function (error) {
                console.error(error);
            },
        });

        equipmentData = null;
        clearSquare();
        interval = setInterval(fetchEquipmentData, 1000);
        checkAwateList();
    }
}

// Requisita passar o equipamento de novo no sensor pra remover
function checkRemoveRow(rowNumber) {
    var rows = table_itens.find("tr");
    var col = rows.eq(rowNumber).find("td");
    obs = col.eq(7).html();
    amount = col.eq(5).html();

    if (col.eq(3).html() !== 'Munição') {
        var serialNum = col.eq(1).html();
        var popup = popUp("Passe de volta o equipamento", { closeBtn: false });

        clearInterval(interval);

        interval = setInterval(function () {
            $.ajax({
                url: 'http://localhost:8000/equipamento/get_disponivel',
                type: 'POST',
                dataType: 'json',
                data: {
                    user: user,
                    pass: pass,
                },
                success: function (data) {
                    if (data.uid !== '') {
                        for (var key in list_equipment) {
                            if (key === data.equipment.serial_number) {
                                if (key == serialNum) {
                                    removeRow(rowNumber);
                                    document.body.removeChild(popup);
                                    clearInterval(interval);
                                    console.log(list_equipment);

                                    $.ajax({
                                        url: 'http://localhost:8000/carga/lista_equipamentos/remover/',
                                        type: 'POST',
                                        data: {
                                            user: user,
                                            pass: pass,
                                            serial_number: caliber,
                                            obs: obs,
                                        },
                                    });

                                    interval = setInterval(fetchEquipmentData, 1000);
                                    return;
                                } else {
                                    popUp("Equipamento incorreto!");
                                    return;
                                }
                            }
                        }
                        if (data.msm != null) {
                            popUp(data.msm);
                        } else {
                            popUp("O equipamento não está na lista!");
                        }
                    }
                },
                error: function (error) {
                    console.error('Erro ao buscar dados do equipamento:', error);
                },
            });
        }, 1000);
    } else {
        var caliber = col.eq(4).html();
        removeRow(rowNumber);

        $.ajax({
            url: 'http://localhost:8000/carga/lista_equipamentos/remover/',
            type: 'POST',
            data: {
                user: user,
                pass: pass,
                serial_number: caliber,
                obs: obs,
            },
        });
    }
}

// Remove a linha da tabela
function removeRow(rowNumber) {
    var rows = table_itens.find("tr");
    var serialNum = rows.eq(rowNumber).find("td").eq(1).html();
    delete list_equipment[serialNum];

    table_itens[0].deleteRow(rowNumber);
    updateRowNumbers();
}

function edit(i) {
    var rows = table_itens.find("tr");
    var serialNum = rows.eq(i).find("td").eq(1).html();
    console.log(rows);
    addToSquare(list_equipment[serialNum]);
    removeRow(i);
}

// checa se a lista tá vazia
function confirmCargo() {
    var rows = table_itens.find("tr");
    if (rows.length > 0) {
        $("#form-equipment").submit();
    } else {
        popUp("Lista vazia!");
    }
}

function checkAwateList(type = 'none') {
    console.log(type);
    if (list_awate_equipment.length > 0) {
        equipmentData = list_awate_equipment[list_awate_equipment.length - 1];
        data = list_awate_equipment[list_awate_equipment.length - 1];
        list_awate_equipment.pop();
        addToSquare(data);

        if (type != "search") {
            check_cargo_square();
        }
    }
}

function searchWatingList() {
    $.ajax({
        url: 'http://localhost:8000/equipamento/lista_espera/get/',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function (data) {
            var waitingList = "";
            for (var i in data) {
                waitingList += "<tr>" + data[i] + "</tr>";
            }
            $("#wating_list").html(waitingList);
        }
    });
}

var intervalWatingList = setInterval(searchWatingList, 1000);
