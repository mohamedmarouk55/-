#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
فحص جميع الـ routes في النظام
"""

import re
import os

def check_routes():
    """فحص جميع الـ routes المعرفة في app.py"""
    print("🔍 فحص جميع الـ routes في النظام...")
    print("=" * 50)
    
    # قراءة ملف app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن جميع الـ routes
    route_pattern = r"@app\.route\(['\"]([^'\"]+)['\"]"
    routes = re.findall(route_pattern, content)
    
    print(f"📊 تم العثور على {len(routes)} route:")
    print("-" * 30)
    
    for i, route in enumerate(routes, 1):
        print(f"{i:2d}. {route}")
    
    print("-" * 30)
    
    # فحص القوالب المطلوبة
    print("\n🔍 فحص القوالب المطلوبة...")
    
    # البحث عن render_template في الكود
    template_pattern = r"render_template\(['\"]([^'\"]+)['\"]"
    templates = re.findall(template_pattern, content)
    
    print(f"📊 تم العثور على {len(set(templates))} قالب مطلوب:")
    
    templates_dir = 'templates'
    missing_templates = []
    existing_templates = []
    
    for template in set(templates):
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            existing_templates.append(template)
            print(f"✅ {template}")
        else:
            missing_templates.append(template)
            print(f"❌ {template} - مفقود!")
    
    print("-" * 30)
    print(f"✅ القوالب الموجودة: {len(existing_templates)}")
    print(f"❌ القوالب المفقودة: {len(missing_templates)}")
    
    if missing_templates:
        print(f"\n⚠️ القوالب المفقودة: {', '.join(missing_templates)}")
    
    print("\n" + "=" * 50)
    
    # فحص الروابط في القائمة الجانبية
    print("🔍 فحص روابط القائمة الجانبية...")
    
    base_template_path = os.path.join(templates_dir, 'base.html')
    if os.path.exists(base_template_path):
        with open(base_template_path, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        # البحث عن url_for في القائمة الجانبية
        url_for_pattern = r"url_for\(['\"]([^'\"]+)['\"]"
        sidebar_routes = re.findall(url_for_pattern, base_content)
        
        print(f"📊 روابط القائمة الجانبية ({len(set(sidebar_routes))}):")
        
        for route_name in set(sidebar_routes):
            if route_name in [r.split('/')[-1] or 'index' for r in routes] or route_name == 'index':
                print(f"✅ {route_name}")
            else:
                print(f"❌ {route_name} - route مفقود!")
    
    print("\n🎉 انتهى الفحص!")
    return len(missing_templates) == 0

if __name__ == '__main__':
    check_routes()