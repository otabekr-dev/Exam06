# ♟️ Chess Rating System API

**Professional Chess Rating Platform — Backend System**

---

## Loyiha Haqida

Bu loyiha **shaxmat reytingi va turnir tizimi** uchun backend API bo'lib, Chess.com va Lichess.org kabi platformalar prinsiplariga asoslangan.

**Muhim:** Authentication talab qilinmaydi — barcha endpointlar ochiq (public access).

Tizim **Game (Turnir)**, **Player (Shaxmatchi)**, va **Score (Partiya natijasi)** ma'lumotlarini boshqaradi, hamda **Rating System** va **Leaderboard** funksiyalarini qo'llab-quvvatlaydi.

---

## 📂 Loyiha Strukturasi

```
/
├── core/                    # Project: Asosiy project
├── games/                   # App: Turnirlar moduli
├── players/                 # App: Shaxmatchilar moduli
├── scores/                  # App: Partiyalar va natijalar
├── leaderboard/             # App: Rating va statistika
```

---

## Ma'lumotlar Bazasi Modellari

### **1. Game Model** (`games/models.py`)

Shaxmat turnirlari haqida ma'lumot.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | AutoField | Primary key | Auto-generated |
| `title` | CharField(200) | Turnir nomi | **Required**, max_length=200 |
| `location` | CharField(100) | O'tkazilish joyi | **Required** |
| `start_date` | DateField | Boshlanish sanasi | **Required** |
| `description` | TextField | Tavsif | Optional, blank=True, null=True |
| `created_at` | DateTimeField | Yaratilgan vaqt | auto_now_add=True |

**Model xususiyatlari:**
- `__str__` metodi `title` qaytaradi
- O'chirishdan oldin unga bog'liq score'lar tekshiriladi
- Meta class: ordering by `-created_at`

---

### **2. Player Model** (`players/models.py`)

Shaxmatchilar profili va reytingi.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | AutoField | Primary key | Auto-generated |
| `nickname` | CharField(50) | Shaxmatchi nomi | **Required**, **unique** |
| `country` | CharField(50) | Mamlakat | **Required** |
| `rating` | IntegerField | Joriy reyting | Default: 0 |
| `created_at` | DateTimeField | Ro'yxatdan o'tgan vaqt | auto_now_add=True |

**Model xususiyatlari:**
- `nickname` unique bo'lishi shart
- `__str__` metodi `nickname` qaytaradi
- `rating` avtomatik yangilanadi har partiyadan keyin

---

### **3. Score Model** (`scores/models.py`)

Shaxmat partiyalari natijalari.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | AutoField | Primary key | Auto-generated |
| `game` | ForeignKey | Turnirga bog'lanish | **Required**, on_delete=PROTECT |
| `player` | ForeignKey | Shaxmatchiga bog'lanish | **Required**, on_delete=PROTECT |
| `result` | CharField(10) | Partiya natijasi | Choices: 'win', 'loss', 'draw' |
| `points` | IntegerField | Partiya oldidan reyting |  |
| `opponent_name` | CharField(50) | Raqib ismi | Optional |
| `created_at` | DateTimeField | Natija kiritilgan vaqt | auto_now_add=True |

**Model xususiyatlari:**
- Bir player bir game uchun **ko'p marta** score qo'shishi mumkin (har xil raqiblar bilan)
- Meta class: ordering by `-created_at`

**Result qiymatlari:**
- `win`: G'alaba (10 ball)
- `draw`: Durang (5 ball)
- `loss`: Mag'lubiyat (0 ball)

---

## API Endpointlari

### **Base URL:** `http://localhost:8000/api/`

---

## ♟️ Game (Turnir) Endpoints

### **1. Create Game**
```http
POST /api/games/
Content-Type: application/json

{
  "title": "Tashkent Rapid Championship 2025",
  "location": "Tashkent, Uzbekistan",
  "start_date": "2025-12-15",
  "description": "Open tournament for all ratings"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Tashkent Rapid Championship 2025",
  "location": "Tashkent, Uzbekistan",
  "start_date": "2025-12-15",
  "description": "Open tournament for all ratings",
  "created_at": "2025-11-24T10:30:00Z"
}
```

---

### **3. Retrieve Game**
```http
GET /api/games/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Tashkent Rapid Championship 2025",
  "location": "Tashkent, Uzbekistan",
  "start_date": "2025-12-15",
  "description": "Open tournament for all ratings",
  "created_at": "2025-11-24T10:30:00Z"
}
```

---

### **4. Update Game**
```http
PATCH /api/games/{id}/
Content-Type: application/json

{
  "description": "Updated tournament info"
}
```

---

### **5. Delete Game**
```http
DELETE /api/games/{id}/
```

**Response (400 Bad Request):** — Agar score'lar mavjud bo'lsa:
```json
{
  "error": "Cannot delete game with existing scores. Tournament has active games."
}
```

---

## 👤 Player (Shaxmatchi) Endpoints

### **1. Create Player**
```http
POST /api/players/
Content-Type: application/json

{
  "nickname": "ChessMaster",
  "country": "Uzbekistan",
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "nickname": "ChessMaster",
  "country": "Uzbekistan",
  "rating": 0,
  "created_at": "2025-11-24T11:00:00Z"
}
```

**Validatsiyalar:**
- `nickname` unique bo'lishi shart

---

### **2. List Players**
```http
GET /api/players/
```

**Query Parameters:**
- `country` — mamlakat bo'yicha
- `min_rating` — minimal reyting
- `search` — nickname bo'yicha qidiruv

**Examples:**
```http
GET /api/players/?country=uzbekistan
GET /api/players/?min_rating=2000
GET /api/players/?search=master
```

**Response (200 OK):**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nickname": "ChessMaster",
      "country": "Uzbekistan",
      "rating": 1850,
      "total_games": 45,
      "wins": 28,
      "draws": 10,
      "losses": 7,
      "created_at": "2025-11-24T11:00:00Z"
    }
  ]
}
```

---

### **3. Retrieve Player**
```http
GET /api/players/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "nickname": "ChessMaster",
  "country": "Uzbekistan",
  "rating": 1850,
  "total_games": 45,
  "wins": 28,
  "draws": 10,
  "losses": 7,
  "created_at": "2025-11-24T11:00:00Z"
}
```

---

### **4. Update Player**
```http
PATCH /api/players/{id}/
Content-Type: application/json

{
  "country": "Kazakhstan"
}
```

---

### **5. Delete Player**
```http
DELETE /api/players/{id}/
```

**Response (400 Bad Request):** — Agar score'lar mavjud bo'lsa:
```json
{
  "error": "Cannot delete player with game history. Player has 45 recorded games."
}
```

---

## 🏆 Score (Partiya natijasi) Endpoints

### **1. Create Score**
```http
POST /api/scores/
Content-Type: application/json

{
  "game": 1,
  "player": 3,
  "result": "win",
  "opponent_name": "GrandMaster",
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "game": {
    "id": 1,
    "title": "Tashkent Rapid Championship 2025"
  },
  "player": {
    "id": 3,
    "nickname": "ChessMaster"
  },
  "result": "win",
  "points": +10,
  "opponent_name": "GrandMaster",
  "created_at": "2025-11-24T12:00:00Z"
}
```

**Validatsiyalar:**
- `result` faqat: win, draw, loss
- Rating avtomatik hisoblanadi

---

### **2. List Scores**
```http
GET /api/scores/
```

**Query Parameters:**
- `game_id` — turnir bo'yicha
- `player_id` — shaxmatchi bo'yicha
- `result` — natija bo'yicha (win, draw, loss)

**Examples:**
```http
GET /api/scores/?game_id=1
GET /api/scores/?player_id=3&result=win
```

**Response (200 OK):**
```json
{
  "count": 120,
  "results": [
    {
      "id": 1,
      "game": {
        "id": 1,
        "title": "Tashkent Rapid Championship 2025"
      },
      "player": {
        "id": 3,
        "nickname": "ChessMaster"
      },
      "result": "win",
      "points": 10,
      "opponent_name": "GrandMaster",
      "created_at": "2025-11-24T12:00:00Z"
    }
  ]
}
```

---

### **3. Retrieve Score**
```http
GET /api/scores/{id}/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "game": {
    "id": 1,
    "title": "Tashkent Rapid Championship 2025",
    "location": "Tashkent"
  },
  "player": {
    "id": 3,
    "nickname": "ChessMaster",
    "country": "Uzbekistan"
  },
  "result": "win",
  "points": 1850,
  "opponent_name": "GrandMaster",
  "created_at": "2025-11-24T12:00:00Z"
}
```

---

### **4. Delete Score**
```http
DELETE /api/scores/{id}/
```

**Response (204 No Content)**

**Eslatma:** Score o'chirilganda player reytingi qayta hisoblanadi.

---

## 🏆 Leaderboard Endpoints

### **1. Game Leaderboard**
```http
GET /api/leaderboard/?game_id={id}
```

**Query Parameters:**
- `game_id` — **Majburiy** — qaysi turnir uchun leaderboard

**Business Logic:**
1. Faqat bitta turnir uchun barcha score'larni olish
2. Har bir player uchun jami ballni hisoblash (win=10, draw=5, loss=0)
3. Ball bo'yicha **kamayish tartibi**da saralash
4. Reyting o'zgarishini ko'rsatish

**Example:**
```http
GET /api/leaderboard/?game_id=1
```

**Response (200 OK):**
```json
[
  {
    "rank": 1,
    "player": "ChessMaster",
    "player_id": 3,
    "country": "Uzbekistan",
    "rating": 1878,
    "points": 75,
    "wins": 7,
    "draws": 1,
    "losses": 1,
    "rating_change": +75
  },
  {
    "rank": 2,
    "player": "GrandMaster",
    "player_id": 7,
    "country": "Russia",
    "rating": 2150,
    "points": 70,
    "wins": 6,
    "draws": 2,
    "losses": 1,
    "rating_change": +70
  }
]
```

---

### **2. Top Players Leaderboard**
```http
GET /api/leaderboard/top/?game_id={id}&limit={n}
```

**Query Parameters:**
- `game_id` — **Majburiy**
- `limit` — Top N ta player (default: 10, max: 50)

**Example:**
```http
GET /api/leaderboard/top/?game_id=1&limit=5
```

**Response (200 OK):**
```json
{
  "game_id": 1,
  "game_title": "Tashkent Rapid Championship 2025",
  "limit": 5,
  "total_players": 24,
  "leaderboard": [
    {
      "rank": 1,
      "player": "ChessMaster",
      "country": "Uzbekistan",
      "rating": 1878,
      "points": 75
    }
  ]
}
```

---

### **3. Global Rating Leaderboard**
```http
GET /api/leaderboard/global/
```

Barcha shaxmatchilar reytingi bo'yicha.

**Query Parameters:**
- `country` — mamlakat bo'yicha filterlash
- `limit` — top N (default: 100, max: 500)

**Example:**
```http
GET /api/leaderboard/global/?country=uzbekistan&limit=20
```

**Response (200 OK):**
```json
{
  "total_players": 156,
  "country": "Uzbekistan",
  "leaderboard": [
    {
      "rank": 1,
      "player": "ChessMaster",
      "rating": 2250,
      "total_games": 145,
    }
  ]
}
```

---

## 🔍 Filtering & Search

### **Game Filtering**
- `search` — title bo'yicha
- `location` — joy bo'yicha

### **Player Filtering**
- `country` — mamlakat bo'yicha
- `min_rating` — minimal reyting
- `search` — nickname bo'yicha

### **Score Filtering**
- `game_id` — turnir bo'yicha
- `player_id` — shaxmatchi bo'yicha
- `result` — win, draw, loss

---


## 📚 Foydali Resurslar

- [Django Documentation](https://docs.djangoproject.com/)
- [ELO Rating System](https://en.wikipedia.org/wiki/Elo_rating_system)
- [Chess.com](https://www.chess.com/)
- [Lichess.org](https://lichess.org/)

---

## 🎉 Omad Tilaymiz!

Bu imtihon sizni **real-world chess platform backend**ga tayyorlash uchun mo'ljallangan.
