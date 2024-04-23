CREATE SCHEMA IF NOT EXISTS data_science

-- 2.2.1) 2276 Unique Ships
SELECT COUNT(DISTINCT imo) AS Ship_Count
	   FROM data_science.vessel_info
	
/* 
2.2.2) ULCV - Ultra Large Container Vessel
	   According to Wikipedia an ULCV needs to meet the following requirements:
										    - Capacity(TEU): 14,501 and higher
										    - Length(m): 366 and longer
										    - Width(m): 49 and wider
	   1 TEU = 10 tons therefore I will classify a ship as ULCV with the following where clauses.
*/
SELECT COUNT(*) AS ULCV_Count 
	   FROM data_science.vessel_info 
WHERE data_science.vessel_info.dwt >= 145010
	   AND data_science.vessel_info.length >= 366
	   AND data_science.vessel_info.width >= 49


-- 2.2.3) List of 284 rows returned
SELECT * 
	FROM data_science.vessel_ports
WHERE LEFT(data_science.vessel_ports.code, 2) != data_science.vessel_ports.country_code
