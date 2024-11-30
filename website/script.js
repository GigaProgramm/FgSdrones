let currentLanguage = 'en';
let downloadCount = 0;

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
        document.querySelector('.sidebar a[href="#progect3"]').innerText = 'Редактор кода для квадрокоптера';
        document.querySelector('.about').innerText = 'О нас';
        document.querySelector('.download-section p').innerText = 'скачано: ' + downloadCount + ' раз';
    } else {
        document.querySelector('.sidebar a[href="#products"]').innerText = 'Products';
        document.querySelector('.sidebar a[href="sim.html"]').innerText = 'Web simulator';
        document.querySelector('.sidebar a[href="#progect2"]').innerText = 'Unity game';
        document.querySelector('.sidebar a[href="#progect3"]').innerText = 'Ide and drones';
        document.querySelector('.about').innerText = 'About';
        document.querySelector('.download-section p').innerText = 'downloaded: ' + downloadCount + ' times';
    }
}

function incrementDownloadCount() {
    downloadCount++;
    document.getElementById('download-count').innerText = downloadCount;
    if (currentLanguage === 'ru') {
        document.querySelector('.download-section p').innerText = 'скачано: ' + downloadCount + ' раз';
    } else {
        document.querySelector('.download-section p').innerText = 'downloaded: ' + downloadCount + ' times';
    }
}

function switchImage(imageUrl) {
    document.getElementById('main-image').src = imageUrl;
}