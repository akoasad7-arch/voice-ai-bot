# تعريف نفسك لـ Git (نفذها مرة واحدة فقط)
git config --global user.name "akoasad7-arch"
git config --global user.email "بريدك_الإلكتروني_هنا"

# تحويل المجلد الحالي لمستودع محلي
git init

# إضافة الملفات (الكود وقائمة المكتبات)
git add main.py requirements.txt

# تسجيل التغييرات
git commit -m "إضافة بوت تحويل النص لصوت"

# ربط المستودع المحلي بالمستودع الذي أنشأته على GitHub
# استبدل الرابط برابط مستودعك الجديد
git remote add origin https://github.com/akoasad7-arch/voice-ai-bot.git

# رفع الكود (سيطلب منك اسم المستخدم وكلمة السر/Token)
git push -u origin main

