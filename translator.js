(function() {
    // 1. تحميل سكربت جوجل ترجمة تلقائياً
    var googleScript = document.createElement('script');
    googleScript.type = 'text/javascript';
    googleScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.head.appendChild(googleScript);

    // 2. دالة تهيئة جوجل ترجمة (مخفية لمنع الشريط العشوائي)
    window.googleTranslateElementInit = function() {
        new google.translate.TranslateElement({
            pageLanguage: 'ar',
            includedLanguages: 'en,ru,de,fr,zh-CN,ar',
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
    };

    // 3. دالة تغيير اللغة عبر الأزرار المخصصة
    window.changelang = function(lang) {
        var frame = document.querySelector('.goog-te-banner-frame');
        var select = document.querySelector('.goog-te-combo');
        if (select) {
            select.value = lang;
            select.dispatchEvent(new Event('change'));
        }
    };

    // 4. بناء واجهة الأدوات (زر الترجمة المنسدل + محول العملات + زر الحجز العائم)
    window.addEventListener('DOMContentLoaded', function() {
        // حاوية مخفية لمحرك جوجل الأصلي
        var hiddenDiv = document.createElement('div');
        hiddenDiv.id = 'google_translate_element';
        hiddenDiv.style.display = 'none';
        document.body.appendChild(hiddenDiv);

        // شريط الأدوات العلوي الموحد
        var container = document.createElement('div');
        container.className = 'custom-translate-container';
        container.style.cssText = 'text-align: left; margin: 15px 10px; font-family: Tahoma, sans-serif; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;';

        // قائمة اللغات المنسدلة
        var langDropdownHTML = `
            <div style="position: relative; display: inline-block;">
                <button class="globe-btn" onclick="let m=this.nextElementSibling; m.style.display = m.style.display === 'block' ? 'none' : 'block';" style="background: #1e3c72; color: white; border: none; padding: 10px 18px; border-radius: 30px; cursor: pointer; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;">
                    🌐 Languages / Языки
                </button>
                <div class="lang-menu" style="display: none; position: absolute; right: 0; top: 45px; background: white; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); z-index: 1000; min-width: 150px; overflow: hidden;">
                    <button onclick="changelang('ar')" style="width: 100%; padding: 10px; border: none; background: none; text-align: right; cursor: pointer; font-weight: bold;">العربية</button>
                    <button onclick="changelang('en')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer;">English</button>
                    <button onclick="changelang('ru')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer;">Русский</button>
                    <button onclick="changelang('de')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer;">Deutsch</button>
                    <button onclick="changelang('fr')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer;">Français</button>
                    <button onclick="changelang('zh-CN')" style="width: 100%; padding: 10px; border: none; background: none; text-align: left; cursor: pointer;">中文</button>
                </div>
            </div>
        `;

        // أداة محول العملات المبسطة
        var currencyConverterHTML = `
            <div style="display: flex; align-items: center; gap: 5px; background: #f8f9fa; padding: 5px 12px; border-radius: 20px; border: 1px solid #ddd;">
                <span style="font-size: 12px; font-weight: bold; color: #333;">💱 العملة:</span>
                <select id="globalCurrencySelect" onchange="convertCurrency(this.value)" style="border: none; background: transparent; font-size: 13px; cursor: pointer; outline: none;">
                    <option value="EGP">EGP (جنيه)</option>
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                    <option value="SAR">SAR (ريال)</option>
                </select>
            </div>
        `;

        container.innerHTML = langDropdownHTML + currencyConverterHTML;
        
        // إدراج الشريط في بداية الصفحة تلقائياً
        if (document.body.firstChild) {
            document.body.insertBefore(container, document.body.firstChild);
        } else {
            document.body.appendChild(container);
        }

        // إغلاق القائمة عند النقر خارجها
        window.addEventListener('click', function(e) {
            if (!e.target.closest('.globe-btn')) {
                document.querySelectorAll('.lang-menu').forEach(menu => {
                    menu.style.display = 'none';
                });
            }
        });

        // 5. إضافة أيقونة الحجز العائمة (Floating Booking Icon)
        var floatBtn = document.createElement('a');
        floatBtn.href = "#hotels-section"; // يمكنك تعديل الوصلة لرابط الحجز الخاص بك
        floatBtn.innerHTML = "🏨 احجز فندقك الآن";
        floatBtn.style.cssText = "position: fixed; bottom: 20px; right: 20px; background-color: #28a745; color: white; padding: 12px 20px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 9999; font-size: 14px; transition: 0.3s;";
        floatBtn.onmouseover = function() { this.style.backgroundColor = '#218838'; };
        floatBtn.onmouseout = function() { this.style.backgroundColor = '#28a745'; };
        document.body.appendChild(floatBtn);
    });

    // دالة تحويل العملات الوظيفية (تلقائية للتوضيح)
    window.convertCurrency = function(currency) {
        console.log("تم تغيير العملة إلى: " + currency);
        // يمكنك ربطها لاحقاً بتحديث الأسعار الظاهرة في الصفحة بناءً على العملة المختارة
    };
})();
