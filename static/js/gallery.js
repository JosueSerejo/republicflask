document.addEventListener("DOMContentLoaded", () => {
    const mainImg = document.getElementById("current-img");
    const thumbs = document.querySelectorAll(".thumbs img");

    thumbs.forEach((thumb) => {
        thumb.addEventListener("click", () => {
            const newSrc = thumb.getAttribute("src");
            mainImg.setAttribute("src", newSrc);
        });
    });
});
