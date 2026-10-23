\# GeoServer Configuration



\## Purpose

GeoServer provides a service for publishing and accessing geographic data.



\## Local Setup

\- GeoServer version: 2.27.2

\- Local service URL: `http://localhost:8080/geoserver`

\- Workspace: `cite`

\- Store: `schools`

\- Published layer: `cite:gis\_osm\_buildings\_a\_free\_1`

\- Coordinate reference system: EPSG:4326



\## Verification

The published layer was queried through the Web Feature Service (WFS), and 1,062 features were returned during testing.



\## Limitations

This document records the local development configuration. Access restrictions and deployment security should be independently verified before production use.



\## Security

Do not include GeoServer passwords, authentication tokens, or other secrets in the submission archive.

