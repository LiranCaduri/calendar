function setToggle(elementClass, targetElement, classToAdd, lastIndex) {
    const allDays = document.getElementsByClassName(elementClass);
    const target = document.getElementById(targetElement);
    for (let i = lastIndex; i < allDays.length; ++i) {
        allDays[i].addEventListener("click", function () {
            target.classList.toggle(classToAdd);
        })
    }
}

document.addEventListener(
    'DOMContentLoaded', function () {
        setToggle("day", "day-view", "day-view-visible", 0);
    }
)


function loadWeek(lastDay, index) {
    if (lastDay.dataset.last === "false") {
        return false;
    }
    const path = '/calendar/month/' + lastDay.id;
    const newDays = document.createElement("div");
    fetch(path).then(function (response) {
        lastDay.dataset.last = false;
        return response.text();
    }).then(function (html) {
        newDays.innerHTML = html;
        document.getElementById("calender-grid").append(newDays.firstElementChild);
        setToggle("day", "day-view", "day-view-visible", index);
    });
}

window.addEventListener(
    'scroll', function () {
        const tolerance = 1;
        if (window.scrollY + window.innerHeight + tolerance < document.documentElement.scrollHeight) {
            return false;
        }
        const allDays = document.getElementsByClassName('day');
        const lastDay = allDays[allDays.length - 1];
        loadWeek(lastDay, allDays.length);
    }
)