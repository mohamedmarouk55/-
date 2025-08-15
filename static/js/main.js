// الوظائف الرئيسية لنظام الإدارة الشامل

// تهيئة التطبيق عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// تهيئة التطبيق
function initializeApp() {
    setupSidebar();
    setupAnimations();
    setupFormValidation();
    setupDataTables();
    setupNotifications();
    setupTheme();
}

// إعداد القائمة الجانبية التفاعلية
function setupSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    if (sidebar && mainContent) {
        // تأثير الماوس للقائمة الجانبية
        sidebar.addEventListener('mouseenter', function() {
            this.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
        });
        
        sidebar.addEventListener('mouseleave', function() {
            this.classList.add('collapsed');
            mainContent.classList.add('expanded');
        });
        
        // إضافة تأثيرات للروابط
        const sidebarLinks = sidebar.querySelectorAll('.sidebar-menu a');
        sidebarLinks.forEach(link => {
            link.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(-5px)';
            });
            
            link.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
            });
        });
    }
}

// إعداد الرسوم المتحركة
function setupAnimations() {
    // تأثير الظهور التدريجي للعناصر
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // مراقبة البطاقات والعناصر
    const elementsToAnimate = document.querySelectorAll('.card, .stats-card, .table');
    elementsToAnimate.forEach(el => {
        observer.observe(el);
    });
}

// إعداد التحقق من صحة النماذج
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                showNotification('يرجى ملء جميع الحقول المطلوبة', 'error');
            }
            form.classList.add('was-validated');
        });
        
        // تحسين تجربة المستخدم للحقول
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

// التحقق من صحة حقل واحد
function validateField(field) {
    const isValid = field.checkValidity();
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    return isValid;
}

// إعداد الجداول التفاعلية
function setupDataTables() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        // إضافة تأثيرات التمرير
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.animationDelay = `${index * 0.1}s`;
            
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.02)';
                this.style.zIndex = '10';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.zIndex = '1';
            });
        });
        
        // إضافة وظيفة البحث إذا لم تكن موجودة
        if (!table.parentElement.querySelector('.search-input')) {
            addSearchFunctionality(table);
        }
    });
}

// إضافة وظيفة البحث للجداول
function addSearchFunctionality(table) {
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'form-control search-input mb-3';
    searchInput.placeholder = 'البحث في الجدول...';
    
    table.parentElement.insertBefore(searchInput, table);
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const shouldShow = text.includes(searchTerm);
            
            row.style.display = shouldShow ? '' : 'none';
            
            if (shouldShow && searchTerm) {
                highlightSearchTerm(row, searchTerm);
            } else {
                removeHighlight(row);
            }
        });
        
        updateTableStats(table, searchTerm);
    });
}

// تمييز نتائج البحث
function highlightSearchTerm(row, term) {
    const cells = row.querySelectorAll('td');
    cells.forEach(cell => {
        const text = cell.textContent;
        const regex = new RegExp(`(${term})`, 'gi');
        const highlightedText = text.replace(regex, '<mark>$1</mark>');
        
        if (highlightedText !== text) {
            cell.innerHTML = highlightedText;
        }
    });
}

// إزالة التمييز
function removeHighlight(row) {
    const marks = row.querySelectorAll('mark');
    marks.forEach(mark => {
        mark.outerHTML = mark.textContent;
    });
}

// تحديث إحصائيات الجدول
function updateTableStats(table, searchTerm) {
    const visibleRows = table.querySelectorAll('tbody tr[style=""], tbody tr:not([style])');
    const totalRows = table.querySelectorAll('tbody tr').length;
    
    let statsElement = table.parentElement.querySelector('.table-stats');
    if (!statsElement) {
        statsElement = document.createElement('div');
        statsElement.className = 'table-stats text-muted small mt-2';
        table.parentElement.appendChild(statsElement);
    }
    
    if (searchTerm) {
        statsElement.textContent = `عرض ${visibleRows.length} من أصل ${totalRows} سجل`;
    } else {
        statsElement.textContent = `إجمالي ${totalRows} سجل`;
    }
}

// إعداد الإشعارات
function setupNotifications() {
    // إنشاء حاوية الإشعارات
    if (!document.getElementById('notifications-container')) {
        const container = document.createElement('div');
        container.id = 'notifications-container';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
}

// عرض إشعار
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notifications-container');
    const notification = document.createElement('div');
    
    const typeClasses = {
        success: 'alert-success',
        error: 'alert-danger',
        warning: 'alert-warning',
        info: 'alert-info'
    };
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    };
    
    notification.className = `alert ${typeClasses[type]} alert-dismissible fade show`;
    notification.innerHTML = `
        <i class="${icons[type]} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    // إزالة الإشعار تلقائياً
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, duration);
}

// إعداد المظهر
function setupTheme() {
    // التحقق من تفضيل المستخدم للمظهر المظلم
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (prefersDark) {
        document.body.classList.add('dark-theme');
    }
    
    // إضافة زر تبديل المظهر
    addThemeToggle();
}

// إضافة زر تبديل المظهر
function addThemeToggle() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'btn btn-outline-secondary btn-sm ms-2';
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        themeToggle.title = 'تبديل المظهر';
        
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            const isDark = document.body.classList.contains('dark-theme');
            this.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            
            // حفظ التفضيل
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
        
        navbar.querySelector('div').appendChild(themeToggle);
        
        // تحميل التفضيل المحفوظ
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
    }
}

// وظائف مساعدة للتنسيق
function formatCurrency(amount) {
    return new Intl.NumberFormat('ar-SA', {
        style: 'currency',
        currency: 'SAR',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ar-SA');
}

function formatNumber(number) {
    return new Intl.NumberFormat('ar-SA').format(number);
}

// وظائف التصدير
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csvContent = [];
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(cell => {
            return '"' + cell.textContent.replace(/"/g, '""') + '"';
        });
        csvContent.push(rowData.join(','));
    });
    
    const csvString = csvContent.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

// وظائف الطباعة
function printTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>طباعة الجدول</title>
                <style>
                    body { font-family: Arial, sans-serif; direction: rtl; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                ${table.outerHTML}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// وظائف التحديث التلقائي للإحصائيات
function startStatsAutoUpdate(interval = 30000) {
    setInterval(() => {
        updateDashboardStats();
    }, interval);
}

function updateDashboardStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStatsDisplay(data);
        })
        .catch(error => {
            console.error('خطأ في تحديث الإحصائيات:', error);
        });
}

function updateStatsDisplay(data) {
    const elements = {
        'employeesCount': data.employees_count,
        'carsCount': data.cars_count,
        'availableCars': data.available_cars,
        'totalIncome': formatCurrency(data.total_income),
        'totalExpenses': formatCurrency(data.total_expenses),
        'netProfit': formatCurrency(data.net_profit)
    };
    
    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            animateNumberChange(element, value);
        }
    });
}

function animateNumberChange(element, newValue) {
    element.style.transform = 'scale(1.1)';
    element.style.color = '#28a745';
    
    setTimeout(() => {
        element.textContent = newValue;
        element.style.transform = 'scale(1)';
        element.style.color = '';
    }, 200);
}

// تهيئة التحديث التلقائي عند تحميل الصفحة الرئيسية
if (window.location.pathname === '/' || window.location.pathname.includes('index')) {
    document.addEventListener('DOMContentLoaded', () => {
        startStatsAutoUpdate();
    });
}