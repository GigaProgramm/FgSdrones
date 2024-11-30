let currentLanguage = 'en';

function openNav(event) {
    event.stopPropagation();
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
    } else {
        document.querySelector('.sidebar a[href="#products"]').innerText = 'Products';
        document.querySelector('.sidebar a[href="sim.html"]').innerText = 'Web simulator';
        document.querySelector('.sidebar a[href="#progect2"]').innerText = 'Unity game';
        document.querySelector('.sidebar a[href="ide.html"]').innerText = 'Ide and drones';
    }
}