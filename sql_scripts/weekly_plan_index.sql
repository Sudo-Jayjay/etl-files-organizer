/* This is a weekly cadence to identify new Plans that are not in our main Look up tables.
 
 
 
 --- Use this code to send 1 file to Brian
 
 
 
 ---Copy Script and run in SQL Server
 
 */
DROP TABLE Combined_Pat_Phy_NewPlans
SELECT COMBINED.* INTO Combined_Pat_Phy_NewPlans
FROM (
        SELECT [STRATA_PLAN_CODE],
            [MARKET],
            [PLAN1_DESC],
            [CONTRACT_PRODUCT],
            [TOP_PAYOR],
            [AFFILIATE_NAME],
            [PRODUCT2],
            [PRODUCT3],
            [KI_PAYOR],
            [KI_PAYOR_CLASS],
            [SSPG],
            [STATE],
            [NETWORK_STATUS],
            [NET_REV_PAYOR_GROUP],
            [Tag]
        FROM dbo.PLAN_INDEX_MISSING_PAT_WEEKLY_FINAL_Weekly ----FROM PHYSICIAN_CONSOL
        UNION ALL
        SELECT [STRATA_PLAN_CODE],
            [MARKET],
            [PLAN1_DESC],
            [CONTRACT_PRODUCT],
            [TOP_PAYOR],
            [AFFILIATE_NAME],
            [PRODUCT2],
            [PRODUCT3],
            [KI_PAYOR],
            [KI_PAYOR_CLASS],
            [SSPG],
            [STATE],
            [NETWORK_STATUS],
            [NET_REV_PAYOR_GROUP],
            [Tag]
        FROM PLAN_INDEX_MISSING_PHY_WEEKLY_FINAL_Weekly --- from PAT_CONSOL
    ) AS COMBINED
ORDER BY STRATA_PLAN_CODE,
    MARKET ---Send this file to Brian
select *
from Combined_Pat_Phy_NewPlans
order by Strata_PLAN_CODE ------Distinct Strata_Plan_Code
SELECT DISTINCT [STRATA_PLAN_CODE],
    [MARKET]
FROM Combined_Pat_Phy_NewPlans ---Check if there are new facility. Run attached script