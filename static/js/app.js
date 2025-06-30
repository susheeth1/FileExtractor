document.addEventListener('DOMContentLoaded', function() {
    // File upload functionality
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const zipSubmitBtn = document.getElementById('zipSubmitBtn');
    const githubForm = document.getElementById('githubForm');
    const githubSubmitBtn = document.getElementById('githubSubmitBtn');
    const githubUrl = document.getElementById('github_url');

    // Drag and drop functionality
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.name.toLowerCase().endsWith('.zip')) {
                handleFileSelection(file);
            } else {
                showAlert('Please select a ZIP file.', 'error');
            }
        }
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileSelection(file);
        }
    });

    function handleFileSelection(file) {
        fileName.textContent = file.name;
        fileSize.textContent = `(${formatFileSize(file.size)})`;
        fileInfo.style.display = 'block';
        zipSubmitBtn.disabled = false;
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // GitHub URL validation
    githubUrl.addEventListener('input', function() {
        const url = this.value.trim();
        if (url) {
            const isValid = /^https:\/\/github\.com\/[^\/]+\/[^\/]+\/?$/.test(url);
            if (isValid) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                githubSubmitBtn.disabled = false;
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
                githubSubmitBtn.disabled = true;
            }
        } else {
            this.classList.remove('is-valid', 'is-invalid');
            githubSubmitBtn.disabled = false;
        }
    });

    // Form submission handling
    document.getElementById('zipForm').addEventListener('submit', function(e) {
        if (!fileInput.files[0]) {
            e.preventDefault();
            showAlert('Please select a ZIP file first.', 'error');
            return;
        }
        
        showProcessingState(zipSubmitBtn, 'Processing ZIP file...');
    });

    githubForm.addEventListener('submit', function(e) {
        const url = githubUrl.value.trim();
        if (!url) {
            e.preventDefault();
            showAlert('Please enter a GitHub repository URL.', 'error');
            return;
        }
        
        showProcessingState(githubSubmitBtn, 'Cloning repository...');
    });

    function showProcessingState(button, text) {
        button.disabled = true;
        button.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
        button.classList.add('processing');
    }

    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'info'} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at the top of the main container
        const container = document.querySelector('.container');
        const firstChild = container.querySelector('.row');
        container.insertBefore(alertDiv, firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // GitHub URL examples
    const githubExamples = [
        'https://github.com/torvalds/linux',
        'https://github.com/microsoft/vscode',
        'https://github.com/facebook/react',
        'https://github.com/python/cpython'
    ];

    // Add example link functionality
    const githubInput = document.getElementById('github_url');
    if (githubInput) {
        githubInput.addEventListener('focus', function() {
            if (!this.value) {
                // Show placeholder with random example
                const example = githubExamples[Math.floor(Math.random() * githubExamples.length)];
                this.placeholder = example;
            }
        });
    }

    // Auto-resize textareas if any
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });

    // Tooltips initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File size validation
    const maxFileSize = 100 * 1024 * 1024; // 100MB
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file && file.size > maxFileSize) {
            showAlert('File size exceeds 100MB limit. Please choose a smaller file.', 'error');
            this.value = '';
            fileInfo.style.display = 'none';
            zipSubmitBtn.disabled = true;
        }
    });
});
