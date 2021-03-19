# <ins>Mobile Applications Ontology: SPARQL Queries</ins>
Once the ontology is complete, you can query the model created for a better understanding of the classification.
This section shows some <ins>**SPARQL queries**</ins> used to extrapolate important results.

### Most used programming language for Mobile Application development:

```
AppCategory and 
(firstVersionReleaseDate some xsd:dateTime[>=2016-01-01T00:00:00 ]) 
and 
(firstVersionReleaseDate some xsd:dateTime[<=2021-01-01T00:00:00 ])
```