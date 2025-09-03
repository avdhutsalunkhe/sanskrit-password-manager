// Password Manager Main JavaScript

let currentPassword = '';
let modalTimeout;

// Show password in modal
function showPassword(passwordId) {
    const button = event.target.closest('button');
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Loading...';
    
    fetch(`/api/get-password/${passwordId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentPassword = data.password;
                document.getElementById('revealedPassword').textContent = data.password;
                document.getElementById('passwordModal').classList.remove('hidden');
                
                // Auto-close after 30 seconds for security
                modalTimeout = setTimeout(() => {
                    closePasswordModal();
                    showAlert('Password hidden for security', 'info');
                }, 30000);
                
                // Focus on copy button for accessibility
                setTimeout(() => {
                    document.querySelector('#passwordModal [onclick="copyRevealedPassword()"]').focus();
                }, 100);
            } else {
                showAlert(data.error || 'Failed to retrieve password', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Network error occurred', 'error');
        })
        .finally(() => {
            // Reset button
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-eye mr-2"></i>Show Password';
        });
}

// Copy password directly to clipboard
function copyPassword(passwordId) {
    const button = event.target.closest('button');
    const originalContent = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Copying...';
    
    fetch(`/api/get-password/${passwordId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                return navigator.clipboard.writeText(data.password);
            } else {
                throw new Error(data.error || 'Failed to retrieve password');
            }
        })
        .then(() => {
            button.innerHTML = '<i class="fas fa-check mr-2"></i>Copied!';
            button.classList.add('bg-green-600', 'text-white');
            showAlert('Password copied to clipboard!', 'success');
            
            // Reset button appearance after 2 seconds
            setTimeout(() => {
                button.innerHTML = originalContent;
                button.classList.remove('bg-green-600', 'text-white');
            }, 2000);
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert(error.message || 'Failed to copy password', 'error');
        })
        .finally(() => {
            button.disabled = false;
        });
}

// Delete password with confirmation
function deletePassword(passwordId) {
    const button = event.target.closest('button');
    
    // Create custom confirmation modal for better UX
    const confirmed = confirm(
        '⚠️ Delete Password?\n\n' +
        'This action cannot be undone. The password will be permanently deleted from your vault.\n\n' +
        'Are you sure you want to continue?'
    );
    
    if (!confirmed) return;
    
    const originalContent = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Deleting...';
    
    fetch(`/api/delete-password/${passwordId}`, { 
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Animate removal
                const passwordCard = button.closest('.card-hover') || button.closest('[class*="bg-white"]');
                if (passwordCard) {
                    passwordCard.style.transform = 'scale(0.95)';
                    passwordCard.style.opacity = '0.5';
                    passwordCard.style.transition = 'all 0.3s ease';
                    
                    setTimeout(() => {
                        passwordCard.remove();
                        showAlert('Password deleted successfully', 'success');
                        
                        // Update password count if display exists
                        const countBadge = document.querySelector('[class*="bg-red-100"]');
                        if (countBadge) {
                            const currentCount = parseInt(countBadge.textContent);
                            countBadge.textContent = `${currentCount - 1} Total`;
                        }
                        
                        // Show empty state if no passwords left
                        const remainingCards = document.querySelectorAll('.card-hover, [class*="bg-white"]').length;
                        if (remainingCards <= 1) {
                            location.reload(); // Reload to show empty state
                        }
                    }, 300);
                }
            } else {
                throw new Error(data.error || 'Failed to delete password');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert(error.message || 'Failed to delete password', 'error');
            button.innerHTML = originalContent;
            button.disabled = false;
        });
}

// Copy password from modal
function copyRevealedPassword() {
    if (!currentPassword) {
        showAlert('No password to copy', 'error');
        return;
    }
    
    navigator.clipboard.writeText(currentPassword)
        .then(() => {
            showAlert('Password copied to clipboard!', 'success');
            closePasswordModal();
        })
        .catch(() => {
            showAlert('Failed to copy password', 'error');
        });
}

// Close password modal
function closePasswordModal() {
    document.getElementById('passwordModal').classList.add('hidden');
    currentPassword = '';
    if (modalTimeout) {
        clearTimeout(modalTimeout);
    }
}

// Enhanced alert system
function showAlert(message, type) {
    // Remove existing alerts
    document.querySelectorAll('.alert-notification').forEach(alert => alert.remove());
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-notification fixed top-20 right-4 z-50 p-4 rounded-lg shadow-lg animate-fade-in max-w-sm ${getAlertClasses(type)}`;
    
    alertDiv.innerHTML = `
        <div class="flex items-start">
            <i class="fas fa-${getAlertIcon(type)} mr-3 mt-0.5 flex-shrink-0" aria-hidden="true"></i>
            <div class="flex-1">
                <div class="font-medium">${message}</div>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" 
                    class="ml-2 text-current opacity-70 hover:opacity-100" 
                    aria-label="Close notification">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.style.opacity = '0';
            alertDiv.style.transform = 'translateX(100%)';
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, 5000);
}

function getAlertClasses(type) {
    const classes = {
        'error': 'bg-red-100 border border-red-300 text-red-700',
        'success': 'bg-green-100 border border-green-300 text-green-700',
        'warning': 'bg-yellow-100 border border-yellow-300 text-yellow-700',
        'info': 'bg-blue-100 border border-blue-300 text-blue-700'
    };
    return classes[type] || classes['info'];
}

function getAlertIcon(type) {
    const icons = {
        'error': 'exclamation-circle',
        'success': 'check-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || icons['info'];
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // ESC key closes modal
    if (event.key === 'Escape') {
        const modal = document.getElementById('passwordModal');
        if (modal && !modal.classList.contains('hidden')) {
            closePasswordModal();
        }
    }
});

// Click outside modal to close
document.getElementById('passwordModal')?.addEventListener('click', function(event) {
    if (event.target === this) {
        closePasswordModal();
    }
});

// Initialize tooltips on page load
document.addEventListener('DOMContentLoaded', function() {
    // Simple tooltip implementation
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip fixed bg-gray-900 text-white text-sm px-2 py-1 rounded z-50 pointer-events-none';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
            tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
        });
        
        element.addEventListener('mouseleave', function() {
            document.querySelectorAll('.tooltip').forEach(tooltip => tooltip.remove());
        });
    });
});

// --- Existing functionality below ---

function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    
    // Clear previous errors
    clearFieldError(event);
    
    // Validation rules
    if (field.required && !value) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }
    
    if (field.name === 'password' && value) {
        if (value.length < 8) {
            showFieldError(field, 'Password must be at least 8 characters long');
            return false;
        }
    }
    
    return true;
}

function showFieldError(field, message) {
    field.classList.add('border-red-500');
    
    const errorElement = document.createElement('div');
    errorElement.className = 'text-red-500 text-sm mt-1';
    errorElement.textContent = message;
    errorElement.id = `error-${field.name}`;
    
    const existingError = document.getElementById(`error-${field.name}`);
    if (existingError) {
        existingError.remove();
    }
    
    field.parentNode.insertBefore(errorElement, field.nextSibling);
}

function clearFieldError(event) {
    const field = event.target;
    field.classList.remove('border-red-500');
    
    const errorElement = document.getElementById(`error-${field.name}`);
    if (errorElement) {
        errorElement.remove();
    }
}

function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
}

// Password strength checker
function checkPasswordStrength(password) {
    let score = 0;
    const feedback = [];
    
    // Length check
    if (password.length >= 12) score += 25;
    else if (password.length >= 8) score += 15;
    else feedback.push('Use at least 8 characters');
    
    // Character variety
    if (/[a-z]/.test(password)) score += 5;
    else feedback.push('Add lowercase letters');
    
    if (/[A-Z]/.test(password)) score += 5;
    else feedback.push('Add uppercase letters');
    
    if (/[0-9]/.test(password)) score += 10;
    else feedback.push('Add numbers');
    
    if (/[^A-Za-z0-9]/.test(password)) score += 15;
    else feedback.push('Add symbols');
    
    // Determine strength level
    let level = 'Very Weak';
    let color = 'red';
    
    if (score >= 80) {
        level = 'Very Strong';
        color = 'green';
    } else if (score >= 60) {
        level = 'Strong';
        color = 'blue';
    } else if (score >= 40) {
        level = 'Medium';
        color = 'yellow';
    } else if (score >= 20) {
        level = 'Weak';
        color = 'orange';
    }
    
    return {
        score: Math.min(100, score),
        level,
        color,
        feedback: feedback.slice(0, 3)
    };
}

// Utility functions
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Export for use in other files
window.PasswordManager = {
    validateField,
    checkPasswordStrength,
    debounce,
    throttle,
    showPassword,
    copyPassword,
    deletePassword,
    copyRevealedPassword,
    closePasswordModal,
    showAlert
};
