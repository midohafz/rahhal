document.addEventListener("DOMContentLoaded", function() {
    // 1. رابط التتبع العام والمصرح به عبر شبكة CJ لـ Booking.com
    const cjAffiliateUrl = "https://www.anrdoezrs.net/click-101918477-15364575";

    // 2. تصحيح جميع روابط الفنادق و Booking.com في صفحات المدن
    const hotelButtons = document.querySelectorAll("a[href*='booking.com'], .btn-booking");
    hotelButtons.forEach(button => {
        if (!button.style.position || button.style.position !== "fixed") {
            button.href = cjAffiliateUrl;
            button.target = "_blank";
            button.rel = "nofollow noopener sponsored";
        }
    });

    // 3. معالجة وتعديل أزرار الطيران المضللة لتعكس خدمات الإقامة بدقة
    const flightButtons = document.querySelectorAll(".btn-flight, a[href*='flight']");
    flightButtons.forEach(btn => {
        btn.innerHTML = "🏨 عرض الفنادق والإقامة";
        btn.href = cjAffiliateUrl;
        btn.target = "_blank";
        btn.rel = "nofollow noopener sponsored";
    });
    
    // أيضاً البحث عن الأزرار بالاعتماد على النص العربي
    document.querySelectorAll("a").forEach(a => {
        if (a.innerText.includes("حجز طيران") || a.innerText.includes("طيران")) {
            a.innerHTML = "🏨 عرض الفنادق والإقامة";
            a.href = cjAffiliateUrl;
            a.target = "_blank";
            a.rel = "nofollow noopener sponsored";
        }
    });

    // 4. تفعيل الخطوة 3: إدراج تذييل إفصاح العمولة تلقائياً أسفل الصفحة
    if (!document.getElementById("rahhal-footer-disclosure")) {
        const footerDiv = document.createElement("footer");
        footerDiv.id = "rahhal-footer-disclosure";
        footerDiv.style.cssText = "background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 13px; color: #6c757d; border-top: 1px solid #e9ecef; margin-top: 40px; direction: rtl;";
        footerDiv.innerHTML = `
            <p style="margin-bottom: 8px;"><strong>إفصاح الشفافية:</strong> يحتوي هذا الموقع على روابط تسويق بالعمولة (Affiliate Links). عند النقر على هذه الروابط وإجراء حجز، قد نتحصل على عمولة بسيطة من منصة Booking.com دون أي تكلفة إضافية عليك. يساعدنا هذا في استمرار تقديم الأدلة السياحية المجانية.</p>
            <p style="margin: 0;">© 2026 رحال للسفر والسياحة - جميع الحقوق محفوظة</p>
        `;
        document.body.appendChild(footerDiv);
    }

    // 5. إنشاء زر الحجز العائم (FAB)
    const fabButton = document.createElement("a");
    fabButton.href = cjAffiliateUrl;
    fabButton.target = "_blank";
    fabButton.rel = "nofollow noopener sponsored";
    fabButton.innerHTML = "🏨 احجز فندقك الآن";
    
    fabButton.style.position = "fixed";
    fabButton.style.bottom = "20px";
    fabButton.style.right = "20px";
    fabButton.style.backgroundColor = "#003580";
    fabButton.style.color = "#ffffff";
    fabButton.style.padding = "12px 20px";
    fabButton.style.borderRadius = "30px";
    fabButton.style.boxShadow = "0 4px 10px rgba(0,0,0,0.3)";
    fabButton.style.fontFamily = "Arial, sans-serif";
    fabButton.style.fontWeight = "bold";
    fabButton.style.fontSize = "15px";
    fabButton.style.zIndex = "9999";
    fabButton.style.textDecoration = "none";
    fabButton.style.transition = "background-color 0.3s ease";

    fabButton.onmouseover = function() {
        fabButton.style.backgroundColor = "#00224f";
    };
    fabButton.onmouseout = function() {
        fabButton.style.backgroundColor = "#003580";
    };

    document.body.appendChild(fabButton);
});
