async function votar(num, rm) {
    createPopUp(await (await fetch('/votar?vote=' + num + '&rm=' + rm)).text());
}
function cadastro() {
    window.location.href = '/cadastro';
}
function createPopUp(msg) {
    const popUp = document.createElement('div');
    popUp.className = 'popUp';
    popUp.innerHTML = msg;
    document.body.appendChild(popUp);
    setTimeout(() => {
        popUp.remove();
    }, 2000);
}
function pedirRm(voto) {
    const rm = prompt('Digite seu RM');
    if (rm != null) {
        votar(voto, rm);
    }
}
document.querySelector('main > button').addEventListener('click', cadastro);
const buttonsHtml = document.querySelectorAll('div > button');
buttons = [...buttonsHtml];
buttons.forEach((button) => {
    button.addEventListener('click', () => {
        pedirRm(button.id);
    });
});
