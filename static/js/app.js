// =========================================
// SQL Agent - Frontend JavaScript
// =========================================

let currentSQL = "";

// =========================================
// INICIALIZACIÓN
// =========================================
document.addEventListener("DOMContentLoaded", () => {
    loadSuggestions();
    loadSchema();

    // Enviar con Enter + Ctrl
    document.getElementById("questionInput").addEventListener("keydown", (e) => {
        if (e.key === "Enter" && e.ctrlKey) {
            submitQuestion();
        }
    });
});

// =========================================
// CARGAR SUGERENCIAS
// =========================================
async function loadSuggestions() {
    try {
        const response = await fetch("/api/suggestions");
        const data = await response.json();
        
        const container = document.getElementById("suggestionsList");
        container.innerHTML = "";
        
        data.suggestions.forEach((suggestion) => {
            const item = document.createElement("div");
            item.className = "suggestion-item";
            item.innerHTML = `<i class="bi bi-chevron-right"></i><span>${suggestion}</span>`;
            item.onclick = () => {
                document.getElementById("questionInput").value = suggestion;
                document.getElementById("questionInput").focus();
            };
            container.appendChild(item);
        });
    } catch (error) {
        console.error("Error cargando sugerencias:", error);
    }
}

// =========================================
// CARGAR ESQUEMA
// =========================================
async function loadSchema() {
    try {
        const response = await fetch("/api/schema");
        const data = await response.json();
        
        if (data.success) {
            document.getElementById("schemaContent").textContent = data.schema;
        }
    } catch (error) {
        document.getElementById("schemaContent").textContent = "Error cargando el esquema.";
    }
}

// =========================================
// ENVIAR CONSULTA
// =========================================
async function submitQuestion() {
    const question = document.getElementById("questionInput").value.trim();
    
    if (!question) {
        shakeElement("questionInput");
        return;
    }

    // UI: mostrar loading
    setLoadingState(true);

    try {
        const response = await fetch("/api/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        });

        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            displayError(data.error);
        }
    } catch (error) {
        displayError("Error de conexión. Verifica que el servidor esté corriendo.");
    } finally {
        setLoadingState(false);
    }
}

// =========================================
// MOSTRAR RESULTADOS
// =========================================
function displayResults(data) {
    // Ocultar estados previos
    hideAllStates();
    
    // Mostrar contenedor de resultados
    document.getElementById("resultsContainer").classList.remove("d-none");
    
    // Interpretación
    document.getElementById("interpretationText").textContent = data.interpretation;
    
    // SQL generado
    currentSQL = data.sql;
    document.getElementById("sqlCode").textContent = data.sql;
    
    // Tabla de resultados
    if (data.data && data.data.rows.length > 0) {
        buildTable(data.data.columns, data.data.rows);
        document.getElementById("rowCount").textContent = 
            `${data.data.total_rows} resultado${data.data.total_rows !== 1 ? "s" : ""}`;
    } else {
        document.getElementById("tableBody").innerHTML = `
            <tr>
                <td colspan="100%" class="text-center text-muted py-4">
                    <i class="bi bi-inbox me-2"></i>No se encontraron resultados
                </td>
            </tr>
        `;
    }
}

// =========================================
// CONSTRUIR TABLA DINÁMICA
// =========================================
function buildTable(columns, rows) {
    // Headers
    const thead = document.getElementById("tableHead");
    thead.innerHTML = `
        <tr>
            ${columns.map(col => `<th>${formatColumnName(col)}</th>`).join("")}
        </tr>
    `;
    
    // Rows
    const tbody = document.getElementById("tableBody");
    tbody.innerHTML = rows.map(row => `
        <tr>
            ${row.map(cell => `<td>${formatCellValue(cell)}</td>`).join("")}
        </tr>
    `).join("");
}

// =========================================
// FORMATEAR VALORES
// =========================================
function formatColumnName(col) {
    return col
        .replace(/_/g, " ")
        .replace(/\b\w/g, l => l.toUpperCase());
}

function formatCellValue(value) {
    if (value === null || value === undefined) return '<span class="text-muted">—</span>';
    
    // Detectar números grandes (salarios/montos)
    if (typeof value === "number" && value > 10000) {
        return `<span class="text-success">$${value.toLocaleString("es-CO")}</span>`;
    }
    
    // Booleanos
    if (typeof value === "boolean") {
        return value 
            ? '<span class="badge bg-success">Sí</span>' 
            : '<span class="badge bg-danger">No</span>';
    }
    
    // Fechas
    if (typeof value === "string" && value.match(/^\d{4}-\d{2}-\d{2}/)) {
        return new Date(value).toLocaleDateString("es-CO", {
            year: "numeric", month: "short", day: "numeric"
        });
    }
    
    return value;
}

// =========================================
// MOSTRAR ERROR
// =========================================
function displayError(message) {
    hideAllStates();
    document.getElementById("errorState").classList.remove("d-none");
    document.getElementById("errorMessage").textContent = message;
}

// =========================================
// ESTADOS UI
// =========================================
function setLoadingState(loading) {
    const btn = document.getElementById("submitBtn");
    const btnText = document.getElementById("btnText");
    const spinner = document.getElementById("btnSpinner");
    
    if (loading) {
        btn.disabled = true;
        btnText.textContent = "Procesando...";
        spinner.classList.remove("d-none");
        hideAllStates();
        document.getElementById("loadingState").classList.remove("d-none");
    } else {
        btn.disabled = false;
        btnText.textContent = "Consultar Base de Datos";
        spinner.classList.add("d-none");
        document.getElementById("loadingState").classList.add("d-none");
    }
}

function hideAllStates() {
    document.getElementById("emptyState").classList.add("d-none");
    document.getElementById("loadingState").classList.add("d-none");
    document.getElementById("resultsContainer").classList.add("d-none");
    document.getElementById("errorState").classList.add("d-none");
}

// =========================================
// COPIAR SQL
// =========================================
function copySQL() {
    navigator.clipboard.writeText(currentSQL).then(() => {
        const btn = event.target.closest("button");
        const original = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check me-1"></i>¡Copiado!';
        btn.classList.add("btn-success");
        btn.classList.remove("btn-outline-secondary");
        setTimeout(() => {
            btn.innerHTML = original;
            btn.classList.remove("btn-success");
            btn.classList.add("btn-outline-secondary");
        }, 2000);
    });
}

// =========================================
// ANIMACIÓN DE SHAKE
// =========================================
function shakeElement(elementId) {
    const el = document.getElementById(elementId);
    el.style.animation = "none";
    el.offsetHeight; // reflow
    el.style.animation = "shake 0.4s ease";
    el.style.borderColor = "var(--accent-orange) !important";
    setTimeout(() => {
        el.style.animation = "";
        el.style.borderColor = "";
    }, 600);
}

// CSS de shake dinámico
const style = document.createElement("style");
style.textContent = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-8px); }
    40% { transform: translateX(8px); }
    60% { transform: translateX(-4px); }
    80% { transform: translateX(4px); }
}
`;
document.head.appendChild(style);