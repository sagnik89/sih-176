function setQueryStatus(message, active = false) {
    const status = document.getElementById("query-status");

    if (!status) {
        return;
    }

    status.innerHTML = `
        <span class="status-dot"></span>
        ${escapeHtml(message)}
    `;

    status.classList.toggle("active", active);
}


function setAgentStatus(status) {
    const agentStatus = document.getElementById("agent-status");

    if (agentStatus) {
        agentStatus.textContent = status;
    }
}


function setAgentState(agentName, state) {

    const ids = {
        MarineAgent: "agent-marine",
        WeatherAgent: "agent-weather",
        SatelliteAgent: "agent-satellite",
        EcologyAgent: "agent-ecology",
        ReasoningAgent: "agent-reasoning"
    };

    const element = document.getElementById(
        ids[agentName]
    );

    if (!element) {
        return;
    }

    const stateElement =
        element.querySelector(".agent-state");

    const indicator =
        element.querySelector(".agent-state i");

    element.classList.remove(
        "active",
        "complete"
    );

    if (state === "active") {

        element.classList.add("active");

        if (stateElement) {
            stateElement.innerHTML = `
                <i></i>
                ANALYZING
            `;
        }

    } else if (state === "complete") {

        element.classList.add("complete");

        if (stateElement) {
            stateElement.innerHTML = `
                <i></i>
                COMPLETE
            `;
        }

    } else {

        if (stateElement) {
            stateElement.innerHTML = `
                <i></i>
                READY
            `;
        }
    }

    if (indicator) {
        indicator.style.animation =
            state === "active"
                ? "pulse 1s infinite"
                : "none";
    }
}


function resetAgents() {

    const agents = [
        "MarineAgent",
        "WeatherAgent",
        "SatelliteAgent",
        "EcologyAgent",
        "ReasoningAgent"
    ];

    agents.forEach(agent => {
        setAgentState(agent, "ready");
    });

    setAgentStatus("STANDBY");
}


async function animateAgents() {

    const agents = [
        "MarineAgent",
        "WeatherAgent",
        "SatelliteAgent",
        "EcologyAgent",
        "ReasoningAgent"
    ];

    setAgentStatus("PROCESSING");

    for (const agent of agents) {

        setAgentState(agent, "active");

        await sleep(350);

        setAgentState(agent, "complete");
    }

    setAgentStatus("COMPLETE");
}


function showLoadingState() {

    const emptyResult =
        document.getElementById("empty-result");

    const resultContainer =
        document.getElementById("result-container");

    if (emptyResult) {
        emptyResult.classList.add("hidden");
    }

    if (resultContainer) {
        resultContainer.classList.remove("hidden");

        resultContainer.innerHTML = `
            <div class="empty-result">
                <div class="empty-orbit">
                    <span>O</span>
                </div>

                <h3>ORCA is reasoning...</h3>

                <p>
                    Specialized agents are analyzing
                    the available environmental evidence.
                </p>
            </div>
        `;
    }
}


function displayResult(result) {

    const emptyResult =
        document.getElementById("empty-result");

    const resultContainer =
        document.getElementById("result-container");

    if (!resultContainer) {
        return;
    }

    if (emptyResult) {
        emptyResult.classList.add("hidden");
    }

    resultContainer.classList.remove("hidden");

    const risk =
        result.risk || {};

    const riskLevel =
        String(
            risk.level || "UNKNOWN"
        ).toUpperCase();

    const riskScore =
        Number(
            risk.score || 0
        );

    resultContainer.innerHTML = `
        <div class="result-grid">

            <div class="answer-card">

                <span class="section-tag">
                    ORCA ASSESSMENT
                </span>

                <h4>Environmental Intelligence</h4>

                <p id="result-answer">
                    ${escapeHtml(
                        result.answer ||
                        "No assessment was generated."
                    )}
                </p>

            </div>


            <div class="risk-card">

                <span class="section-tag">
                    ECOLOGICAL RISK
                </span>

                <div
                    id="risk-level"
                    class="risk-level ${getRiskClass(riskLevel)}"
                >
                    ${escapeHtml(riskLevel)}
                </div>

                <div class="risk-meter">
                    <div
                        id="risk-meter-fill"
                        class="${getRiskClass(riskLevel)}"
                        style="width: ${Math.min(
                            Math.max(riskScore * 100, 0),
                            100
                        )}%"
                    ></div>
                </div>

                <div class="risk-score">

                    <span>RISK SCORE</span>

                    <strong id="risk-score">
                        ${riskScore.toFixed(2)}
                    </strong>

                </div>

            </div>

        </div>


        <div class="report-card">

            <div class="card-title">
                <span class="section-tag">
                    KEY FINDINGS
                </span>
            </div>

            <ul id="findings-list">
                ${renderFindings(
                    result.findings || []
                )}
            </ul>

        </div>


        <div class="report-card">

            <div class="card-title">
                <span class="section-tag">
                    EVIDENCE TRAIL
                </span>
            </div>

            <div id="evidence-list">
                ${renderEvidence(
                    result.evidence || []
                )}
            </div>

        </div>


        <div class="result-footer">

            <span>
                AGENTS
                <strong>
                    ${escapeHtml(
                        (result.agents_used || [])
                            .join(" · ")
                    )}
                </strong>
            </span>

            <span>
                MODEL
                <strong>
                    ${escapeHtml(
                        result.model_used ||
                        "Deterministic fallback"
                    )}
                </strong>
            </span>

            <span>
                DATA MODE
                <strong>
                    SYNTHETIC DEMO
                </strong>
            </span>

        </div>
    `;
}


function renderFindings(findings) {

    if (!findings.length) {
        return `
            <li>
                No specific findings were returned.
            </li>
        `;
    }

    return findings
        .slice(0, 10)
        .map(
            finding => `
                <li>
                    ${escapeHtml(finding)}
                </li>
            `
        )
        .join("");
}


function renderEvidence(evidence) {

    if (!evidence.length) {
        return `
            <div class="evidence-item">
                <strong>No evidence available</strong>
                <span>
                    The analysis returned no evidence records.
                </span>
            </div>
        `;
    }

    return evidence
        .map(item => {

            const agent =
                item.agent || "Unknown Agent";

            const findings =
                item.findings || [];

            const metrics =
                item.metrics || {};

            const metricText =
                Object.entries(metrics)
                    .slice(0, 4)
                    .map(
                        ([key, value]) =>
                            `${formatMetricName(key)}: ${formatMetricValue(value)}`
                    )
                    .join(" · ");

            return `
                <div class="evidence-item">

                    <strong>
                        ${escapeHtml(agent)}
                    </strong>

                    <span>
                        ${escapeHtml(
                            findings[0] ||
                            metricText ||
                            "Evidence collected successfully."
                        )}
                    </span>

                    ${
                        metricText
                            ? `
                                <span>
                                    ${escapeHtml(metricText)}
                                </span>
                            `
                            : ""
                    }

                </div>
            `;
        })
        .join("");
}


function getRiskClass(level) {

    switch (level) {

        case "HIGH":
            return "risk-high";

        case "MODERATE":
            return "risk-moderate";

        case "LOW":
            return "risk-low";

        default:
            return "risk-unknown";
    }
}


function formatMetricName(name) {

    return String(name)
        .replace(/_/g, " ")
        .replace(/\b\w/g, char =>
            char.toUpperCase()
        );
}


function formatMetricValue(value) {

    if (typeof value === "number") {
        return value.toFixed(2);
    }

    return String(value);
}


function sleep(milliseconds) {

    return new Promise(resolve =>
        setTimeout(resolve, milliseconds)
    );
}


function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}