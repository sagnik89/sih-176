document.addEventListener("DOMContentLoaded", () => {

    initializeApplication();

});


async function initializeApplication() {

    setupQueryInput();
    setupExampleQueries();

    resetAgents();

    try {

        const health = await checkHealth();

        setQueryStatus(
            `ORCA ONLINE · ${health.records || 0} RECORDS LOADED`
        );

        const locations = await getLocations();

        initializeRegions(
            locations.locations || []
        );

    } catch (error) {

        console.error("ORCA initialization failed:", error);

        setQueryStatus(
            "ORCA API CONNECTION FAILED",
            false
        );

    }
}


function setupQueryInput() {

    const input =
        document.getElementById("query-input");

    const button =
        document.getElementById("query-button");

    if (!input || !button) {
        return;
    }


    button.addEventListener(
        "click",
        handleQuery
    );


    input.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter" &&
                (event.ctrlKey || event.metaKey)
            ) {
                event.preventDefault();

                handleQuery();
            }

        }
    );

}


function setupExampleQueries() {

    document
        .querySelectorAll(".example-query")
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const input =
                        document.getElementById(
                            "query-input"
                        );

                    if (!input) {
                        return;
                    }

                    input.value =
                        button.textContent.trim();

                    input.focus();

                }
            );

        });

}


async function handleQuery() {

    const input =
        document.getElementById("query-input");

    const button =
        document.getElementById("query-button");

    if (!input || !button) {
        return;
    }

    const query =
        input.value.trim();


    if (!query) {

        setQueryStatus(
            "ENTER A QUESTION TO BEGIN",
            false
        );

        input.focus();

        return;
    }


    button.disabled = true;

    button.innerHTML = `
        <span>ANALYZING...</span>
        <span class="button-arrow">◌</span>
    `;


    setQueryStatus(
        "ORCA AGENTS ARE ANALYZING THE QUERY",
        true
    );


    resetAgents();

    showLoadingState();


    try {

        /*
         * Start visual agent activity while the
         * backend performs the actual analysis.
         */
        const agentAnimation =
            animateAgents();


        const result =
            await runQuery(query);


        await agentAnimation;


        if (!result.success) {
            throw new Error(
                result.error ||
                "ORCA analysis failed."
            );
        }


        displayResult(result);


        setQueryStatus(
            "ANALYSIS COMPLETE · EVIDENCE FUSED",
            true
        );


        setAgentStatus("COMPLETE");


        scrollToResults();

    } catch (error) {

        console.error(
            "ORCA query failed:",
            error
        );


        showError(
            error.message ||
            "Unable to complete the analysis."
        );


        setQueryStatus(
            "ANALYSIS FAILED",
            false
        );


        setAgentStatus("ERROR");

    } finally {

        button.disabled = false;

        button.innerHTML = `
            <span>RUN ANALYSIS</span>
            <span class="button-arrow">→</span>
        `;

    }

}


function showError(message) {

    const emptyResult =
        document.getElementById("empty-result");

    const resultContainer =
        document.getElementById(
            "result-container"
        );


    if (emptyResult) {
        emptyResult.classList.add("hidden");
    }


    if (!resultContainer) {
        return;
    }


    resultContainer.classList.remove("hidden");


    resultContainer.innerHTML = `
        <div class="empty-result">

            <div class="empty-orbit">
                <span>!</span>
            </div>

            <h3>
                Analysis unavailable
            </h3>

            <p>
                ${escapeHtml(message)}
            </p>

        </div>
    `;

}


function scrollToResults() {

    const results =
        document.querySelector(
            ".results-section"
        );

    if (!results) {
        return;
    }


    setTimeout(() => {

        results.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }, 100);

}