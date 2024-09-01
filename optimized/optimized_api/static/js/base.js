// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.theme-toggle-button');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');

    if (!sunIcon || !moonIcon) {
        console.error('Icons not found in the document');
        return;
    }

    // Получаем сохранённое состояние темы из localStorage
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.body.classList.add(currentTheme);
        updateIcons(currentTheme);
    }

    // Переключение темы и сохранение в localStorage
    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const theme = document.body.classList.contains('dark-theme') ? '' : 'dark-theme';
            document.body.classList.toggle('dark-theme', theme);
            localStorage.setItem('theme', theme);
            updateIcons(theme);
            
            // Убираем фокус с кнопки
            toggleButton.blur();
        });
    }

    function updateIcons(theme) {
        if (theme === 'dark-theme') {
            sunIcon.style.display = 'inline';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'inline';
        }
    }
});


// Получаем все элементы с классом 'accordion'
var acc = document.getElementsByClassName("accordion");

// Проходим по каждому элементу
for (var i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        // Переключаем класс 'active' для кнопки аккордеона
        this.classList.toggle("active");

        // Получаем следующий элемент после кнопки (это панель)
        var panel = this.nextElementSibling;

        // Переключаем видимость панели
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px"; 
        }

    });
}
