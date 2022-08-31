async function votar(num, rm) {
    createPopUp(await (await fetch('/votar?vote=' + num + '&rm=' + rm)).text());
}
function cadastro() {
    window.location.href = '/cadastro';
}
function createPopUp(msg, time = 2000) {
    const popUp = document.createElement('div');
    popUp.className = 'popUp';
    popUp.innerHTML = msg;
    document.body.appendChild(popUp);
    setTimeout(() => {
        popUp.remove();
    }, time);
}
function pedirRm(voto) {
    if (rmInput.value) votar(voto, rmInput.value);
    else createPopUp('Preencha o campo Codigo', 1500);
    rmInput.value = '';
}
function encerrar() {
    confirm('Deseja encerrar o voto?')
        ? (window.location.href = '/encerrar')
        : null;
}
const rmInput = document.querySelector('input');
document.querySelector('#cadastrar').addEventListener('click', cadastro);
document.querySelector('#encerrar').addEventListener('click', encerrar);
const buttonsHtml = document.querySelectorAll('div > button');
buttons = [...buttonsHtml];
buttons.forEach((button) => {
    button.addEventListener('click', () => {
        pedirRm(button.id);
    });
});
