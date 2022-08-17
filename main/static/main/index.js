async function votar(num) {
    console.log(num);
    console.log(await (await fetch('/votar?vote=' + num)).json());
}
function cadastro() {
    window.location.href = '/cadastro';
}
document.querySelector('main > button').addEventListener('click', cadastro);
const buttonsHtml = document.querySelectorAll('div > button');
buttons = [...buttonsHtml];
buttons.forEach((button) => {
    button.addEventListener('click', () => {
        votar(button.id);
    });
});
