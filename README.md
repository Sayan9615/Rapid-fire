# 🎯 Rapid Fire

Rapid Fire este un joc arcade creat în Python folosind biblioteca Pygame.

---

## 🕹️ Reguli joc

1. Țintește și trage cu click stânga pe țintele care apar.
2. Țintele eliminate oferă puncte în funcție de nivel.
3. Fiecare țintă eliminată îți oferă **+3 secunde** bonus la timp.
4. Când ai **o singură viață**, există **10% șansă** să apară o inimă. Dacă o lovești, primești +1 viață (maxim 5).
5. Dacă ratezi (tragi pe lângă sau scapă o țintă), pierzi o viață.
6. Jocul se termină când timpul expiră sau rămâi fără vieți.
7. La fiecare 100 de puncte, nivelul crește și jocul devine mai rapid și mai greu.

---

## 📋 Clasament

- Scorurile sunt salvate automat în fișierul leaderboard.json.
- Este păstrat **top 10**.
- Dacă joci cu același nume, doar cel mai bun scor este salvat.

---

## ✅ Instalare

### Varianta 1 – Clonează proiectul

bash
git clone https://github.com/Sayan9615/Rapid-fire.git
cd Rapid-fire

###**Varianta 2 – Descarcă proiectul**

1.Accesează https://github.com/Sayan9615/Rapid-fire

2.Apasă pe butonul verde Code → Download ZIP

3.Extrage arhiva pe calculatorul tău

4.Deschide folderul Rapid-fire

**Rulare joc**

1.Asigură-te că ai instalat Python 3

2.Instalează biblioteca Pygame cu comanda:
  pip install pygame

3.Rulează jocul cu:
  python main.py

