# <ins>Mobile Applications Ontology: SPARQL Queries</ins>
Once the ontology is complete, you can query the model created for a better understanding of the classification.
This section shows some <ins>**SPARQL queries**</ins> used to extrapolate important results.

## Top Rated Free iOS Apps

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

## Trending Android Apps For Music

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


## All Developers who have created an application in the Games category and who are over 25 years old

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

## The youngest successful application programmer