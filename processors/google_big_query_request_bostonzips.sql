SELECT
  date,
  NET.SAFE_IP_FROM_STRING (client.IP) AS ip,
  a.MeanThroughputMbps AS MeanThroughputMbps,
  a.MinRTT AS MinRTT,
  client.Geo.city AS City,
  client.Network.ASNumber AS ProviderNumber,
  client.Network.ASName AS ProviderName,
  client.Geo.Subdivision2ISOCode AS Subdivision2ISOCode,
  client.Geo.Subdivision2Name AS Subdivision2Name,
  client.Geo.PostalCode AS PostalCode,
  client.Geo.MetroCode AS MetroCode,
  client.Geo.AreaCode AS AreaCode,
  client.Geo.Latitude AS Latitude,
  client.Geo.Longitude AS Longitude,
  client.Geo.AccuracyRadiusKm AS AccuracyRadiusKm
FROM
  `measurement-lab.ndt.unified_uploads`
WHERE
  client.geo.CountryCode = "US"
  AND client.Geo.region = "MA"
  AND client.Geo.City IN("Boston")
  AND client.Geo.PostalCode IN("02119","02120","02121","02122")
  AND date BETWEEN "2019-01-01"
  AND "2021-7-31"