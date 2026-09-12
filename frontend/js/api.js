const API_BASE_URL = "http://127.0.0.1:5000/api";


async function apiRequest(endpoint, options = {}) {
    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            },
            ...options
        }
    );

    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error(
            `Invalid response from ORCA API (${response.status}).`
        );
    }

    if (!response.ok) {
        throw new Error(
            data.error ||
            `ORCA API request failed (${response.status}).`
        );
    }

    return data;
}


async function checkHealth() {
    return apiRequest("/health");
}
 
  
async function getLocations() {
    return apiRequest("/locations");
}


async function runQuery(query) {
    return apiRequest(
        "/query",
        {
            method: "POST",
            body: JSON.stringify({
                query: query
            })
        }
    );
}


async function getLocation(region) {
    return apiRequest(
        `/location/${encodeURIComponent(region)}`
    );
}


async function getCapabilities() {
    return apiRequest("/capabilities");
}