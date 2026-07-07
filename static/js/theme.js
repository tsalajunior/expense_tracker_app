function setTheme(theme) {

    document.documentElement.setAttribute("data-theme", theme);

    localStorage.setItem("theme", theme);

}

document.addEventListener("DOMContentLoaded", () => {

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {

        document.documentElement.setAttribute("data-theme", savedTheme);

    }

    document.querySelectorAll("[data-theme-value]").forEach(item => {

        item.addEventListener("click", () => {

            setTheme(item.dataset.themeValue);

        });

    });

});