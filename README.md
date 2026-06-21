# IoT Okos Öntözőrendszer

Talajnedvesség-mérő és automata öntöző rendszer ESP32-vel. A mikrokontroller
óránként méri a talaj nedvességét, és ha az egy küszöbérték alá esik,
lokálisan bekapcsolja a szivattyút. Nap végén elküldi a napi átlagos
nedvességértéket egy Python szervernek, amely MariaDB-be menti.

## Felépítés

```
okos-ontozo/
├── docker-compose.yml
├── .env.example
├── mariadb-init/
│   └── 01_schema.sql
├── server/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── esp32/
    ├── main.py
    ├── config.py
    ├── wifi_manager.py
    ├── sensors.py
    └── api_client.py
```

## Működés

- Az ESP32 óránként mérést végez (`MEASURE_INTERVAL_SECONDS`).
- Ha a nedvesség a küszöb (`MOISTURE_THRESHOLD_PERCENT`) alá esik, és a
  szivattyú nincs lehűlési időben, az ESP32 lokálisan bekapcsolja a
  szivattyút (`PUMP_RUN_SECONDS`-ig).
- A napi mérések átlagát az ESP32 helyben számolja.
- Amikor új napra ér, elküldi az előző nap átlagát egyetlen HTTP POST
  kéréssel a szervernek.
- A szerver a `daily_moisture` táblába menti (eszköz + dátum szerint
  egyedi sorként).

## Indítás

1. `.env` létrehozása `.env.example` alapján.
2. Indítás:

```bash
docker compose up -d --build
```

3. Ellenőrzés:

```bash
curl http://localhost:5000/health
```

## ESP32 feltöltés

1. MicroPython firmware az ESP32-re flashelve.
2. `config.py`-ban WiFi adatok, `SERVER_URL` (a szervert futtató gép IP-je),
   `API_TOKEN` kitöltése.
3. Fájlok feltöltése (pl. `mpremote`):

```bash
mpremote connect /dev/ttyUSB0 cp config.py wifi_manager.py sensors.py api_client.py main.py :
mpremote connect /dev/ttyUSB0 run main.py
```

## API

`POST /api/v1/daily-moisture`

```json
{
  "device_uid": "esp32-balkon-01",
  "date": "2026-06-21",
  "avg_moisture": 42.5
}
```

Header: `Authorization: Bearer <API_TOKEN>`
