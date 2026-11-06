// translator.js - المحرك الموحد لإصلاح وتتبع روابط الأفلييت وضبط الواجهة
document.addEventListener("DOMContentLoaded", function() {
    // رابط التتبع العام والمصرح به عبر شبكة CJ لـ Booking.com
    const cjAffiliateUrl = "https://www.anrdoezrs.net/click-101918477-15364575";

    // 1. تصحيح جميع روابط الفنادق و Booking.com في صفحات المدن وتوجيهها عبر CJ
    const hotelButtons = document.querySelectorAll("a[href*='booking.com'], .btn-booking");
    hotelButtons.forEach(button => {
        // استثناء الزر العائم الأساسي لتفادي التكرار البرمجي
        if (!button.style.position || button.style.position !== "fixed") {
            button.href = cjAffiliateUrl;
            button.target = "_blank";
            button.rel = "nofollow noopener";
        }
    });

    // 2. تصحيح أزرار "حجز طيران" المضللة وتعديل مسمياتها ووظيفتها
    const flightButtons = document.querySelectorAll(".btn-flight, a[href*='flight']");
    flightButtons.forEach(btn => {
        btn.innerHTML = "🏨 عرض الفنادق والإقامة";
        btn.href = cjAffiliateUrl;
        btn.target = "_blank";
        btn.rel = "nofollow noopener";
    });

    // 3. إنشاء وتثبيت زر الحجز العائم الاحترافي (FAB)
    const fabButton = document.createElement("a");
    fabButton.href = cjAffiliateUrl;
    fabButton.target = "_blank";
    fabButton.rel = "nofollow noopener";
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
