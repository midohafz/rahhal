document.addEventListener("DOMContentLoaded", function() {
    const affiliateUrl = "https://www.anrdoezrs.net/click-101918477-15364575";

    // 1. تحديث أزرار الحجز الخاصة بالفنادق داخل الصفحة تلقائياً
    const hotelBookingButtons = document.querySelectorAll(".btn-booking, a[href*='booking.com']");
    hotelBookingButtons.forEach(button => {
        // استثناء الزر العائم حتى لا يحدث تداخل إذا تم تعريفه بفئة أخرى
        if (!button.style.position || button.style.position !== "fixed") {
            button.href = affiliateUrl;
            button.target = "_blank";
            button.rel = "nofollow noopener";
        }
    });

    // 2. إنشاء زر الحجز العائم (FAB)
    const fabButton = document.createElement("a");
    fabButton.href = affiliateUrl;
    fabButton.target = "_blank";
    fabButton.rel = "nofollow noopener";
    fabButton.innerHTML = "🏨 احجز الآن (Book Now)";
    
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
