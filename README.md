### Description
This script takes a Fedora 3 object and datastream store and parses the MODS records to find and 
count the distinct XPaths.

### Usage
This script takes 4 parameters.

`-o` or `--objectstore` defines the root directory of the Fedora objectstore (required)

`-d-` or `--datastreamstore` defines the root directory of the Fedora datastreamstore (required).

`-l` or `--hash_length` defines the directory hash length used when locating datastreams from their objects.
This has a default of `2` (optional).

`-n` or `--namespaces` is a comma separated list of namespaces to parse, otherwise the file is skipped not parsed.
Defaults to `islandora` only (optional). 

Currently this prints to the standard out the files being processed and a list of 
Xpaths and counts at the end.

#### Example execution

```
> ./mods_crawler.py -o objectStore -d datastreamStore
Processing objectstore file /data/objectStore/0d/info%3Afedora%2Fislandora%3Asp%5Fbasic%5Fimage%5Fcollection
Processing objectstore file /data/objectStore/66/info%3Afedora%2Fislandora%3Asp%5Fweb%5Farchive%5Fcollection
Processing objectstore file /data/objectStore/50/info%3Afedora%2Fislandora%3Amaps
Skipping /data/objectStore/6f/info%3Afedora%2Ffedora-system%3AContentModel-3.0 due to namespace restrictions.
Processing objectstore file /data/objectStore/51/info%3Afedora%2Fislandora%3Acompound%5Fcollection
Skipping /data/objectStore/0b/info%3Afedora%2Fir%3AthesisCModel due to namespace restrictions.
Processing objectstore file /data/objectStore/0e/info%3Afedora%2Fislandora%3AbookCModel
Processing objectstore file /data/objectStore/02/info%3Afedora%2Fislandora%3A1173.36
Processing objectstore file /data/objectStore/a4/info%3Afedora%2Fislandora%3A45
Processing objectstore file /data/objectStore/d1/info%3Afedora%2Fislandora%3Aaudio%5Fcollection
Processing objectstore file /data/objectStore/bc/info%3Afedora%2Fislandora%3A29
Processing objectstore file /data/objectStore/d8/info%3Afedora%2Fislandora%3Asp%5Fpdf%5Fcollection
Processing objectstore file /data/objectStore/e5/info%3Afedora%2Fislandora%3A38
Skipping /data/objectStore/e5/info%3Afedora%2Ffedora-system%3AFedoraObject-3.0 due to namespace restrictions.
Processing objectstore file /data/objectStore/f4/info%3Afedora%2Fislandora%3AorganizationCModel
Processing objectstore file /data/objectStore/c7/info%3Afedora%2Fislandora%3A13
Processing objectstore file /data/objectStore/ee/info%3Afedora%2Fislandora%3Avideo%5Fcollection
Processing objectstore file /data/objectStore/ee/info%3Afedora%2Fislandora%3Asp%5Fpdf
Processing objectstore file /data/objectStore/e4/info%3Afedora%2Fislandora%3A39
Processing objectstore file /data/objectStore/ed/info%3Afedora%2Fislandora%3A9
Processing objectstore file /data/objectStore/7d/info%3Afedora%2Fislandora%3A44
Processing objectstore file /data/objectStore/89/info%3Afedora%2Fislandora%3A6
Processing objectstore file /data/objectStore/73/info%3Afedora%2Fislandora%3Asp%5Flarge%5Fimage%5Fcmodel
Processing objectstore file /data/objectStore/87/info%3Afedora%2Fislandora%3A40
Processing objectstore file /data/objectStore/87/info%3Afedora%2Fislandora%3AnewspaperIssueCModel
Processing objectstore file /data/objectStore/80/info%3Afedora%2Fislandora%3A5
Processing objectstore file /data/objectStore/80/info%3Afedora%2Fislandora%3A42
Processing objectstore file /data/objectStore/80/info%3Afedora%2Fislandora%3AcollectionCModel
Processing objectstore file /data/objectStore/21/info%3Afedora%2Fislandora%3Amusic
Processing objectstore file /data/objectStore/81/info%3Afedora%2Fislandora%3A3
Processing objectstore file /data/objectStore/38/info%3Afedora%2Fislandora%3A7
Skipping /data/objectStore/9a/info%3Afedora%2Fir%3AcitationCollection due to namespace restrictions.
Processing objectstore file /data/objectStore/36/info%3Afedora%2Fislandora%3A53
Processing objectstore file /data/objectStore/5d/info%3Afedora%2Fislandora%3AcMsGnfaetIQr96ZD
Processing objectstore file /data/objectStore/91/info%3Afedora%2Fislandora%3Asp%5Fbasic%5Fimage
Processing objectstore file /data/objectStore/65/info%3Afedora%2Fislandora%3A50
Processing objectstore file /data/objectStore/96/info%3Afedora%2Fislandora%3AlggKmEA3Pbsv9zhs
Skipping /data/objectStore/96/info%3Afedora%2Ffedora-system%3AServiceDefinition-3.0 due to namespace restrictions.
Processing objectstore file /data/objectStore/54/info%3Afedora%2Fislandora%3Aentity%5Fcollection
Processing objectstore file /data/objectStore/08/info%3Afedora%2Fislandora%3Asubcollection
Processing objectstore file /data/objectStore/39/info%3Afedora%2Fislandora%3A55
Processing objectstore file /data/objectStore/99/info%3Afedora%2Fislandora%3A4
Processing objectstore file /data/objectStore/0f/info%3Afedora%2Fislandora%3A43
Processing objectstore file /data/objectStore/0f/info%3Afedora%2Fislandora%3AeventCModel
Processing objectstore file /data/objectStore/64/info%3Afedora%2Fislandora%3A41
Processing objectstore file /data/objectStore/d4/info%3Afedora%2Fislandora%3A36
Processing objectstore file /data/objectStore/ba/info%3Afedora%2Fislandora%3A54
Processing objectstore file /data/objectStore/b8/info%3Afedora%2Fislandora%3AentityCModel
Processing objectstore file /data/objectStore/af/info%3Afedora%2Fislandora%3A8
Processing objectstore file /data/objectStore/a1/info%3Afedora%2Fislandora%3Asp%5Fweb%5Farchive
Processing objectstore file /data/objectStore/e1/info%3Afedora%2Fislandora%3A37
Processing objectstore file /data/objectStore/f0/info%3Afedora%2Fislandora%3AnewspaperCModel
Processing objectstore file /data/objectStore/ff/info%3Afedora%2Fislandora%3Asp%5Fdisk%5Fimage%5Fcollection
Processing objectstore file /data/objectStore/ff/info%3Afedora%2Fislandora%3Asp%5Fdisk%5Fimage
Processing objectstore file /data/objectStore/c2/info%3Afedora%2Fislandora%3A57
Processing objectstore file /data/objectStore/f6/info%3Afedora%2Fislandora%3Anewspaper%5Fcollection
Processing objectstore file /data/objectStore/f1/info%3Afedora%2Fislandora%3AnewspaperPageCModel
Processing objectstore file /data/objectStore/cb/info%3Afedora%2Fislandora%3Asp-audioCModel
Processing objectstore file /data/objectStore/cb/info%3Afedora%2Fislandora%3ApersonCModel
Skipping /data/objectStore/48/info%3Afedora%2Fir%3AcitationCModel due to namespace restrictions.
Processing objectstore file /data/objectStore/48/info%3Afedora%2Fislandora%3Asp%5Flarge%5Fimage%5Fcollection
Processing objectstore file /data/objectStore/48/info%3Afedora%2Fislandora%3AplaceCModel
Processing objectstore file /data/objectStore/84/info%3Afedora%2Fislandora%3A56
Processing objectstore file /data/objectStore/15/info%3Afedora%2Fislandora%3ApageCModel
Skipping /data/objectStore/8c/info%3Afedora%2Ffedora-system%3AServiceDeployment-3.0 due to namespace restrictions.
Processing objectstore file /data/objectStore/76/info%3Afedora%2Fislandora%3AcompoundCModel
Processing objectstore file /data/objectStore/49/info%3Afedora%2Fislandora%3A1
Processing objectstore file /data/objectStore/78/info%3Afedora%2Fislandora%3AbookCollection
Processing objectstore file /data/objectStore/13/info%3Afedora%2Fislandora%3A2
Processing objectstore file /data/objectStore/13/info%3Afedora%2Fislandora%3Aroot
Processing objectstore file /data/objectStore/8e/info%3Afedora%2Fislandora%3Asp%5FvideoCModel

XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}titleInfo was used 46 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}name[@type="personal"] was used 21 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}name[@type="personal"]/{http://www.loc.gov/mods/v3}role was used 19 times
XPath /{http://www.loc.gov/mods/v3}mods was used 129 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}originInfo was used 61 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}language was used 27 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}physicalDescription was used 32 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}subject was used 94 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}subject/{http://www.loc.gov/mods/v3}hierarchicalGeographic was used 112 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}subject/{http://www.loc.gov/mods/v3}cartographics was used 25 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}recordInfo was used 11 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}originInfo/{http://www.loc.gov/mods/v3}place was used 39 times
XPath /{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}location was used 1 times

Done

``` 

### Maintainers
* [Jared Whiklo](https://github.com/whikloj)

### License
* [MIT](./LICENSE)
