setTimeout(function () {
    let ix = 0;
    for (let el of document.getElementsByClassName("flashed-message")) {
        setTimeout(() => {
            el.style.display = "none";
        }, ix * 500);
        ix += 1;
    }
}, 5000);