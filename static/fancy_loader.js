window.addEventListener("load", function() {
    const startTime = Date.now();
    const minWait = 800;

    const hideLoader = () => {
        const loader = document.getElementById("loader");
        loader.style.transition = "opacity 0.4s";
        loader.style.opacity = "0";
        setTimeout(() => loader.style.display = "none", 400);
    };

    const elapsed = Date.now() - startTime;
    
    if (elapsed < minWait) {
        setTimeout(hideLoader, minWait - elapsed);
    } else {
        hideLoader();
    }
});