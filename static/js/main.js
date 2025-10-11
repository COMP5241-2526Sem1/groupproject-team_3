// Main JavaScript for Learning Activity Management System
// Handles client-side interactions and AJAX requests

// Utility function for making API calls
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// Mobile navigation toggle
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
            
            // Show error message
            let errorMsg = input.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('form-error')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'form-error';
                errorMsg.textContent = 'This field is required';
                input.parentNode.insertBefore(errorMsg, input.nextSibling);
            }
        } else {
            input.classList.remove('error');
            const errorMsg = input.nextElementSibling;
            if (errorMsg && errorMsg.classList.contains('form-error')) {
                errorMsg.remove();
            }
        }
    });
    
    return isValid;
}

// Loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    spinner.id = 'loading-spinner';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// Handle form submissions
async function handleFormSubmit(formId, url, method = 'POST') {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!validateForm(formId)) {
            showAlert('Please fill in all required fields', 'danger');
            return;
        }
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        showLoading();
        
        try {
            const result = await apiCall(url, method, data);
            hideLoading();
            
            if (result.success) {
                showAlert(result.message, 'success');
                
                // Redirect if URL provided
                if (result.redirect) {
                    setTimeout(() => {
                        window.location.href = result.redirect;
                    }, 1000);
                }
            } else {
                showAlert(result.message, 'danger');
            }
        } catch (error) {
            hideLoading();
            showAlert('An error occurred. Please try again.', 'danger');
        }
    });
}

// Activity link copy function
function copyActivityLink(link) {
    const fullLink = window.location.origin + '/a/' + link;
    
    navigator.clipboard.writeText(fullLink).then(() => {
        showAlert('Link copied to clipboard!', 'success');
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = fullLink;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showAlert('Link copied to clipboard!', 'success');
    });
}

// Export table to CSV
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename + '.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Confirm before delete
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search filter for tables
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    const debouncedSearch = debounce(() => {
        const filter = input.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
        });
    }, 300);
    
    input.addEventListener('input', debouncedSearch);
}

// Add option to list (for poll creation)
function addPollOption() {
    const container = document.getElementById('poll-options');
    if (!container) return;
    
    const optionCount = container.children.length + 1;
    const div = document.createElement('div');
    div.className = 'form-group';
    div.innerHTML = `
        <label class="form-label">Option ${optionCount}</label>
        <div class="flex gap-2">
            <input type="text" class="form-control poll-option" name="options[]" required>
            <button type="button" class="btn btn-danger btn-sm" onclick="this.parentElement.parentElement.remove()">
                Remove
            </button>
        </div>
    `;
    container.appendChild(div);
}

// Character counter for textarea
function setupCharCounter(textareaId, counterId, maxChars) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    
    if (!textarea || !counter) return;
    
    textarea.addEventListener('input', () => {
        const length = textarea.value.length;
        counter.textContent = `${length} / ${maxChars} characters`;
        
        if (length > maxChars) {
            counter.style.color = 'var(--danger-color)';
        } else {
            counter.style.color = 'var(--dark-text)';
        }
    });
}

// Initialize tooltips (if using tooltip library)
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = e.target.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = e.target.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
        });
        
        element.addEventListener('mouseleave', () => {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

// Export functions for global use
window.apiCall = apiCall;
window.showAlert = showAlert;
window.openModal = openModal;
window.closeModal = closeModal;
window.validateForm = validateForm;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.handleFormSubmit = handleFormSubmit;
window.copyActivityLink = copyActivityLink;
window.exportTableToCSV = exportTableToCSV;
window.confirmDelete = confirmDelete;
window.formatDate = formatDate;
window.filterTable = filterTable;
window.addPollOption = addPollOption;
window.setupCharCounter = setupCharCounter;
