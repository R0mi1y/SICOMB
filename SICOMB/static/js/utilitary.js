function popUp(message, options = {}) {
    const defaultOptions = {
        closeBtn: true,
        yn: false,
        adicional: '',
        timer: null,
        yesFunction: false,
        noFunction: false,
        overlay: true,
    };

    const settings = { ...defaultOptions, ...options };
    const overlay = document.createElement('a');
    if (settings.overlay) {
        overlay.classList.add('popup-overlay');
    }
    
    const popUpElement = document.createElement('div');
    popUpElement.style.opacity = '0';
    popUpElement.classList.add('popup');

    if (settings.closeBtn) {
        const closeButton = document.createElement('button');
        closeButton.textContent = 'x';
        closeButton.classList = 'close-button';
        closeButton.addEventListener('click', () => {
            if (settings.overlay) document.body.removeChild(overlay);
            else document.getElementById("messages").removeChild(popUpElement);
        });
        popUpElement.appendChild(closeButton);
        
        // if (settings.overlay) {
        //     overlay.addEventListener('click', () => {
        //         document.body.removeChild(overlay);
        //     });
        // }
    }

    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    popUpElement.appendChild(messageElement);

    if (settings.adicional) {
        popUpElement.insertAdjacentHTML('beforeend', settings.adicional);
    }

    if (settings.yn) {
        const yesButton = document.createElement('button');
        yesButton.textContent = "SIM";
        yesButton.classList.add('popup-button', 'green');
        yesButton.addEventListener('click', () => {
            if (settings.overlay) document.body.removeChild(overlay);
            else document.getElementById("messages").removeChild(popUpElement);
            settings.yesFunction();
        });

        const noButton = document.createElement('button');
        noButton.textContent = "NÃO";
        noButton.classList.add('popup-button', 'red');
        noButton.addEventListener('click', () => {
            if (settings.overlay) document.body.removeChild(overlay);
            else document.getElementById("messages").removeChild(popUpElement);
            settings.noFunction();
        });

        popUpElement.appendChild(yesButton);
        popUpElement.appendChild(noButton);
    }

    if (settings.overlay) {
        overlay.appendChild(popUpElement);
        document.body.appendChild(overlay);
    }
    else document.getElementById("messages").appendChild(popUpElement);

    setTimeout(() => {
        if (settings.overlay) {
            overlay.style.opacity = '1'; // Torna o pop-up visível
            popUpElement.style.opacity = '1';
        } else popUpElement.style.opacity = '1';
        
    }, 10);

    if (settings.timer) {
        setTimeout(() => {
            if (settings.overlay) document.body.removeChild(overlay);
            else document.getElementById("messages").removeChild(popUpElement);
        }, settings.timer);
    }

    return overlay;
}

// Função para alternar a visibilidade do menu
function toggleMenu() {
    var menu = document.getElementById('menu');
    if (menu.style.opacity === '1') {
        menu.style.opacity = '0';
        menu.style.pointerEvents = 'none'; // Impede interações com o menu oculto
    } else {
        menu.style.opacity = '1';
        menu.style.pointerEvents = 'auto'; // Restaura interações com o menu visível
    }
}

function handleFileSelection(event) {
    const fileInput = event.target;
    const fileSelectedMessage = document.querySelector('#fileSelectedMessage');
    console.log(fileSelectedMessage);
    if (fileInput.files && fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileSelectedMessage.textContent = `Arquivo: ${fileName}`;
    } else {
        fileSelectedMessage.textContent = "Nenhum arquivo selecionado";
    }
}