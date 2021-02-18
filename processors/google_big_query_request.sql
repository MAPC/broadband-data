SELECT
  date,
  NET.SAFE_IP_FROM_STRING (client.IP) AS ip,
  a.MeanThroughputMbps AS MeanThroughputMbps,
  a.MinRTT AS MinRTT,
  client.Geo.city AS City,
  client.Network.ASNumber AS ProviderNumber,
  client.Network.ASName AS ProviderName
FROM
  `measurement-lab.ndt.unified_uploads`
WHERE
  client.geo.CountryCode = "US"
  AND client.Geo.region = "MA"
  AND client.Geo.City IN("Revere", "Everett", "Chelsea")
  AND date BETWEEN "2019-01-01"
  AND "2019-12-31"