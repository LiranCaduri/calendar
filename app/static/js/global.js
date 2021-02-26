function insertText(targetId, text) {
    const target = document.getElementById(targetId);
    target.innerHTML = text;
}

function openPanel(targetID) {
    const target = document.getElementById(targetID);
    target.classList.toggle("feature-settings-open");
}

function setFeatureInformation(elementID) {
    const id = elementID.split("-").pop();
    // TODO: fetch to get the info and then enter it to the panelInfo array
    const panelId = ["feature-name", "feature-followers", "feature-creator", "feature-info"];
    const panelinfo = ["featuename", 0, "username", "some information about the feature"];
    for (let i = 0; i < panelInfo.length; ++i) {
        insertText(panelId[i], panelinfo[i]);
    }
}

function setFeaturesSettings() {
    const allFeatures = document.getElementsByClassName("feature");
    for (let i = 0; i < allFeatures.length; ++i) {
        allFeatures[i].addEventListener('click', function () {
            openPanel("feature-set-panel", "feature-settings-open");
            const target = document.getElementById("feature-set-panel");
            if (target.classList.contains("feature-settings-closed")) {
                setFeatureInformation(allFeatures[i].id);
            }
        })
    }
}

document.addEventListener(
    'DOMContentLoaded', function () {
        setFeaturesSettings();
    }
)