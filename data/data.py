from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QLabel, QLCDNumber

prepositions = {
    "akk": [['bis (до, until)', 0],
            ['durch (через, through)', 0],
            ['für (для, for)', 0],
            ['ohne (без, without)', 0],
            ['gegen (против, against)', 0],
            ['um (вокруг, around)', 0]],
    "akk_dat": [['in (в, in)', 0],
                ['an (в, at)', 0],
                ['auf (на, on)', 0],
                ['neben (рядом с, next to)', 0],
                ['hinter (позади, behind)', 0],
                ['über (выше, above)', 0],
                ['unter (под, under)', 0],
                ['zwischen (между, between)', 0],
                ['vor (до, before)', 0]],
    "dat": [['ab (прочь, away)', 0],
            ['außer (кроме, except)', 0],
            ['zu (к, to)', 0],
            ['nach (после, after)', 0],
            ['bei (в, at)', 0],
            ['von (от, from)', 0],
            ['aus (снаружи, out of)', 0],
            ['mit (с, with)', 0],
            ['seit (с, from)', 0],
            ['gegenüber (противоположный, opposite)', 0]]
}
inderet = ["Wissen Sie, wo ... finde?",
           "Sagen Sie mir bitte, ob der Zug nach Berlin heute Verspätung hat? (Об ставится только когда можно ответить 'да' или 'нет' )"]
