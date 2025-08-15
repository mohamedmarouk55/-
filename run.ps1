# نظام إدارة شامل - سكريبت التشغيل

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       نظام إدارة شامل - التشغيل" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من وجود Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python مثبت: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "خطأ: Python غير مثبت على النظام" -ForegroundColor Red
    Write-Host "يرجى تثبيت Python من: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "تأكد من إضافة Python إلى PATH أثناء التثبيت" -ForegroundColor Yellow
    Read-Host "اضغط Enter للخروج"
    exit 1
}

Write-Host ""
Write-Host "تثبيت المكتبات المطلوبة..." -ForegroundColor Yellow

# تثبيت المكتبات
try {
    pip install Flask==2.3.3 Werkzeug==2.3.7 Jinja2==3.1.2 MarkupSafe==2.1.3 itsdangerous==2.1.2 click==8.1.7 blinker==1.6.3
    Write-Host "تم تثبيت المكتبات بنجاح!" -ForegroundColor Green
} catch {
    Write-Host "خطأ في تثبيت المكتبات" -ForegroundColor Red
    Read-Host "اضغط Enter للخروج"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "التطبيق يعمل الآن على:" -ForegroundColor Green
Write-Host "http://localhost:5000" -ForegroundColor White -BackgroundColor Blue
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "لإيقاف التطبيق، اضغط Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# تشغيل التطبيق
try {
    python run_app.py
} catch {
    Write-Host "خطأ في تشغيل التطبيق" -ForegroundColor Red
    Read-Host "اضغط Enter للخروج"
}