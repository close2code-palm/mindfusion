const send_char = e => {
    console.log(e.id);
    window.Telegram.WebApp.sendData(e.id);
}