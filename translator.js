(function() {
    // 1. تحميل سكربت جوجل ترجمة تلقائياً
    var googleScript = document.createElement('script');
    googleScript.type = 'text/javascript';
    googleScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.head.appendChild(googleScript);

    // 2. تهيئة محرك الترجمة
    window.googleTranslateElementInit = function() {
        new google.translate.TranslateElement({
            pageLanguage: 'ar',
            includedLanguages: 'en,ru,de,fr,zh-CN,ar',
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
    };

    // 3. دالة تبديل اللغة
    window.changelang = function(lang) {
        var select = document.querySelector('.goog-te-combo');
        if (select) {
            select.value = lang;
            select.dispatchEvent(new Event('change'));
        }
    };

    // 4. إدراج زر الترجمة وأيقونة الحجز العائمة بعد تحميل الصفحة
    window.addEventListener('DOMContentLoaded', function() {
        // عنصر جوجل المخفي
        var hiddenDiv = document.createElement('div');
        hiddenDiv.id = 'google_translate_element';
        hiddenDiv.style.display = 'none';
        document.body.appendChild(hiddenDiv);

        // حاوية زر الترجمة
        var container = document.createElement('div');
        container.className = 'custom-translate-container';
        container.style.cssText = 'text-align: left; margin: 15px 10px; font-family: Tahoma, sans-serif;';

        // زر اختيار اللغة المنسدل (بدون كلمة روسية)
        container.innerHTML = `
            <div style="position: relative; display: inline-block;">
                <button class="globe-btn" onclick="let m=this.nextElementSibling; m.style.display = m.style.display === 'block' ? 'none' : 'block';" style="background: #1e3c72; color: white; border: none; padding: 10px 18px; border-radius: 30px; cursor: pointer; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-weight: bold;">
                    🌐 اللغة / Language
                </button>
                <div class="lang-menu" style="display: none; position: absolute; left: 0; top: 45px; background: white; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); z-index: 1000; min-width: 150px; overflow: hidden;">
                    <button onclick="changelang('ar')" style="width: 100%; padding: 10px; border: none; background: none; text-align: right; cursor: pointer; font-weight: bold; border-bottom: 1px solid #eee;">العربية</button>
                    <button onclick="changelang('en')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer; border-bottom: 1px solid #eee;">English</button>
                    <button onclick="changelang('ru')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer; border-bottom: 1px solid #eee;">Русский</button>
                    <button onclick="changelang('de')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer; border-bottom: 1px solid #eee;">Deutsch</button>
                    <button onclick="changelang('fr')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer; border-bottom: 1px solid #eee;">Français</button>
                    <button onclick="changelang('zh-CN')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer;">中文</button>
                </div>
            </div>
        `;
        
        // إدراج زر الترجمة أعلى الصفحة
        if (document.body.firstChild) {
            document.body.insertBefore(container, document.body.firstChild);
        } else {
            document.body.appendChild(container);
        }

        // إغلاق القائمة عند النقر في أي مكان خارجها
        window.addEventListener('click', function(e) {
            if (!e.target.closest('.globe-btn')) {
                document.querySelectorAll('.lang-menu').forEach(function(menu) {
                    menu.style.display = 'none';
                });
            }
        });

        // 5. أيقونة الحجز العائمة الذكية (تفتح رابط الحجز المباشر في نافذة جديدة)
        var floatBtn = document.createElement('a');
        floatBtn.href = "https://www.anrdoezrs.net/click-101918477-13833777"; // رابط الحجز بالعمولة الخاص بك
        floatBtn.target = "_blank"; // فتح الرابط في نافذة جديدة
        floatBtn.rel = "nofollow sponsored";
        floatBtn.innerHTML = "🏨 احجز الفندق الآن / Book Now";
        floatBtn.style.cssText = "position: fixed; bottom: 20px; right: 20px; background-color: #003580; color: white; padding: 12px 22px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 9999; font-size: 14px; font-family: sans-serif; transition: 0.3s;";
        
        floatBtn.onmouseover = function() { this.style.backgroundColor = '#00224f'; };
        floatBtn.onmouseout = function() { this.style.backgroundColor = '#003580'; };
        
        document.body.appendChild(floatBtn);
    });
})();
