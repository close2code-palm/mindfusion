let tg = window.Telegram.WebApp;

let images = document.getElementsByTagName('img');
console.log(images);
console.dir(images);
[...images].forEach(element => {
    element.addEventListener('click', function(){
        console.log(element.id);
        tg.sendData(element.id);
    })
});