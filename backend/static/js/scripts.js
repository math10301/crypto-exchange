// Переключение темы (светлая/тёмная)
document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
    }

    themeToggle.addEventListener("click", function() {
        body.classList.toggle("dark-mode");
        localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
    });
});

// Обновление баланса пользователя
function updateBalance(newBalance) {
    document.getElementById("balance").textContent = `$${newBalance}`;
}

// Динамическое обновление курса криптовалют (пример)
function updateMarketData() {
    const prices = document.querySelectorAll(".crypto-price");
    prices.forEach(price => {
        let randomChange = (Math.random() * 2 - 1).toFixed(2); // Генерация случайного изменения
        let currentPrice = parseFloat(price.textContent.replace("$", ""));
        price.textContent = `$${(currentPrice + parseFloat(randomChange)).toFixed(2)}`;
    });
}

setInterval(updateMarketData, 5000); // Обновление каждые 5 сек