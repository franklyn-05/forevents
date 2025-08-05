document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("artistFilter").addEventListener("change", applyFilters);
    document.getElementById("cityFilter").addEventListener("change", applyFilters);
    applyFilters();
});

function applyFilters(){
    const artist = document.getElementById("artistFilter").value;
    const city = document.getElementById("cityFilter").value;
    const items = document.getElementsByClassName("filterDiv");

    for (let i = 0; i < items.length; i++) {
        const matchesArtist = (artist === "all" || items[i].classList.contains(artist));
        const matchesCity = (city === "all" || items[i].classList.contains(city));

        if (matchesArtist && matchesCity) {
            items[i].classList.add("show");
        } else {
            items[i].classList.remove("show")
        }
    }
}