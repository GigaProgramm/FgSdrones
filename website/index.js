let currentLanguage = 'en';

function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
}

function toggleLanguage() {
    if (currentLanguage === 'en') {
        setLanguage('ru');
    } else {
        setLanguage('en');
    }
}

function setLanguage(lang) {
    currentLanguage = lang;
    if (lang === 'ru') {
        document.querySelector('.sidebar a[href="#products"]').innerText = 'Продукты';
        document.querySelector('.sidebar a[href="sim.html"]').innerText = 'Веб симулятор';
        document.querySelector('.sidebar a[href="#progect2"]').innerText = 'Игра на юнити';
        document.querySelector('.sidebar a[href="ide.html"]').innerText = 'Редактор кода для квадрокоптера';
        document.querySelector('.sidebar a[href="about.html"]').innerText = "Докуметация"

        document.getElementById('projects').innerText = 'ПРОЕКТЫ';
        document.getElementById('socialmedia').innerHTML = 'Социальные сети<div class="icons"><a href="https://github.com/ArduRadioKot/FgSdrones/tree/main" target="_blank"><i class="fab fa-github"></i></a><a href="https://discord.com" target="_blank"><i class="fab fa-discord"></i></a><a href="https://telegram.org" target="_blank"><i class="fab fa-telegram"></i></a><a href="https://vk.com" target="_blank"><i class="fab fa-vk"></i></a></div>';
        document.getElementById('footer').innerText = '© 2023 FgSDRONES. Все права защищены.';
    } else {
        document.querySelector('.sidebar a[href="#products"]').innerText = 'Products';
        document.querySelector('.sidebar a[href="#progect1"]').innerText = 'Web simulator';
        document.querySelector('.sidebar a[href="#progect2"]').innerText = 'Unity game';
        document.querySelector('.sidebar a[href="ide.html"]').innerText = 'Ide and drone';
        document.querySelector('.sidebar a[href="about.html"]').innerText = "Documentation"
        document.getElementById('projects').innerText = 'PROGECTS';
        document.getElementById('socialmedia').innerHTML = 'Socialmedia<div class="icons"><a href="https://github.com/ArduRadioKot/FgSdrones/tree/main" target="_blank"><i class="fab fa-github"></i></a><a href="https://discord.com" target="_blank"><i class="fab fa-discord"></i></a><a href="https://telegram.org" target="_blank"><i class="fab fa-telegram"></i></a><a href="https://vk.com" target="_blank"><i class="fab fa-vk"></i></a></div>';
        document.getElementById('footer').innerText = '© 2023 FgSDRONES. All rights reserved.';
    }
}