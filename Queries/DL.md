# <ins>Mobile Applications Ontology: DL Queries</ins>
Once the ontology is complete, you can query the model created for a better understanding of the classification.
This section shows some <ins>**DL queries**</ins> used to extrapolate important results.

### 1) Applications developed for iOS, native, which require GPS:

```
AppCategory 
and developedFor value iOS 
and hasAppTypology value Native
and requires value GPS
```

#### Result

|   Instances  |
|:------------:|
|     Fancy    |
|   FoodPanda  |
|  Foursquare  |
|  GoogleMaps  |
|  NikeRunning |
| RuntasticPro |

### 2) Applications released between 2016 and 2021:

```
AppCategory and 
(firstVersionReleaseDate some xsd:dateTime[>=2016-01-01T00:00:00 ]) 
and 
(firstVersionReleaseDate some xsd:dateTime[<=2021-01-01T00:00:00 ])
```

#### Results

| Instances |
|:---------:|
|  Facebook |
|  GoodTask |
| PaypalApp |
|  Shapr3D  |
|   Shazam  |

### 3) Application that requires some Device Access:

```
AppCategory and 
(
    (requires value Accelerometer) or (requires value GPS)
    or (requires value Camera) or (requires value Microphone)
)
```

#### Result

|       Instances       |
|:---------------------:|
|       CouchTo5k       |
|         Fancy         |
|       FoodPanda       |
|       Foursquare      |
|       GoogleMaps      |
|      NikeRunning      |
| PerformanceStretching |
|      RuntasticPro     |
|        Shapr3D        |
|         Shazam        |

### 4) Totally free Android applications (which are free in the store and do not allow in-app purchases) written in Java:

```
AppCategory 
and (hasInAppPurchase value false)
and (developedFor value Android) 
and (hasFrontendLanguage value Java)
and (price value 0.0f)
```

#### Result

|   Instances  |
|:------------:|
|   Whatsapp   |
| YahooWeather |

### 5) Top Paid iOS Apps:

```
AppCategory and 
(userRanking some xsd:float[>=4.0]) and
(hasUserRatingCount some xsd:integer[>=2000]) and 
(price some xsd:float[>0.0]) and
developedFor value iOS
```

#### Result

|   Instances   |
|:-------------:|
|     Shazam    |
| SwiftKeyboard |