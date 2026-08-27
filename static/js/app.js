const dataElement =
    document.getElementById("mausam-data");


const mausamData =
    dataElement
        ? JSON.parse(dataElement.textContent)
        : {};



/* =========================
   DOM ELEMENTS
   ========================= */

const insightTitle =
    document.getElementById(
        "insight-title"
    );

const score =
    document.getElementById(
        "score"
    );

const scoreProgress =
    document.getElementById(
        "score-progress"
    );

const bestTime =
    document.getElementById(
        "best-time"
    );

const insightIcon =
    document.querySelector(
        ".insight-icon"
    );



/* =========================
   PERSONA LABELS
   ========================= */

const personaLabels = {

    fitness:
        "FITNESS SCORE",

    health:
        "HEALTH SCORE",

    travel:
        "TRAVEL SCORE",

    commute:
        "COMMUTE SCORE",

    beach:
        "BEACH SCORE",

    family:
        "FAMILY SCORE",

    agriculture:
        "AGRICULTURE SCORE",

    events:
        "EVENT SCORE"

};



/* =========================
   UPDATE RECOMMENDATIONS
   ========================= */

function updateRecommendations(
    persona
) {

    const data =
        mausamData[persona];


    if (!data) {

        console.warn(
            "No personalization data for:",
            persona
        );

        return;

    }


    insightTitle.textContent =
        data.title;


    score.textContent =
        data.score;


    scoreProgress.style.width =
        `${data.score}%`;


    bestTime.textContent =
        data.best_time;


    insightIcon.textContent =
        data.icon;


    data.cards.forEach(
        (card, index) => {

            const number =
                index + 1;


            const icon =
                document.getElementById(
                    `rec-icon-${number}`
                );


            const title =
                document.getElementById(
                    `rec-title-${number}`
                );


            const text =
                document.getElementById(
                    `rec-text-${number}`
                );


            if (!icon ||
                !title ||
                !text) {

                return;

            }


            icon.textContent =
                card.icon;


            icon.className =
                `recommendation-icon ${card.type}`;


            title.textContent =
                card.title;


            text.textContent =
                card.text;

        }
    );


    updateScoreLabel(
        persona
    );

}



/* =========================
   UPDATE SCORE LABEL
   ========================= */

function updateScoreLabel(
    persona
) {

    const label =
        document.querySelector(
            ".insight-score span"
        );


    if (!label) {
        return;
    }


    label.textContent =
        personaLabels[persona] ||
        "PERSONALIZED SCORE";

}



/* =========================
   PERSONA BUTTONS
   ========================= */

function setupPersonaButtons() {

    const personaButtons =
        document.querySelectorAll(
            ".persona"
        );


    personaButtons.forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    personaButtons.forEach(
                        btn => {

                            btn.classList.remove(
                                "active"
                            );

                        }
                    );


                    button.classList.add(
                        "active"
                    );


                    const selectedPersona =
                        button.dataset.persona;


                    updateRecommendations(
                        selectedPersona
                    );

                }
            );

        }
    );


    return personaButtons;

}



/* =========================
   DYNAMIC PERSONA FUNCTION
   ========================= */

window.updatePersona =
    function(persona) {

        updateRecommendations(
            persona
        );

    };



/* =========================
   INITIALIZE
   ========================= */

const personaButtons =
    setupPersonaButtons();


if (personaButtons.length > 0) {

    const activeButton =
        document.querySelector(
            ".persona.active"
        );


    if (activeButton) {

        updateRecommendations(
            activeButton.dataset.persona
        );

    }

}