var list_equipment = [];
var square_equipment;
var list_returned_equipment = [];
var id_cargo;
var done_svg =
    '<svg fill="green" height="24" viewBox="0 -960 960 960" width="24"><path d="M382-240 154-468l57-57 171 171 367-367 57 57-424 424Z"/></path></svg>';

// seta a data e a hora atual => {
function set_date() {
    var dataAtual = new Date();
    var dia = dataAtual.getDate();
    var mes = dataAtual.getMonth() + 1;
    var ano = dataAtual.getFullYear();

    var diaFormatado = dia < 10 ? "0" + dia : dia;
    var mesFormatado = mes < 10 ? "0" + mes : mes;

    var time = dataAtual.getHours() + ":" + dataAtual.getMinutes();
    var data = diaFormatado + "/" + mesFormatado + "/" + ano;

    $("#date").text(data);
    $("#time").text(time);

    $("#cancel_btn")
        .prop("disabled", false)
        .removeClass("btn_disabled")
        .addClass("btn_cancel");
}

function set_carga_id(id) {
    id_cargo = id;

    var inputHidden = $("<input>").attr({
        type: "hidden",
        name: "turn_type",
        value: "descarga",
    });
    $("#form-equipment").append(inputHidden);

    inputHidden = $("<input>").attr({
        type: "hidden",
        name: "load_id",
        value: id,
    });
    $("#form-equipment").append(inputHidden);

    $("#insert_btn").val("DEVOLVER");

    $.ajax({
        url: "/carga/get/" + id_cargo + "/",
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function (data_cargo) {
            $.each(data_cargo.equipment_loads, function (cargo, equipment) {
                insertLine(equipment["Equipment&model"], false);
                list_equipment.push(equipment["Equipment&model"]);
            });
            $(document).ready(function () {
                $.ajax({
                    url: "/carga/lista_equipamentos_atual/get",
                    type: "POST",
                    dataType: "json",
                    data: {
                        user: user,
                        pass: pass,
                    },
                    success: function (data) {
                        console.log(data);
                        var table_itens = $("#body_table_itens");
                        var lines = table_itens.find("tr");

                        lines.each(function (j, line) {
                            var camps = $(line).find("td");
                            $.each(data, function (key, eq) {
                                let amount_input = eq.amount;

                                if (camps.eq(1).text() == "-") {
                                    var line_serial_number = camps.eq(4).text();
                                } else {
                                    var line_serial_number = camps.eq(1).text();
                                }

                                if (line_serial_number == key) {
                                    if (
                                        parseInt(camps.eq(5).text()) >
                                        amount_input
                                    ) {
                                        var ultimaLinha = $(line).clone(true);
                                        camps.eq(5).text(amount_input);

                                        ultimaLinha
                                            .find("td")
                                            .eq(5)
                                            .html(
                                                parseInt(
                                                    ultimaLinha
                                                        .find("td")
                                                        .eq(5)
                                                        .text()
                                                ) - amount_input
                                            );

                                        table_itens.append(ultimaLinha);
                                        updateRowNumbers(false);
                                    }

                                    list_returned_equipment.push(
                                        square_equipment
                                    );

                                    camps.eq(8).html(done_svg);

                                    interval = setInterval(
                                        fetchUnvalibleEquipmentData,
                                        1000
                                    );
                                }

                                console.log(eq);
                            });
                            console.log(line);
                        });
                    },
                });
            });
        },
    });
}

$(document).ready(function () {
    $("#search-btn").on("click", search);
});

function search() {
    var search = $("#search-camp");
    fetchUnvalibleEquipmentData(search.val(), "search");
    search.val("");
}

interval = setInterval(fetchUnvalibleEquipmentData, 1000);

function fetchUnvalibleEquipmentData(serial_number, type = "none") {
    let url = "/equipamento/get_indisponivel/" + id_cargo + "/";

    if (!(serial_number == null || serial_number == undefined)) {
        if (/^[0-9]+$/.test(serial_number)) {
            console.log("Equipaamento");
            url =
                "/equipamento/get_indisponivel/" +
                id_cargo +
                "/?type=equipment&pk=" +
                serial_number;
        } else if (serial_number.includes("ac")) {
            console.log("Acessório");
            url =
                "/equipamento/get_indisponivel/" +
                id_cargo +
                "/?type=equipment&pk=" +
                serial_number;
        } else {
            console.log("Munição");
            url =
                "/equipamento/get_indisponivel/" +
                id_cargo +
                "/?type=bullet&pk=" +
                serial_number;
        }
    }

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function (data) {
            if (data.uid !== "") {
                $.each(list_equipment, function (i, equipment) {
                    serial_number = equipment.equipment["serial_number"];
                    caliber = equipment.equipment["caliber"];

                    if (
                        serial_number != undefined &&
                        serial_number === data.equipment.serial_number
                    ) {
                        addToSquare(data);
                        square_equipment = data;
                        if (type != "search") {
                            check_cargo_square(type);
                        }
                        return false;
                    } else if (
                        caliber != undefined &&
                        caliber === data.equipment.caliber
                    ) {
                        addToSquare(data);
                        square_equipment = data;
                        if (type != "search") {
                            check_cargo_square(type);
                        }
                        return false;
                    }
                });
            } else if (data.confirmCargo) {
                $("#submit_btn")
                    .prop("disabled", false)
                    .removeClass("btn_disabled")
                    .addClass("btn_confirm");
            }
            if ("msm" in data) {
                popUp(data.msm);
            }
        },
        error: function (error) {
            console.error("Erro ao buscar dados do equipamento:", error);
        },
    });
}

function fetchEquipmentData(serial_number, type = "none") {
    let url =
        serial_number == null || serial_number == undefined
            ? "/equipamento/get_disponivel"
            : "/equipamento/get/" + serial_number;

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function (data) {
            if (data.uid !== "") {
                if (
                    data.equipment.serial_number != null &&
                    data.equipment.serial_number != undefined
                ) {
                    let equipAlreadyInList = list_equipment.find(function (
                        equipment
                    ) {
                        return (
                            equipment.equipment.serial_number ==
                            data.equipment.serial_number
                        );
                    });

                    if (equipAlreadyInList) {
                        popUp("Equipamento já na lista!");
                        return;
                    }
                }

                if (data.campo !== false) {
                    list_awate_equipment.push(data);
                    checkAwateList(type);
                }
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

function checkAwateList(type = "none") {
    if (list_awate_equipment.length > 0) {
        let equipmentData = list_awate_equipment.pop();
        addToSquare(equipmentData);
        if (type != "search") {
            check_cargo_square();
        }
        if (semaphore) {
            semaphore = false;
        }
    }
}

function check_cargo_square() {
    var observation = $("#note_equipment").val();
    var table_itens = $("#body_table_itens");
    var amount_input = $("#amount_input").val();
    var serialNumberInput = $("#serial_number").text();

    if (serialNumberInput == "-") {
        serialNumberValue = square_equipment["equipment"]["caliber"];
    } else {
        serialNumberValue = serialNumberInput;
    }

    var lines = table_itens.find("tr");

    lines.each(function (j, line) {
        var camps = $(line).find("td");
        var status = camps.eq(8).html();

        if (serialNumberInput == "-" && camps.eq(1).text() == "-") {
            var line_serial_number = camps.eq(4).text();
        } else {
            var line_serial_number = camps.eq(1).text();
        }

        if (line_serial_number == serialNumberValue && status !== done_svg) {
            if (parseInt(camps.eq(5).text()) > amount_input) {
                var ultimaLinha = $(line).clone(true);
                camps.eq(5).text(amount_input);

                ultimaLinha
                    .find("td")
                    .eq(5)
                    .html(
                        parseInt(ultimaLinha.find("td").eq(5).text()) -
                            amount_input
                    );

                table_itens.append(ultimaLinha);
                updateRowNumbers(false);
            }

            list_returned_equipment.push(square_equipment);

            camps.eq(8).html(done_svg);

            interval = setInterval(fetchUnvalibleEquipmentData, 1000);
            // Adicionar ao array de equipamentos do Django

            var serialNumber =
                square_equipment.equipment["serial_number"] ??
                square_equipment.equipment["caliber"] ??
                "";

            // Realizar solicitação Ajax
            $.ajax({
                url: "/carga/lista_equipamentos/add/",
                type: "POST",
                dataType: "json",
                data: {
                    serialNumber: serialNumber,
                    observation: observation,
                    amount: amount_input,
                    user: user,
                    pass: pass,
                },
                success: function (data) {
                    clearSquare();
                    square_equipment = null;
                },
                error: function (error) {
                    console.error(error);
                },
            });
            return false;
        }
    });
}

// checa se a lista tá vazia
function confirmCargo() {
    console.log(list_returned_equipment);
    if (list_returned_equipment.length > 0)
        document.getElementById("form-equipment").submit();
    // se tiver certo redireciona pra confirmar a carga
    else popUp("Lista vazia!");
}
