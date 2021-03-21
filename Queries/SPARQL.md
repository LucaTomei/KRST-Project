# <ins>Mobile Applications Ontology: SPARQL Queries</ins>
Once the ontology is complete, you can query the model created for a better understanding of the classification.
This section shows some <ins>**SPARQL queries**</ins> used to extrapolate important results.

## 1) Top 2 heaviest (in terms of bytes) applications in the store

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX foaf: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT DISTINCT ?Application (str(?bytes) as ?byte_app_size) ?Producer
WHERE {
	?Application rdf:type/rdfs:subClassOf* foaf:AppCategory.
	?Application foaf:appSize ?bytes.
	?Producer foaf:isProducerOf ?Application.
}
ORDER BY DESC(?bytes)
LIMIT 2
```

#### Result

| **Application** | **byte_app_size** |   **Producer**  |
|:-----------:|:-------------:|:-----------:|
|  PaypalApp  |   278119424   |    Paypal   |
|   Facebook  |   268193792   | FacebookInc |

## 2) Top Rated Free iOS Apps

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX app: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT DISTINCT ?name 
WHERE {
	?x app:price ?price.
	FILTER (?price =0.0).
	?x app:name ?name.
	?x app:hasUserRatingCount ?userRating.
	FILTER (?userRating >50000).
	?x app:developedFor ?iOS.	
}
```

#### Result

|      **name**      |
|:------------------:|
|    Runtastic Pro   |
|       Spotify      |
|      PaypalApp     |
| Whatsapp Messenger |
|       Twitter      |
|     GoogleMaps     |

## 3) Trending Android Apps For Music

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX app: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT DISTINCT ?x  (str(?price) as ?pricestr) 
WHERE {
	?x app:userRanking ?userRanking.
	FILTER (?userRanking >4).
	?x app:developedFor ?Android.
	?x app:price ?price.
	?x app:hasUserRatingCount ?userRating.
	FILTER (?userRating >50000).
	?x rdf:type app:Music
}
```

#### Result

|    x    | price |
|:-------:|:-----:|
| Spotify |  0.0  |


## 4) All Developers who have developed an application in the Games category and who are over 25 years old

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX app: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT DISTINCT ?Developer (str(?Age) as ?age)  ?Application
WHERE {
	?Developer rdf:type app:Developer.
	?Developer app:hasAge ?Age.
	FILTER (?Age >25).
	?Application rdf:type/rdfs:subClassOf* app:Games.
	?Developer app:isDeveloperOf ?Application.
}
ORDER BY ?Age
```

#### Result

|    Developer   | age |  Application |
|:--------------:|:---:|:------------:|
|  Jaako_Iisalo  |  32 |  AngryBirds  |
| Anton_Sitnikov |  36 | WorldOfTanks |

## 5) The youngest successful application Developer

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX foaf: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT ?Developer (str(?Age) as ?age) ?Application
WHERE {
	?Developer foaf:isDeveloperOf ?Application.
	?Developer foaf:hasAge ?Age
	{
		SELECT (min(?y) as ?Age)
		WHERE {?Developer foaf:hasAge ?y}
	}
	?Application foaf:hasUserRatingCount ?userRating.
	FILTER (?userRating >3000).
	?Application foaf:userRanking ?userRanking.
	FILTER (?userRanking >4).
}
```

#### Result

|    Developer   | age | Application |
|:--------------:|:---:|:-----------:|
| Ludovix_Haraux |  24 |   Shapr3D   |

## 6) Top rated application developed in Java between 2019 and 2021 developed by a Producer that has branch in United States

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX foaf: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT DISTINCT ?Application ?Producer (str(?Ranking) as ?ranking) (str(?releaseDate) as ?first_release)  (str(?currReleaseDate) as ?latest_update)
WHERE {
	?Application rdf:type/rdfs:subClassOf* foaf:AppCategory.
	?Application foaf:userRanking ?Ranking
	{
		SELECT (max(?y) as ?Ranking)
		WHERE {?Application foaf:userRanking ?y}
	}
	?Application foaf:hasLanguage* ?Java.
	?Application foaf:firstVersionReleaseDate ?releaseDate
	FILTER (?releaseDate > "2019-01-01T00:00:00Z"^^xsd:dateTime)
	?Application foaf:currVersionReleaseDate ?currReleaseDate
	FILTER (?releaseDate < "2021-01-01T00:00:00Z"^^xsd:dateTime)
	?Producer foaf:hasBranchIn ?United_States.
	?Producer foaf:isProducerOf ?Application.
}
```

#### Result

| Application | Producer | ranking |     first_release    |     latest_update    |
|:-----------:|:--------:|:-------:|:--------------------:|:--------------------:|
|  PaypalApp  |  Paypal  | 4.81788 | 2019-02-03T08:00:00Z | 2021-03-08T16:31:37Z |

## 7) Most used cross-platform backend programming language in application development

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX foaf: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT  ?Language (COUNT(?Language) as ?backend) 
WHERE {
	?Application rdf:type/rdfs:subClassOf* foaf:AppCategory.
	?Application foaf:hasBackendLanguage ?Language.
	?Language foaf:isCrossPlatform ?cross.
}
GROUP BY ?Language
ORDER BY DESC(?backend)
LIMIT 1
```

#### Result 

| Language | backend |
|:--------:|:-------:|
|    C++   |    9    |

## 8) Developers working from top rated application producers in a nation

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX foaf: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT  DISTINCT ?Nation  ?Producer ?Application  (str(?userRanking) as ?userRankingCount)
WHERE {
	?Nation rdf:type foaf:Nation.
	?Developer rdf:type foaf:Developer.
	?Producer rdf:type foaf:Producer.
	?Developer foaf:worksIn ?Producer.
	?Producer foaf:hasBranchIn ?Nation.
	?Application rdf:type/rdfs:subClassOf* foaf:AppCategory.
	?Developer foaf:isDeveloperOf ?Application.
	?Application foaf:userRanking ?userRanking.
	FILTER (?userRanking >4.5).
}
```