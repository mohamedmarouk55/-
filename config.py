# إعدادات التطبيق

import os
from datetime import timedelta

class Config:
    # إعدادات Flask الأساسية
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    # إعدادات قاعدة البيانات
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'management_system.db')
    
    # إعدادات الجلسة
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # إعدادات التطبيق
    APP_NAME = 'نظام الإدارة الشامل'
    APP_VERSION = '1.0.0'
    
    # إعدادات الأمان
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # إعدادات التحميل
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # إعدادات التطوير
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # إعدادات الخادم
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # إعدادات اللغة والمنطقة
    LANGUAGES = ['ar', 'en']
    DEFAULT_LANGUAGE = 'ar'
    TIMEZONE = 'Asia/Riyadh'
    
    # إعدادات العملة
    CURRENCY = 'SAR'
    CURRENCY_SYMBOL = 'ريال'
    
    # إعدادات النسخ الاحتياطي
    BACKUP_ENABLED = True
    BACKUP_INTERVAL_HOURS = 24
    BACKUP_RETENTION_DAYS = 30
    
    # إعدادات التقارير
    REPORTS_PER_PAGE = 50
    EXPORT_FORMATS = ['csv', 'excel', 'pdf']
    
    # إعدادات الإشعارات
    NOTIFICATIONS_ENABLED = True
    EMAIL_NOTIFICATIONS = False
    
    # إعدادات الأداء
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # إعدادات السجلات
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'app.log'
    
    @staticmethod
    def init_app(app):
        """تهيئة التطبيق مع الإعدادات"""
        pass

class DevelopmentConfig(Config):
    """إعدادات بيئة التطوير"""
    DEBUG = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """إعدادات بيئة الإنتاج"""
    DEBUG = False
    WTF_CSRF_ENABLED = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # إعداد السجلات للإنتاج
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            file_handler = RotatingFileHandler(
                cls.LOG_FILE, 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('تم بدء تشغيل نظام الإدارة الشامل')

class TestingConfig(Config):
    """إعدادات بيئة الاختبار"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATABASE_PATH = ':memory:'

# قاموس الإعدادات
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}