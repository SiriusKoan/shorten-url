function hide(obj) {
    obj.style.opacity = "0";
    setTimeout(() => {
        obj.style.display = "none";
    }, 300);
}