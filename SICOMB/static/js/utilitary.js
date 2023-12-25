var popUp = function (message, options = {}) {
    console.log(message, options);
    const defaultOptions = {
        closeBtn: true,
        yn: false,
        adicional: "",
        timer: null,
        yesFunction: false,
        noFunction: false,
        overlay: true,
        textArea: false,
        contentTextarea: "",
    };

    const settings = { ...defaultOptions, ...options };

    const overlay = $("<a id='overlay'></a>");
    if (settings.overlay) {
        overlay.addClass("popup-overlay");
    }

    const popUpElement = $("<div></div>");
    popUpElement.css("opacity", "0");
    popUpElement.addClass("popup");

    if (settings.closeBtn) {
        const closeButton = $("<button>x</button>");
        closeButton.addClass("close-button");
        closeButton.on("click", () => {
            if (settings.overlay) overlay.remove();
            else {
                // Inicia a animação de saída diminuindo a opacidade
                popUpElement.css("opacity", "0");
    
                // Adiciona um atraso antes de remover o elemento do DOM
                setTimeout(() => {
                    popUpElement.remove();
                }, 300); // Ajuste conforme necessário
            }
        });
        popUpElement.append(closeButton);
    }

    const messageElement = $("<p></p>");
    messageElement.text(message);
    popUpElement.append(messageElement);

    if (settings.adicional) {
        popUpElement.append($(settings.adicional));
    }

    if (settings.yn) {
        const yesButton = $("<button>SIM</button>");
        yesButton.addClass("popup-button green");
        yesButton.on("click", () => {
            if (settings.overlay) overlay.remove();
            else {
                // Inicia a animação de saída diminuindo a opacidade
                popUpElement.css("opacity", "0");
    
                // Adiciona um atraso antes de remover o elemento do DOM
                setTimeout(() => {
                    popUpElement.remove();
                }, 300); // Ajuste conforme necessário
            }
            settings.yesFunction();
        });

        const noButton = $("<button>NÃO</button>");
        noButton.addClass("popup-button red");
        noButton.on("click", () => {
            if (settings.overlay) overlay.remove();
            else {
                // Inicia a animação de saída diminuindo a opacidade
                popUpElement.css("opacity", "0");
    
                // Adiciona um atraso antes de remover o elemento do DOM
                setTimeout(() => {
                    popUpElement.remove();
                }, 300); // Ajuste conforme necessário
            }
            settings.noFunction();
        });

        popUpElement.append(yesButton);
        popUpElement.append(noButton);
    }

    if (settings.overlay) {
        overlay.append(popUpElement);
        $("body").append(overlay);
    } else $("#messages").append(popUpElement);

    setTimeout(() => {
        if (settings.overlay) {
            overlay.css("opacity", "1");
            popUpElement.css("opacity", "1");
        } else popUpElement.css("opacity", "1");
    }, 10);

    
    if (settings.textArea) {
        const textArea = $("<textarea>" + settings.contentTextarea + "</textarea>");
        textArea.attr("rows", 10);
        textArea.attr("cols", 60);

        textArea.css("border", "solid 1px #685949");
        textArea.css("border-radius", "5px");
        textArea.css("background-color", "#efe5da");
        textArea.css("margin-top", "10px");
        textArea.css("padding", "10px");

        const button = $("<button>CONFIRMAR</button>");
        button.addClass("popup-button");
        button.css("background-color", "#685949");
        button.css("color", "#fff");
        button.on("click", () => {
            if (settings.overlay) overlay.remove();
            else {
                // Inicia a animação de saída diminuindo a opacidade
                popUpElement.css("opacity", "0");
    
                // Adiciona um atraso antes de remover o elemento do DOM
                setTimeout(() => {
                    popUpElement.remove();
                }, 300); // Ajuste conforme necessário
            }
            settings.function_textarea(settings.parm1, settings.parm2, textArea.val());
        });

        popUpElement.append(textArea);
        popUpElement.append(button);
        popUpElement.css("display", "grid");
    }

    if (settings.timer) {
        setTimeout(() => {
            if (settings.overlay) overlay.remove();
            else {
                // Inicia a animação de saída diminuindo a opacidade
                popUpElement.css("opacity", "0");
    
                // Adiciona um atraso antes de remover o elemento do DOM
                setTimeout(() => {
                    popUpElement.remove();
                }, 300); // Ajuste conforme necessário
            }
        }, settings.timer);
    }

    setTimeout(() => {
        popUpElement.css("opacity", "1").addClass('show');
    }, 10);

    return {"overlay": overlay, "close_function": () => {
        if (settings.overlay) overlay.remove();
        else $("#messages").find(popUpElement).remove();
    }, "message": message};
}

// Função para alternar a visibilidade do menu
function toggleMenu() {
    var menu = document.getElementById("menu");
    if (menu.style.opacity === "1") {
        menu.style.opacity = "0";
        menu.style.pointerEvents = "none"; // Impede interações com o menu oculto
    } else {
        menu.style.opacity = "1";
        menu.style.pointerEvents = "auto"; // Restaura interações com o menu visível
    }
}

function handleFileSelection(event) {
    const fileInput = event.target;
    const fileSelectedMessage = document.querySelector("#fileSelectedMessage");
    console.log(fileSelectedMessage);
    if (fileInput.files && fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileSelectedMessage.textContent = `Arquivo: ${fileName}`;
    } else {
        fileSelectedMessage.textContent = "Nenhum arquivo selecionado";
    }
}