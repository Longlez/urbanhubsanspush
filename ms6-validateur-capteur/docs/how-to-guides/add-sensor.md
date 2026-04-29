# Ajouter un capteur

Pour ajouter un capteur pris en charge par le microservice, modifiez les seuils dans `src/config/sensor_thresholds.py` ou utilisez la logique métier de `SensorValidator.add_sensor`.

Exemple d'ajout :

```python
from src.domain.sensor_validation import SensorValidator
SensorValidator.add_sensor("new-sensor", 100.0, 150.0)
```

Ensuite, testez l'API `POST /validate` avec le nom de capteur ajouté.
