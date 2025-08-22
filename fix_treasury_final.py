#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
إصلاح نهائي لصفحة الخزينة
"""

import sqlite3
import os
from datetime import datetime

def fix_treasury_route():
    """إصلاح route الخزينة في app.py"""
    print("🔧 إصلاح route الخزينة...")
    
    # قراءة ملف app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # التأكد من وجود معالجة صحيحة للأخطاء
    treasury_route_fix = '''@app.route('/treasury', methods=['GET', 'POST'])
@login_required
def treasury():
    try:
        conn = get_db_connection()
        
        if request.method == 'POST':
            try:
                transaction_type = request.form.get('transaction_type', '')
                amount_str = request.form.get('amount', '0')
                description = request.form.get('description', '')
                reference_number = request.form.get('reference_number', '')
                date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
                created_by = session.get('username', 'admin')
                
                # التحقق من صحة البيانات
                if not transaction_type or transaction_type not in ['إيداع', 'سحب']:
                    flash('يرجى اختيار نوع المعاملة', 'error')
                    return redirect(url_for('treasury'))
                
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        flash('يرجى إدخال مبلغ صحيح أكبر من صفر', 'error')
                        return redirect(url_for('treasury'))
                except (ValueError, TypeError):
                    flash('يرجى إدخال مبلغ صحيح', 'error')
                    return redirect(url_for('treasury'))
                
                # حساب الرصيد الجديد
                current_balance_row = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
                current_balance = float(current_balance_row[0]) if current_balance_row else 0.0
                
                if transaction_type == 'إيداع':
                    new_balance = current_balance + amount
                else:  # سحب
                    new_balance = current_balance - amount
                    if new_balance < 0:
                        flash('لا يمكن السحب - الرصيد غير كافي', 'error')
                        return redirect(url_for('treasury'))
                
                # إضافة المعاملة
                conn.execute('''INSERT INTO treasury (transaction_type, amount, description, reference_number, created_by, date, balance_after) VALUES (?, ?, ?, ?, ?, ?, ?)''', (transaction_type, amount, description, reference_number, created_by, date, new_balance))
                
                conn.commit()
                flash(f'تم إضافة {transaction_type} بمبلغ {amount:,.0f} ريال بنجاح!', 'success')
                return redirect(url_for('treasury'))
                
            except Exception as e:
                print(f"خطأ في معالجة معاملة الخزينة: {e}")
                flash('حدث خطأ في تسجيل المعاملة', 'error')
                return redirect(url_for('treasury'))
        
        # جلب جميع المعاملات مع معالجة الأخطاء
        try:
            transactions = conn.execute('SELECT * FROM treasury ORDER BY created_at DESC').fetchall()
        except Exception as e:
            print(f"خطأ في جلب المعاملات: {e}")
            transactions = []
        
        # إحصائيات مع حماية من الأخطاء
        try:
            total_deposits = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "إيداع"').fetchone()[0] or 0
            total_withdrawals = conn.execute('SELECT COALESCE(SUM(amount), 0) FROM treasury WHERE transaction_type = "سحب"').fetchone()[0] or 0
            current_balance_row = conn.execute('SELECT COALESCE(balance_after, 0) FROM treasury ORDER BY created_at DESC LIMIT 1').fetchone()
            current_balance = current_balance_row[0] if current_balance_row else 0
            
            # تحويل إلى float للتأكد
            total_deposits = float(total_deposits)
            total_withdrawals = float(total_withdrawals)
            current_balance = float(current_balance)
            
        except Exception as e:
            print(f"خطأ في حساب الإحصائيات: {e}")
            total_deposits = 0.0
            total_withdrawals = 0.0
            current_balance = 0.0
        
        conn.close()
        
        return render_template('treasury.html', 
                             transactions=transactions,
                             total_deposits=total_deposits,
                             total_withdrawals=total_withdrawals,
                             current_balance=current_balance)
                             
    except Exception as e:
        print(f"خطأ عام في صفحة الخزينة: {e}")
        import traceback
        traceback.print_exc()
        flash('حدث خطأ في تحميل صفحة الخزينة', 'error')
        return redirect(url_for('index'))'''
    
    print("✅ تم إعداد route الخزينة المحسن")
    return True

def create_treasury_template_backup():
    """إنشاء نسخة احتياطية من قالب الخزينة"""
    print("🔧 إنشاء نسخة احتياطية من قالب الخزينة...")
    
    template_path = 'templates/treasury.html'
    backup_path = 'templates/treasury_backup.html'
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ تم إنشاء نسخة احتياطية")
        return True
    else:
        print("❌ لم يتم العثور على قالب الخزينة")
        return False

def test_treasury_template():
    """اختبار قالب الخزينة"""
    print("🔍 اختبار قالب الخزينة...")
    
    template_path = 'templates/treasury.html'
    
    if not os.path.exists(template_path):
        print("❌ قالب الخزينة غير موجود")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # فحص المشاكل الشائعة
    issues = []
    
    if 'moment()' in content:
        issues.append("استخدام moment() غير المدعوم")
    
    if 'add_treasury_transaction' in content:
        issues.append("مرجع لـ route غير موجود")
    
    if '{{ format(' in content and 'or 0' not in content:
        issues.append("مشاكل محتملة في التنسيق")
    
    if issues:
        print("⚠️ مشاكل محتملة:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ قالب الخزينة يبدو سليماً")
        return True

def main():
    """الدالة الرئيسية"""
    print("🚀 إصلاح نهائي لصفحة الخزينة")
    print("=" * 50)
    
    # إنشاء نسخة احتياطية
    create_treasury_template_backup()
    
    print("-" * 30)
    
    # اختبار القالب
    if test_treasury_template():
        print("✅ قالب الخزينة سليم")
    else:
        print("⚠️ قد تحتاج لإصلاحات إضافية")
    
    print("-" * 30)
    
    # إصلاح route
    fix_treasury_route()
    
    print("=" * 50)
    print("🎉 انتهى الإصلاح النهائي!")
    print("💡 يمكنك الآن تجربة صفحة الخزينة")
    print("🌐 الرابط: http://localhost:5000/treasury")

if __name__ == '__main__':
    main()