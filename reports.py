# إدارة التقارير والإحصائيات

import sqlite3
from datetime import datetime, timedelta
import json
import csv
import io
from collections import defaultdict

class ReportsManager:
    def __init__(self, db_path='management_system.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_employees_report(self, department=None, status=None):
        """تقرير الموظفين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM employees WHERE 1=1'
        params = []
        
        if department:
            query += ' AND department = ?'
            params.append(department)
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY name'
        
        cursor.execute(query, params)
        employees = cursor.fetchall()
        
        # إحصائيات إضافية
        cursor.execute('SELECT department, COUNT(*) as count FROM employees GROUP BY department')
        dept_stats = dict(cursor.fetchall())
        
        cursor.execute('SELECT AVG(salary) as avg_salary, SUM(salary) as total_salary FROM employees')
        salary_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'employees': [dict(emp) for emp in employees],
            'department_stats': dept_stats,
            'salary_stats': dict(salary_stats),
            'total_count': len(employees)
        }
    
    def get_cars_report(self, status=None, brand=None):
        """تقرير السيارات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM cars WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        if brand:
            query += ' AND brand = ?'
            params.append(brand)
        
        query += ' ORDER BY brand, model'
        
        cursor.execute(query, params)
        cars = cursor.fetchall()
        
        # إحصائيات إضافية
        cursor.execute('SELECT status, COUNT(*) as count FROM cars GROUP BY status')
        status_stats = dict(cursor.fetchall())
        
        cursor.execute('SELECT brand, COUNT(*) as count FROM cars GROUP BY brand')
        brand_stats = dict(cursor.fetchall())
        
        cursor.execute('''
            SELECT 
                SUM(purchase_price) as total_purchase,
                SUM(current_value) as total_current,
                AVG(purchase_price) as avg_purchase,
                AVG(current_value) as avg_current
            FROM cars 
            WHERE purchase_price IS NOT NULL AND current_value IS NOT NULL
        ''')
        value_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'cars': [dict(car) for car in cars],
            'status_stats': status_stats,
            'brand_stats': brand_stats,
            'value_stats': dict(value_stats) if value_stats else {},
            'total_count': len(cars)
        }
    
    def get_financial_report(self, start_date=None, end_date=None, type_filter=None):
        """التقرير المالي"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM financial_records WHERE 1=1'
        params = []
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        if type_filter:
            query += ' AND type = ?'
            params.append(type_filter)
        
        query += ' ORDER BY date DESC'
        
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        # إحصائيات مالية
        cursor.execute('''
            SELECT 
                type,
                SUM(amount) as total,
                COUNT(*) as count,
                AVG(amount) as average
            FROM financial_records 
            WHERE date BETWEEN ? AND ?
            GROUP BY type
        ''', (start_date or '1900-01-01', end_date or '2099-12-31'))
        
        type_stats = {}
        for row in cursor.fetchall():
            type_stats[row['type']] = {
                'total': row['total'],
                'count': row['count'],
                'average': row['average']
            }
        
        # إحصائيات حسب الفئة
        cursor.execute('''
            SELECT 
                category,
                type,
                SUM(amount) as total,
                COUNT(*) as count
            FROM financial_records 
            WHERE date BETWEEN ? AND ?
            GROUP BY category, type
            ORDER BY total DESC
        ''', (start_date or '1900-01-01', end_date or '2099-12-31'))
        
        category_stats = defaultdict(dict)
        for row in cursor.fetchall():
            category_stats[row['category']][row['type']] = {
                'total': row['total'],
                'count': row['count']
            }
        
        # الإيرادات والمصروفات الشهرية
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', date) as month,
                type,
                SUM(amount) as total
            FROM financial_records 
            WHERE date BETWEEN ? AND ?
            GROUP BY strftime('%Y-%m', date), type
            ORDER BY month
        ''', (start_date or '1900-01-01', end_date or '2099-12-31'))
        
        monthly_stats = defaultdict(dict)
        for row in cursor.fetchall():
            monthly_stats[row['month']][row['type']] = row['total']
        
        conn.close()
        
        # حساب صافي الربح
        total_income = type_stats.get('إيراد', {}).get('total', 0)
        total_expense = type_stats.get('مصروف', {}).get('total', 0)
        net_profit = total_income - total_expense
        
        return {
            'records': [dict(record) for record in records],
            'type_stats': type_stats,
            'category_stats': dict(category_stats),
            'monthly_stats': dict(monthly_stats),
            'summary': {
                'total_income': total_income,
                'total_expense': total_expense,
                'net_profit': net_profit,
                'total_records': len(records)
            }
        }
    
    def get_dashboard_stats(self):
        """إحصائيات لوحة التحكم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # إحصائيات الموظفين
        cursor.execute('SELECT COUNT(*) FROM employees WHERE status = "نشط"')
        active_employees = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(salary) FROM employees WHERE status = "نشط"')
        total_salaries = cursor.fetchone()[0] or 0
        
        # إحصائيات السيارات
        cursor.execute('SELECT COUNT(*) FROM cars')
        total_cars = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM cars WHERE status = "متاح"')
        available_cars = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM cars WHERE status = "صيانة"')
        maintenance_cars = cursor.fetchone()[0]
        
        # الإحصائيات المالية لهذا الشهر
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN type = 'إيراد' THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN type = 'مصروف' THEN amount ELSE 0 END) as expense
            FROM financial_records 
            WHERE strftime('%Y-%m', date) = ?
        ''', (current_month,))
        
        monthly_financial = cursor.fetchone()
        monthly_income = monthly_financial['income'] or 0
        monthly_expense = monthly_financial['expense'] or 0
        
        # الإحصائيات المالية الإجمالية
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN type = 'إيراد' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'مصروف' THEN amount ELSE 0 END) as total_expense
            FROM financial_records
        ''')
        
        total_financial = cursor.fetchone()
        total_income = total_financial['total_income'] or 0
        total_expense = total_financial['total_expense'] or 0
        
        conn.close()
        
        return {
            'employees': {
                'active': active_employees,
                'total_salaries': total_salaries
            },
            'cars': {
                'total': total_cars,
                'available': available_cars,
                'maintenance': maintenance_cars,
                'utilization_rate': (total_cars - available_cars) / total_cars * 100 if total_cars > 0 else 0
            },
            'financial': {
                'monthly_income': monthly_income,
                'monthly_expense': monthly_expense,
                'monthly_profit': monthly_income - monthly_expense,
                'total_income': total_income,
                'total_expense': total_expense,
                'total_profit': total_income - total_expense
            }
        }
    
    def export_to_csv(self, data, filename):
        """تصدير البيانات إلى CSV"""
        output = io.StringIO()
        
        if not data:
            return None
        
        # استخدام أول سجل لتحديد الأعمدة
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        
        return output.getvalue()
    
    def get_trends_analysis(self, days=30):
        """تحليل الاتجاهات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # اتجاه الإيرادات والمصروفات
        cursor.execute('''
            SELECT 
                date,
                SUM(CASE WHEN type = 'إيراد' THEN amount ELSE 0 END) as daily_income,
                SUM(CASE WHEN type = 'مصروف' THEN amount ELSE 0 END) as daily_expense
            FROM financial_records 
            WHERE date BETWEEN ? AND ?
            GROUP BY date
            ORDER BY date
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        daily_trends = []
        for row in cursor.fetchall():
            daily_trends.append({
                'date': row['date'],
                'income': row['daily_income'],
                'expense': row['daily_expense'],
                'profit': row['daily_income'] - row['daily_expense']
            })
        
        # اتجاه إضافة الموظفين
        cursor.execute('''
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as new_employees
            FROM employees 
            WHERE created_at BETWEEN ? AND ?
            GROUP BY DATE(created_at)
            ORDER BY date
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        employee_trends = [dict(row) for row in cursor.fetchall()]
        
        # اتجاه إضافة السيارات
        cursor.execute('''
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as new_cars
            FROM cars 
            WHERE created_at BETWEEN ? AND ?
            GROUP BY DATE(created_at)
            ORDER BY date
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        car_trends = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'financial_trends': daily_trends,
            'employee_trends': employee_trends,
            'car_trends': car_trends,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'days': days
            }
        }
    
    def get_performance_metrics(self):
        """مقاييس الأداء الرئيسية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # معدل دوران الموظفين (تقدير بناءً على التواريخ)
        cursor.execute('''
            SELECT 
                COUNT(*) as total_employees,
                AVG(julianday('now') - julianday(hire_date)) as avg_tenure_days
            FROM employees 
            WHERE status = 'نشط'
        ''')
        employee_metrics = cursor.fetchone()
        
        # كفاءة استخدام السيارات
        cursor.execute('''
            SELECT 
                COUNT(*) as total_cars,
                SUM(CASE WHEN status = 'متاح' THEN 1 ELSE 0 END) as available_cars,
                SUM(CASE WHEN status = 'مستأجر' THEN 1 ELSE 0 END) as rented_cars,
                SUM(CASE WHEN status = 'صيانة' THEN 1 ELSE 0 END) as maintenance_cars
            FROM cars
        ''')
        car_metrics = cursor.fetchone()
        
        # الأداء المالي الشهري
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', date) as month,
                SUM(CASE WHEN type = 'إيراد' THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN type = 'مصروف' THEN amount ELSE 0 END) as expense
            FROM financial_records 
            WHERE date >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month DESC
            LIMIT 12
        ''')
        
        monthly_performance = []
        for row in cursor.fetchall():
            monthly_performance.append({
                'month': row['month'],
                'income': row['income'],
                'expense': row['expense'],
                'profit': row['income'] - row['expense'],
                'profit_margin': (row['income'] - row['expense']) / row['income'] * 100 if row['income'] > 0 else 0
            })
        
        conn.close()
        
        # حساب المقاييس
        utilization_rate = ((car_metrics['total_cars'] - car_metrics['available_cars']) / car_metrics['total_cars'] * 100) if car_metrics['total_cars'] > 0 else 0
        
        avg_monthly_profit = sum(m['profit'] for m in monthly_performance) / len(monthly_performance) if monthly_performance else 0
        avg_profit_margin = sum(m['profit_margin'] for m in monthly_performance) / len(monthly_performance) if monthly_performance else 0
        
        return {
            'employee_metrics': {
                'total_employees': employee_metrics['total_employees'],
                'avg_tenure_years': (employee_metrics['avg_tenure_days'] or 0) / 365,
            },
            'car_metrics': {
                'total_cars': car_metrics['total_cars'],
                'utilization_rate': utilization_rate,
                'available_rate': car_metrics['available_cars'] / car_metrics['total_cars'] * 100 if car_metrics['total_cars'] > 0 else 0,
                'maintenance_rate': car_metrics['maintenance_cars'] / car_metrics['total_cars'] * 100 if car_metrics['total_cars'] > 0 else 0
            },
            'financial_metrics': {
                'avg_monthly_profit': avg_monthly_profit,
                'avg_profit_margin': avg_profit_margin,
                'monthly_performance': monthly_performance
            }
        }

# إنشاء مثيل عام لإدارة التقارير
reports_manager = ReportsManager()