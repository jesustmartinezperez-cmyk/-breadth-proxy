# Breadth Rule Proxy

Réplica no oficial del BofA Breadth Rule de Michael Hartnett: % de índices
bursátiles globales que cotizan por encima de su SMA50 y SMA200 a la vez.

## Qué es y qué NO es

- **Es**: una serie diaria propia, calculada con datos públicos (yfinance),
  sobre un universo de 21 índices país/región definido por nosotros.
- **NO es**: el dato oficial de BofA. Hartnett no publica su universo
  exacto de índices ni su metodología completa, así que este número
  no va a coincidir con el suyo cifra a cifra. Sirve para ver tendencia
  y contrastar contra el dato real cuando sale (semanal, en el Flow Show).

## Umbrales de referencia (BofA, dato con fuente de agosto 2026)

- Sobrecompra generalizada: **82%** (nivel citado por Hartnett en esa fecha)
- Señal de venta: se dispara al cruzar **88%**
- A esa fecha, China, India y Brasil eran los únicos grandes mercados
  que NO estaban en sobrecompra

Estos umbrales son del dato oficial, no necesariamente aplicables 1:1
al proxy — el proxy puede moverse en rangos distintos por tener un
universo de índices distinto.

## Estructura

- `breadth.py` — script de cálculo
- `data/breadth_history.csv` — serie histórica diaria (lo que lee la tarea programada)
- `data/detail_YYYY-MM-DD.csv` — detalle diario por país
- `.github/workflows/breadth.yml` — cron diario (L-V, 22:00 UTC)

## Setup

1. Crear repo en GitHub y subir este contenido
2. Settings → Actions → General → Workflow permissions → "Read and write permissions"
3. Lanzar manualmente el workflow una vez (workflow_dispatch) para generar el primer dato
4. Verificar que `data/breadth_history.csv` se ha creado y tiene una fila
