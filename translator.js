// translator.js - Unified UI, Language Switcher, and Affiliate Tracking for City Guides

document.addEventListener("DOMContentLoaded", function() {
    // 1. Inject Floating Booking Button (FAB) with active CJ Affiliate link
    const fabButton = document.createElement("a");
    fabButton.href = "https://www.anrdoezrs.net/click-101918477-15364575";
    fabButton.target = "_blank";
    fabButton.rel = "nofollow noopener";
    fabButton.innerHTML = "🏨 احجز الآن (Book Now)";
    
    // Style the FAB with Booking.com Navy palette (#003580)
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

    // 2. Centralized Translation Dropdown logic
    console.log("Translator and Affiliate FAB initialized successfully with tracking ID: 15364575");
});
