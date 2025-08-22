import sqlite3
import hashlib

def create_database():
    print("🔧 إنشاء قاعدة البيانات يدوياً...")
    
    conn = sqlite3.connect('car_management.db')
    cursor = conn.cursor()
    
    # جدول الموظفين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            hire_date TEXT NOT NULL,
            salary REAL,
            status TEXT DEFAULT 'نشط' CHECK (status IN ('نشط', 'غير نشط')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول السيارات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            license_plate TEXT UNIQUE NOT NULL,
            color TEXT,
            fuel_type TEXT DEFAULT 'بنزين',
            status TEXT DEFAULT 'متاح' CHECK (status IN ('متاح', 'مستأجر', 'صيانة', 'غير متاح')),
            purchase_date TEXT,
            purchase_price REAL,
            current_value REAL,
            engine_number TEXT,
            chassis_number TEXT,
            responsible_employee_id INTEGER,
            insurance_expiry TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (responsible_employee_id) REFERENCES employees (id)
        )
    ''')
    
    # جدول المصروفات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_type TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            amount REAL NOT NULL,
            description TEXT,
            receipt_number TEXT,
            date TEXT NOT NULL,
            related_car_id INTEGER,
            related_employee_id INTEGER,
            approved_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (related_car_id) REFERENCES cars (id),
            FOREIGN KEY (related_employee_id) REFERENCES employees (id)
        )
    ''')
    
    # جدول الخزينة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treasury (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK (type IN ('إيداع', 'سحب')),
            amount REAL NOT NULL,
            description TEXT,
            reference_number TEXT,
            date TEXT NOT NULL,
            balance REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول عهد السيارات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car_custody (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            employee_number TEXT NOT NULL,
            car_id INTEGER NOT NULL,
            custody_date TEXT NOT NULL,
            expected_return TEXT,
            return_date TEXT,
            notes TEXT,
            return_notes TEXT,
            status TEXT DEFAULT 'نشط' CHECK (status IN ('نشط', 'مُسلم')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (id),
            FOREIGN KEY (car_id) REFERENCES cars (id)
        )
    ''')
    
    # جدول البيانات المالية
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK (type IN ('إيراد', 'مصروف')),
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول الإعدادات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول بيانات المطور
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS developer_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_ar TEXT NOT NULL,
            name_en TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إضافة مستخدم افتراضي
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@rashid.com', hashlib.md5('admin123'.encode()).hexdigest(), 'admin'))
    
    # إضافة بيانات المطور
    cursor.execute('''
        INSERT OR IGNORE INTO developer_info (name_ar, name_en, email, mobile)
        VALUES (?, ?, ?, ?)
    ''', ('محمد مبروك عطية', 'Mohamed Marouk Atia', 'mohamedmarouk55@gmail.com', '0570453337'))
    
    # إضافة إعدادات افتراضية
    default_settings = [
        ('company_name', 'RASHID INDUSTRIAL CO.', 'اسم الشركة'),
        ('company_address', 'الرياض، المملكة العربية السعودية', 'عنوان الشركة'),
        ('currency', 'SAR', 'العملة المستخدمة'),
        ('tax_rate', '15', 'معدل الضريبة المضافة'),
        ('developer_name_ar', 'محمد مبروك عطية', 'اسم المطور بالعربية'),
        ('developer_name_en', 'Mohamed Marouk Atia', 'اسم المطور بالإنجليزية'),
        ('developer_email', 'mohamedmarouk55@gmail.com', 'بريد المطور الإلكتروني'),
        ('developer_mobile', '0570453337', 'رقم جوال المطور'),
    ]
    
    for key, value, description in default_settings:
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value, description)
            VALUES (?, ?, ?)
        ''', (key, value, description))
    
    # إضافة رصيد افتراضي للخزينة
    cursor.execute('''
        INSERT OR IGNORE INTO treasury (type, amount, description, reference_number, date, balance)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('إيداع', 10000.0, 'رصيد افتراضي', 'INIT-001', '2024-01-01', 10000.0))
    
    conn.commit()
    conn.close()
    
    print("✅ تم إنشاء قاعدة البيانات بنجاح!")
    print("📊 تم إضافة جميع الجداول والبيانات الافتراضية")
    print("👤 المستخدم الافتراضي: admin / admin123")
    print("💻 بيانات المطور: محمد مبروك عطية")

if __name__ == "__main__":
    create_database()