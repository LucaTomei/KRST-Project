# <ins>Mobile Applications Ontology: SPARQL Queries</ins>
Once the ontology is complete, you can query the model created for a better understanding of the classification.
This section shows some <ins>**SPARQL queries**</ins> used to extrapolate important results.

## 1) Top Rated Free iOS Apps

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

## 2) Trending Android Apps For Music

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


## 3) All Developers who have developed an application in the Games category and who are over 25 years old

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX app: <http://www.semanticweb.org/lucasmac/ontologies/2021/2/mobile_applications#>

SELECT DISTINCT ?Developer ?Age ?Application
WHERE {
	?Developer rdf:type app:Developer.
	?Developer app:hasAge ?Age.
	FILTER (?Age >25).
	?Application rdf:type/rdfs:subClassOf* app:Games.
	?Developer app:isDeveloperOf ?Application.
}
ORDER BY ?Age
```

## 4) The youngest successful application Developer

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

## 5) Top rated application developed in Java between 2019 and 2021 developed by a Producer that has branch in United States

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