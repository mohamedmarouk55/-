# إدارة قاعدة البيانات

import sqlite3
import os
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, db_path='management_system.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
        return conn
    
    def init_database(self):
        """إنشاء الجداول الأساسية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول الموظفين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_number TEXT UNIQUE,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                phone TEXT,
                email TEXT,
                hire_date TEXT NOT NULL,
                status TEXT DEFAULT 'نشط',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إضافة عمود employee_number إذا لم يكن موجوداً
        try:
            cursor.execute('ALTER TABLE employees ADD COLUMN employee_number TEXT UNIQUE')
        except sqlite3.OperationalError:
            pass  # العمود موجود بالفعل
        
        # جدول السيارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                license_plate TEXT UNIQUE NOT NULL,
                color TEXT,
                status TEXT DEFAULT 'متاح',
                purchase_price REAL,
                current_value REAL,
                engine_number TEXT,
                chassis_number TEXT,
                mileage INTEGER DEFAULT 0,
                fuel_type TEXT DEFAULT 'بنزين',
                insurance_expiry TEXT,
                maintenance_date TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إضافة الأعمدة المفقودة إذا لم تكن موجودة
        try:
            cursor.execute('ALTER TABLE cars ADD COLUMN engine_number TEXT')
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute('ALTER TABLE cars ADD COLUMN chassis_number TEXT')
        except sqlite3.OperationalError:
            pass
        
        # جدول البيانات المالية
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK (type IN ('إيراد', 'مصروف')),
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                reference_type TEXT, -- 'employee', 'car', 'general'
                reference_id INTEGER,
                payment_method TEXT DEFAULT 'نقدي',
                receipt_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المستخدمين (للمستقبل)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول السجلات (للتدقيق)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                table_name TEXT NOT NULL,
                record_id INTEGER,
                old_values TEXT,
                new_values TEXT,
                ip_address TEXT,
                user_agent TEXT,
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
        
        # إضافة الفهارس لتحسين الأداء
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_status ON employees(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cars_status ON cars(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cars_brand ON cars(brand)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_financial_type ON financial_records(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_financial_date ON financial_records(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_financial_category ON financial_records(category)')
        
        # جدول عهد السيارات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_custody (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                car_id INTEGER NOT NULL,
                employee_number TEXT NOT NULL,
                custody_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT DEFAULT 'نشط',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (car_id) REFERENCES cars (id)
            )
        ''')
        
        # جدول الخزينة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treasury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL CHECK (transaction_type IN ('إيداع', 'سحب')),
                amount REAL NOT NULL,
                description TEXT,
                reference_number TEXT,
                date TEXT NOT NULL,
                created_by TEXT,
                balance_after REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول المصروفات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                receipt_number TEXT,
                date TEXT NOT NULL,
                approved_by TEXT,
                status TEXT DEFAULT 'معتمد',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إضافة فهارس للجداول الجديدة
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_custody_employee ON car_custody(employee_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_custody_car ON car_custody(car_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_custody_status ON car_custody(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_treasury_type ON treasury(transaction_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_treasury_date ON treasury(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)')
        
        # إدراج الإعدادات الافتراضية
        self._insert_default_settings(cursor)
        
        conn.commit()
        conn.close()
    
    def _insert_default_settings(self, cursor):
        """إدراج الإعدادات الافتراضية"""
        default_settings = [
            ('company_name', 'شركة الإدارة الشاملة', 'اسم الشركة'),
            ('company_address', 'الرياض، المملكة العربية السعودية', 'عنوان الشركة'),
            ('company_phone', '+966501234567', 'هاتف الشركة'),
            ('company_email', 'info@company.com', 'بريد الشركة الإلكتروني'),
            ('currency', 'SAR', 'العملة المستخدمة'),
            ('tax_rate', '15', 'معدل الضريبة المضافة'),
            ('backup_enabled', '1', 'تفعيل النسخ الاحتياطي'),
            ('notifications_enabled', '1', 'تفعيل الإشعارات'),
        ]
        
        for key, value, description in default_settings:
            cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value, description)
                VALUES (?, ?, ?)
            ''', (key, value, description))
    
    def backup_database(self, backup_path=None):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f'backup_management_system_{timestamp}.db'
        
        try:
            # نسخ قاعدة البيانات
            source_conn = self.get_connection()
            backup_conn = sqlite3.connect(backup_path)
            source_conn.backup(backup_conn)
            source_conn.close()
            backup_conn.close()
            
            return True, f'تم إنشاء النسخة الاحتياطية: {backup_path}'
        except Exception as e:
            return False, f'خطأ في إنشاء النسخة الاحتياطية: {str(e)}'
    
    def restore_database(self, backup_path):
        """استعادة قاعدة البيانات من نسخة احتياطية"""
        if not os.path.exists(backup_path):
            return False, 'ملف النسخة الاحتياطية غير موجود'
        
        try:
            # إنشاء نسخة احتياطية من القاعدة الحالية أولاً
            current_backup = f'current_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            self.backup_database(current_backup)
            
            # استعادة من النسخة الاحتياطية
            backup_conn = sqlite3.connect(backup_path)
            restore_conn = sqlite3.connect(self.db_path)
            backup_conn.backup(restore_conn)
            backup_conn.close()
            restore_conn.close()
            
            return True, 'تم استعادة قاعدة البيانات بنجاح'
        except Exception as e:
            return False, f'خطأ في استعادة قاعدة البيانات: {str(e)}'
    
    def get_database_stats(self):
        """الحصول على إحصائيات قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # إحصائيات الجداول
        tables = ['employees', 'cars', 'financial_records', 'users', 'audit_logs']
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            stats[f'{table}_count'] = cursor.fetchone()[0]
        
        # حجم قاعدة البيانات
        if os.path.exists(self.db_path):
            stats['database_size'] = os.path.getsize(self.db_path)
        
        # آخر تحديث
        cursor.execute('''
            SELECT MAX(updated_at) FROM (
                SELECT updated_at FROM employees
                UNION ALL
                SELECT updated_at FROM cars
                UNION ALL
                SELECT updated_at FROM financial_records
            )
        ''')
        last_update = cursor.fetchone()[0]
        stats['last_update'] = last_update
        
        conn.close()
        return stats
    
    def optimize_database(self):
        """تحسين قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # تحليل الجداول
            cursor.execute('ANALYZE')
            
            # ضغط قاعدة البيانات
            cursor.execute('VACUUM')
            
            conn.commit()
            conn.close()
            
            return True, 'تم تحسين قاعدة البيانات بنجاح'
        except Exception as e:
            conn.close()
            return False, f'خطأ في تحسين قاعدة البيانات: {str(e)}'
    
    def log_action(self, user_id, action, table_name, record_id, old_values=None, new_values=None, ip_address=None, user_agent=None):
        """تسجيل العمليات للتدقيق"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, action, table_name, record_id,
            json.dumps(old_values) if old_values else None,
            json.dumps(new_values) if new_values else None,
            ip_address, user_agent
        ))
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """الحصول على إعداد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        return result['value'] if result else default
    
    def set_setting(self, key, value, description=None):
        """تعيين إعداد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, description, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (key, value, description))
        
        conn.commit()
        conn.close()
    
    def close(self):
        """إغلاق الاتصال"""
        pass  # SQLite يغلق الاتصال تلقائياً

# إنشاء مثيل عام لإدارة قاعدة البيانات
db_manager = DatabaseManager()