# Minecraft MCA Browser
*Based on [Dinnerbone's Coordinate Tools](https://dinnerbone.com/minecraft/tools/coordinates/).*

Allows you to find .mca files within a folder based on a coordinate range.

```bash
$ python3 main.py -p '/example/minecraft/world/region' -s 'in' -1300 0 1200 1500 0 -1234

------------------------------------
Number of possible .mca files: 6
List of files based in a real folder?: Yes

== SELECTION DETAILS ==
Block coordenates: "-1536 0 -1536 to 1535 511 1535"
Chunk coordenates: "-96 0 -96 to 95 31 95"
=======================
------------------------------------

Showing .mca files from "/example/minecraft/world/region" that are ->WITHIN<- the indicated coordinates:

'r.-3.-3.mca' 'r.-2.-3.mca' 'r.-1.-3.mca' 'r.0.-3.mca' 'r.1.-3.mca' 'r.2.-3.mca'
```

## Requeriments
* Python3

