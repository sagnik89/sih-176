let orcaLocations = [];


function initializeRegions(locations = []) {
    orcaLocations = locations;

    const regionList = document.getElementById("region-list");
    const locationCount = document.getElementById("location-count");

    if (!regionList) {
        return;
    }

    if (!locations.length) {
        regionList.innerHTML = `
            <div class="region-item">
                <div class="region-info">
                    <strong>No regions available</strong>
                    <span>ORCA API returned no locations</span>
                </div>
            </div>
        `;

        if (locationCount) {
            locationCount.textContent = "0 REGIONS";
        }

        return;
    }

    if (locationCount) {
        locationCount.textContent =
            `${locations.length} REGIONS`;
    }

    regionList.innerHTML = "";

    locations.forEach((location, index) => {

        const item = document.createElement("div");

        item.className = "region-item";

        item.dataset.region = location.region;

        item.innerHTML = `
            <div class="region-number">
                ${String(index + 1).padStart(2, "0")}
            </div>

            <div class="region-info">
                <strong>${escapeHtml(location.region)}</strong>

                <span>
                    ${Number(location.latitude).toFixed(2)}°,
                    ${Number(location.longitude).toFixed(2)}°
                </span>
            </div>

            <div class="region-indicator"></div>
        `;

        item.addEventListener("click", () => {
            selectRegion(location.region);
        });

        regionList.appendChild(item);
    });
}


function selectRegion(region) {

    const input = document.getElementById("query-input");

    if (!input) {
        return;
    }

    input.value =
        `Analyze the marine ecosystem conditions in ${region}.`;

    document.querySelectorAll(".region-item").forEach(item => {
        item.classList.remove("selected");

        if (
            item.dataset.region &&
            item.dataset.region.toLowerCase() ===
            region.toLowerCase()
        ) {
            item.classList.add("selected");
        }
    });

    input.focus();
}


function getSelectedRegion() {

    const input = document.getElementById("query-input");

    if (!input) {
        return null;
    }

    const text = input.value.toLowerCase();

    const match = orcaLocations.find(location =>
        text.includes(
            String(location.region).toLowerCase()
        )
    );

    return match ? match.region : null;
}


function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}