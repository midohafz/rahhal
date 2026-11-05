// translator.js - ملف الترجمة المركزي لأدلة المدن
document.addEventListener("DOMContentLoaded", function() {
    // 1. حقن أداة الترجمة والزر العصري تلقائياً في الصفحة
    const translateDiv = document.createElement('div');
    translateDiv.innerHTML = `
        <div class="custom-translate-container" style="text-align: left; margin: 15px 20px;">
            <div class="lang-dropdown" style="position: relative; display: inline-block;">
                <button class="globe-btn" style="background: #1e3c72; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-size: 13px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    🌐 Languages ▾
                </button>
                <div class="lang-menu" style="display: none; position: absolute; left: 0; background: white; min-width: 150px; box-shadow: 0px 4px 12px rgba(0,0,0,0.15); border-radius: 8px; z-index: 100; overflow: hidden; margin-top: 5px; border: 1px solid #ddd;">
                    <button onclick="changeLanguage('en')" style="display: block; width: 100%; padding: 10px 15px; background: none; border: none; text-align: left; cursor: pointer; font-size: 13px; font-weight: bold; color: #333;">🇬🇧 English</button>
                    <button onclick="changeLanguage('ru')" style="display: block; width: 100%; padding: 10px 15px; background: none; border: none; text-align: left; cursor: pointer; font-size: 13px; font-weight: bold; color: #333;">🇷🇺 Русский</button>
                    <button onclick="changeLanguage('de')" style="display: block; width: 100%; padding: 10px 15px; background: none; border: none; text-align: left; cursor: pointer; font-size: 13px; font-weight: bold; color: #333;">🇩🇪 Deutsch</button>
                    <button onclick="changeLanguage('fr')" style="display: block; width: 100%; padding: 10px 15px; background: none; border: none; text-align: left; cursor: pointer; font-size: 13px; font-weight: bold; color: #333;">🇫🇷 Français</button>
                    <button onclick="changeLanguage('zh-CN')" style="display: block; width: 100%; padding: 10px 15px; background: none; border: none; text-align: left; cursor: pointer; font-size: 13px; font-weight: bold; color: #333;">🇨🇳 中文</button>
                    <button onclick="changeLanguage('ar')" style="display: block; width: 100%; padding: 10px 15px; background: none; border: none; text-align: left; cursor: pointer; font-size: 13px; font-weight: bold; color: #333; border-top: 1px solid #eee;">🇪🇬 العربية</button>
                </div>
            </div>
        </div>
        <div id="google_translate_element" style="display: none;"></div>
    `;
    
    // وضع الأداة في أعلى محتوى الصفحة مباشرة
    document.body.insertBefore(translateDiv, document.body.firstChild);

    // 2. تحميل سكربت جوجل ترجمة في الخلفية
    const gtScript = document.createElement('script');
    gtScript.type = 'text/javascript';
    gtScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(gtScript);

    // 3. تفعيل التفاعل مع القائمة
    setTimeout(() => {
        const globeBtn = document.querySelector('.globe-btn');
        if(globeBtn) {
            globeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                var menu = this.nextElementSibling;
                menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
            });
        }
    }, 1000);
});

function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'ar', autoDisplay: false}, 'google_translate_element');
}

function changeLanguage(langCode) {
  var selectField = document.querySelector(".goog-te-combo");
  if (selectField) {
    selectField.value = langCode;
    selectField.dispatchEvent(new Event('change'));
  }
}

window.addEventListener('click', function() {
    var menus = document.querySelectorAll('.lang-menu');
    menus.forEach(function(menu) {
        menu.style.display = 'none';
    });
});
