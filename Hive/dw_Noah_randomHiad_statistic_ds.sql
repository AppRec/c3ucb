#------------------------------------------------------------------------
# File Name: dw_Noah_randomHiad_statistic_ds.sql
# Copyright(C)Huawei Technologies Co.,Ltd.1998-2014.All rights reserved.
# Purpose:
# Describe：
# Input: dw_Noah_randomFlow_StatisticInfo_ds
# Output: dw_Noah_randomHiad_statistic_ds.sql
# Author: gongbenwei/g00356913
# Creation Date:  2016-10-27
# Last Modified:  2016-11-02
# Last Modified By: gongbenwei/g00356913
# Change History:
#-------------------------------------------------------------------------
#!/bin/bash

export Base_Path=/srv/BigData/hadoop/data12/cuhk/DataFile

hive -e "
use biwarehouse;

CREATE EXTERNAL TABLE IF NOT EXISTS noahwarehouse.dw_Noah_randomHiad_DataInfo_ds
(
    device_id            STRING,
    dev_app_id           STRING,
    oper_time            STRING,
    oper_type            STRING,
    source               STRING,
    subsource            STRING,
    listid               STRING,
    position             STRING
)
PARTITIONED BY(pt_d STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'        
STORED AS TEXTFILE
LOCATION '/user/BIResearch/DW/hiad/dw_Noah_randomHiad_DataInfo_ds';

INSERT OVERWRITE TABLE noahwarehouse.dw_Noah_randomHiad_DataInfo_ds PARTITION(pt_d='$date')
INSERT OVERWRITE TABLE noahwarehouse.dw_Noah_randomHiad_DataInfo_ds PARTITION(pt_d='$date')
SELECT
    biwarehouse.deviceId_UDF(t1.logon_id) AS device_id,
    t2.dev_app_id AS dev_app_id,
    t1.oper_time,
    t1.oper_type,
    t1.source,
    t1.subsource,
    t1.listid,
    t1.position
FROM
(
    select * from noahwarehouse.dw_Noah_HiadFlow_newVersion_ds 
    WHERE pt_d='$date' and expand like '%random%' and listid in ('2', '25', 'zjbb', '5', '6', '18')
)t1
JOIN
(
    select
    IF(lower(substr(dev_app_id,1,1)) != 's', dev_app_id,substr(dev_app_id,2)) AS dev_app_id,
    hispace_app_id
    from dim_hispace_app_info_ds
    where dev_app_id IS NOT NULL and lower(dev_app_id) != '' and hispace_app_id is not NULL
    GROUP BY IF(lower(substr(dev_app_id,1,1)) != 's', dev_app_id,substr(dev_app_id,2)), hispace_app_id
)t2
ON t1.hispace_app_id = t2.hispace_app_id
ORDER BY device_id, listid, CAST(position AS INT);
"

hadoop fs -getmerge /user/BIResearch/DW/hiad/dw_Noah_randomHiad_DataInfo_ds/pt_d='$date' $Base_Path/Data_randomHiad_$date.txt
rm $Base_Path/.Data_randomHiad_$date.txt.crc
