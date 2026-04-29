# Contrats d'API

## POST /validate

Reçoit une donnée capteur valide et retourne la classification.

### Requête

```json
{
  "sensor": "co2",
  "value": 500
}
```

### Réponse

```json
{
  "sensor": "co2",
  "value": 500.0,
  "valid": true,
  "level": "normal",
  "threshold": 800.0,
  "message": "Valeur normale.",
  "timestamp": "2026-04-27T09:00Z"
}
```

## POST /traffic/validate

Reçoit une fenêtre de trafic, enrichit la charge et publie le message validé vers `validated_queue`.

### Requête

```json
{
  "window_id": "window-123",
  "vehicle_count": 720,
  "timestamp": "2026-04-27T09:00Z",
  "location": "zone-1"
}
```

### Réponse

```json
{
  "window_id": "window-123",
  "vehicle_count": 720.0,
  "timestamp": "2026-04-27T09:00Z",
  "location": "zone-1",
  "validated": true,
  "traffic_level": "moderate",
  "validated_timestamp": "2026-04-27T09:00Z"
}
```
