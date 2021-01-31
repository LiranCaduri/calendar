const tolerance = 1;
let last = 0;
let lastIndex = 0;

function setToggle(elementClass, targetElement, classToAdd) {
    alert(lastIndex);
    let allDays = document.getElementsByClassName(elementClass);
    for (let i = lastIndex; i < allDays.length; ++i) {
        allDays[i].addEventListener("click", function () {
            let target = document.getElementById(targetElement);
            target.classList.toggle(classToAdd);
        })
    }
    lastIndex += allDays.length - lastIndex;
}

document.addEventListener(
    'DOMContentLoaded', function () {
        setToggle("day", "day-view", "day-view-visible");
    }
)

function loadWeek(lastDay) {
    if (lastDay != last || last === 0) {
        let path = '/calendar/month/' + lastDay;
        last = lastDay;
        fetch(path).then(function (response) {
            return response.text();
        }).then(function (html) {
            let newDays = document.createElement('html');
            newDays.innerHTML = html;
            document.getElementById("calender-grid").append(newDays);
            setToggle("day", "day-view", "day-view-visible");
        });
    }
}

window.addEventListener(
    'scroll', function () {
        const condition = window.scrollY + window.innerHeight + tolerance >= document.documentElement.scrollHeight;
        if (!condition) {
            return false
        }
        const allDays = document.querySelectorAll('.day');
        const lastDay = allDays[allDays.length - 1].id;
        loadWeek(lastDay);
    }
)