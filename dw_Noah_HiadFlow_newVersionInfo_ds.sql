# File Name: dw_Noah_HiadFlow_newVersion_ds.sql
# Copyright(C)Huawei Technologies Co.,Ltd.1998-2014.All rights reserved.
# Purpose:
# Describe：
# Input: ods_hispace_oper_log_dm; ods_hispace_terminal_code_dm
# Output: dw_Noah_HiadFlow_newVersion_ds.sql
# Author: gongbenwei/g00356913
# Creation Date:  2016-10-27
# Last Modified:  2016-11-21
# Last Modified By: gongbenwei/g00356913
# Change History:
#-------------------------------------------------------------------------
#!/bin/bash


hive -e "
use biwarehouse;

CREATE EXTERNAL TABLE IF NOT EXISTS noahwarehouse.dw_Noah_HiadFlow_newVersion_ds
(
    hispace_app_id           STRING,
    logon_id                 STRING,
    oper_time                STRING,
    oper_type                STRING,
    source                   STRING,
    subsource                STRING,
    listid                   STRING,
    position                 STRING,
    expand                   STRING
)
PARTITIONED BY(pt_d STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'        
STORED AS TEXTFILE
LOCATION '/user/BIResearch/DW/hiad/dw_Noah_HiadFlow_newVersion_ds';

INSERT OVERWRITE TABLE noahwarehouse.dw_Noah_HiadFlow_newVersion_ds PARTITION(pt_d='$date')
INSERT OVERWRITE TABLE noahwarehouse.dw_Noah_HiadFlow_newVersion_ds PARTITION(pt_d='$date')
SELECT 
    t1.hispace_app_id,
    t1.logon_id,
    t1.oper_time,
    t1.oper_type,
    t1.source,
    t1.subsource,
    t1.listid,
    t1.position,
    t1.expand
FROM 
(
    select 
    hispace_app_id, 
    logon_id,
    oper_time,
    oper_type,
    source,
    subsource,
    listid,
    position,
    expand
    from ods_hispace_oper_log_dm where pt_d='$date' AND biwarehouse.IsDeviceIdLegal(biwarehouse.deviceId_UDF(logon_id)) and length(logon_id)>=10 AND not source like '%search%' AND hispace_app_id is not null and hispace_app_id !='' AND listid is not null and listid !='' AND lower(source) like '%hiad%'
    group by hispace_app_id,logon_id,oper_time,oper_type,source,subsource,listid,position,expand 
)t1
JOIN
(
    select * from ods_hispace_terminal_code_dm where pt_d='$date' AND valuetype='7' AND localvalue like '7.%' and localvalue>='7.1.0'
)t2
ON t2.signvaluie = substr(t1.logon_id,9,2)
"